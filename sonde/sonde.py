#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Interface :                                                            #
#        Module pour collecter les informations associés à cette machine    #
#        et les envoyer au système de stockage à distance.                  #
#        Le module recolte l'information à l'aide des commandes bash et     #
#        de la librairie psutils.                                           #
#        Ensuite il enregistre les données dans un fichier xml              #
#        respectant le format prédefini.                                    #
#        Finalement, il envoie ce fichier faisant appel à un webservice.    #
#                                                                           #
#############################################################################

import psutil
import time
from datetime import datetime
import subprocess
from os import path, sys
from operator import attrgetter
#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from util import util
from objets import cpu, disk, process, ram, server, swap, user, arraydataobject



#############################################################################
#    Constantes.                                                            #
#############################################################################

MAX_GREEDY = 10
SLEEP_TIME = 3

# Path et nom de base pour le fichier à générer, par rapport à l'addresse de
# ce fichier. Après le nom du fichier on ajoutera un suffix (genre, le nom
# du serveur et le timestamp) plus l'extension xml.
PATH_OUTPUT = "/../data/data_"



#############################################################################
#    Sonde. Classe principale du module.                                    #
#############################################################################


class Sonde(object):

    def __init__(self):
        self.cpu = cpu.CPU()
        self.ram = ram.RAM()
        self.server = server.Server()
        self.swap = swap.Swap()

        self.disks = []
        self.processes = []
        self.users = []

        self.count_processes = 0
        self.count_zombies = 0

        self.firstLoop = True


    def get_cpu_info(self):
        self.cpu.used = psutil.cpu_percent(1, percpu=False)


    def get_ram_info(self):
        data = psutil.virtual_memory()
        self.ram.used = data.used
        self.ram.total = data.total


    def get_swap_info(self):
        data = psutil.swap_memory()
        self.swap.used = data.used
        self.swap.total = data.total


    def get_server_info(self):
        script = path.dirname(path.abspath(__file__)) + "/get_server_info.sh"
        process = subprocess.Popen(["sh", script], stdout=subprocess.PIPE)
        output = process.communicate()[0].split("|")
        self.server.name = output[0]
        self.server.ip = output[1]
        self.server.uptime = output[2]


    def get_disks_info(self):
        self.disks = []
        for part in psutil.disk_partitions(all=False):
            data = psutil.disk_usage(part.mountpoint)
            d = disk.Disk()
            d.mnt = part.mountpoint
            d.total = data.total
            d.used = data.used
            self.disks.append(d)


    def get_processes_info(self):
        self.count_processes = len(psutil.pids())
        self.count_zombies = 0
        self.processes = []
        total_mem = psutil.virtual_memory().total

        for proc in psutil.process_iter():
            try:
                if (proc.status() == psutil.STATUS_ZOMBIE):
                    raise psutil.ZombieProcess(proc.pid)

                p = process.Process()
                p.pid = proc.pid
                p.command = proc.name()
                p.username = proc.username()
                p.cpu = proc.cpu_percent(interval=None)
                p.ram = proc.memory_info().rss
                p.percent_ram = round(p.ram * 100.0 / total_mem, 2)
                self.processes.append(p)

            except psutil.ZombieProcess:
                # "ZOMBIE ALERT!!"
                self.count_zombies += 1

            except psutil.NoSuchProcess, psutil.AccessDenied:
                pass


    def get_users_info(self):
        self.users = []
        script = path.dirname(path.abspath(__file__)) + "/get_user_info.sh"
        output = subprocess.check_output(["sh", script])

        # On cree un tableau a partir de la reponse, et on supprime le dernier element (un ligne vide)
        output = output.split("\n")[:-1]

        for line in output:
            data = line.split("|")
            u = user.User()
            u.uid = data[0]
            u.name = data[1]
            u.isroot = data[2]
            u.login_time = data[3]
            self.users.append(u)


    def print_info(self):
        print "CPU: ", self.cpu
        print "RAM: ", self.ram
        print "Server: ", self.server
        print "Swap: ", self.swap

        print "Disks:"
        for d in self.disks:
            print d

        print "Processes:"
        print "    Count: ", self.count_processes
        print "    Zombies: ", self.count_zombies
        for p in self.processes:
            print p

        print "Users:"
        for u in self.users:
            print u


    def collect(self):
        self.get_cpu_info()
        self.get_ram_info()
        self.get_server_info()
        self.get_swap_info()
        self.get_disks_info()
        self.get_users_info()

        # On obtient tous les processus et on garde les 10 premiers
        # si c'est la premiere fois qu'on boucle, on obtient deux fois l'info des processus,
        # parce que le pourcentage de CPU du premier passage n'est pas valide
        if self.firstLoop:
            self.firstLoop = False
            self.get_processes_info()

        self.get_processes_info()
        self.processes.sort(reverse=True)
        self.processes = self.processes[:MAX_GREEDY]

        # Ecriture du fichier XML
        baseXML = path.dirname(path.abspath(__file__)) + "/base.xml"
        fBase = open(baseXML, "r")
        firstLine = fBase.readline()
        xml = fBase.read()
        fBase.close()

        timestamp = "" #time.strftime("%Y%m%d_%H%M%s", time.localtime())
        suffix = "" #self.server.name + "_" + timestamp
        outXML = path.dirname(path.abspath(__file__)) + PATH_OUTPUT + suffix + ".xml"
        fOut = open(outXML, "w")

        xml = self.cpu.write_objet_xml(xml, "./cpu", ["used"])
        xml = self.ram.write_objet_xml(xml, "./ram", ["used", "total"])
        xml = self.swap.write_objet_xml(xml, "./swap", ["used", "total"])
        xml = self.server.write_objet_xml(xml, "./server", ["name", "ip", "uptime"])
        xml = disk.Disk.write_list_xml(self.disks, xml, "./disks", ["mnt", "used", "total"])
        xml = user.User.write_list_xml(self.users, xml, "./users", ["uid", "name", "isroot", "login_time"])

        pseudoProcess = arraydataobject.ArrayDataObject()
        pseudoProcess.count = self.count_processes
        pseudoProcess.zombies = self.count_zombies
        xml = pseudoProcess.write_objet_xml(xml, "./processes", ["count", "zombies"])
        xml = process.Process.write_list_xml(self.processes, xml, "./processes", ["pid", "command", "username", "cpu", "ram"])

        fOut.write(firstLine)
        fOut.write(xml)
        fOut.close()



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    s = Sonde()
    while True:
        s.collect()
        time.sleep(SLEEP_TIME)

if __name__=='__main__':
    main()

