#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Stockage :                                                             #
#        Module pour .....                                                  #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################



#############################################################################
#    Stockage. Classe principale du module.                                 #
#############################################################################

import sys
import sqlite3
import pickle

from lxml import etree
from objets import cpu, disk, process, ram, server, swap, user, arraydataobject

class Stockage:
    def __init__(self):
        print "Stockage";
        self.cpu = cpu.CPU()
        self.ram = ram.RAM()
        self.server = server.Server()
        self.swap = swap.Swap()

        self.disks = []
        self.processes = []
        self.users = []
        self.count_p = 0
        self.count_z = 0
    


    def parse_xml(self,doc):
	tree = etree.parse(doc)
	self.server.name = tree.xpath("/data/server/name")
	self.server.ip = tree.xpath("/data/server/ip")
        self.uptime = tree.xpath("/data/server/uptime")
        self.cpu = tree.xpath("/data/cpu/used")
        self.ram.total = tree.xpath("/data/ram/total")
        self.ram.used = tree.xpath("/data/ram/used")
        
        for disk in tree.xpath("/data/disks"):
            disk.get("mnt")
            disk.get("total")
            disk.get("used")
        
        self.swap.used = tree.xpath("/data/swap/used")
        self.swap.total = tree.xpath("/data/swap/total")
        
        for user_info in tree.xpath("/data/users"):
            u = user.User()
            u.name = user_info.get("name")
            u.uid = user_info.get("uid")
            u.gid = user_info.get("gid")
            u.isroot = user_info.get("isroot")
            u.gname = user_info.get("gname")
            u.login_time = user_info.get("login_time")
            self.users.append(u)
        
	self.count_p = tree.xpath("/data/processes/count")      
	self.count_z = tree.xpath("/data/processes/zombies")      


        for process_info in tree.xpath("/data/processes/greedy"):
	    p = process.Process()
            p = process_info.get("pid")
	    p = process_info.get("cpu")
	    p = process_info.get("ram")
	    p = process_info.get("command")
            self.process.append(p)

       
    def stockage(self)
        conn = sqlite3.connect(PATH)        
        c.executescript("""INSERT INTO server (name, ip , uptime)
                           VALUES ?,?,? ;""",self.server.name,self.server.ip,self.server.uptime)

        c.executescript("""INSERT INTO stat (server_name, date, cpu_used, ram_used, ram_total, swap_used,
                      swap_total, processes_count, zombies_count, users_count) VALUES ?,?,?,?""",)
        c.executescript("""""")

        picklestring = pickle.dumps(self.users)
        c.executescript("""INSERT INTO user (server_name , users_list""")

        picklestring = pickle.dumps(self.processes)
        c.executescript("""INSERT INTO process (server_name , users_list""")
             
	    

         

#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    cmdargs = (sys.argv)
    c = Stockage()
    c.parse_xml(cmdargs[1])

if __name__=='__main__':
    main()

