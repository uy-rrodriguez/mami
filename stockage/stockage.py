#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Stockage :                                                             #
#        Module pour stocker les données XML recues des sondes et copiées   #
#        par le webservice dans un repértoire local.                        #
#                                                                           #
#############################################################################

import sys
import sqlite3
import pickle
import time
import glob
import os

from lxml import etree
from objets import cpu, disk, process, ram, server, swap, user, arraydataobject

from interface.config import Config


#############################################################################
#    Constantes.                                                            #
#############################################################################

DELAY = 10
FILES_PATTERN = "data/data_*.xml"
PATH = "data/sonde_info.db"



#############################################################################
#    Stockage. Classe principale du module.                                 #
#############################################################################

class Stockage:
    def __init__(self):
        #print "Stockage";
        self.cpu = cpu.CPU()
        self.ram = ram.RAM()
        self.server = server.Server()
        self.swap = swap.Swap()

        self.disks = []
        self.processes = []
        self.users = []
        self.count_p = 0
        self.count_z = 0
        self.count_u = 0


    def parse_xml(self,doc):
        tree = etree.parse(doc)

        self.server.name = tree.xpath("/data/server/name/text()")[0]
        self.server.ip = tree.xpath("/data/server/ip/text()")[0]
        self.server.uptime = tree.xpath("/data/server/uptime/text()")[0]
        self.cpu.used = tree.xpath("/data/cpu/used/text()")[0]
        self.ram.total = tree.xpath("/data/ram/total/text()")[0]
        self.ram.used = tree.xpath("/data/ram/used/text()")[0]
        self.swap.used = tree.xpath("/data/swap/used/text()")[0]
        self.swap.total = tree.xpath("/data/swap/total/text()")[0]

        for disk_info in tree.xpath("/data/disks/disk"):
            d = disk.Disk()
            d.mnt = disk_info.find("mnt").text
            d.total = disk_info.find("total").text
            d.used = disk_info.find("used").text
            self.disks.append(d)

        #self.swap.used = tree.xpath("/data/swap/used/text()")[0]
        #self.swap.total = tree.xpath("/data/swap/total/text()")[0]

        for user_info in tree.xpath("/data/users/user"):
            u = user.User()
            u.name = user_info.find("name").text
            u.uid = user_info.find("uid").text
            #u.gid = user_info.find("gid").text
            u.isroot = user_info.find("isroot").text
            #u.gname = user_info.find("gname").text
            u.login_time = user_info.find("login_time").text
            self.users.append(u)
            self.count_u += 1

        self.count_p = tree.xpath("/data/processes/count/text()")[0]
        self.count_z = tree.xpath("/data/processes/zombies/text()")[0]


        for process_info in tree.xpath("/data/processes/process"):
            p = process.Process()
            p.pid = process_info.find("pid").text
            p.cpu = process_info.find("cpu").text
            p.ram = process_info.find("ram").text
            p.command = process_info.find("command").text
            p.username = process_info.find("username").text
            self.processes.append(p)


    def stockage_bdd(self):
        conn = sqlite3.connect(PATH)
        c = conn.cursor()

        now = time.time()

        # On cherche le serveur, s'il existe on met à jour les données. Sinon on faiot une insertion.
        cursor = c.execute("SELECT * FROM server WHERE name = ?", [str(self.server.name)])
        res = cursor.fetchone()

        if res != None:
            # Dans ce cas, on fait un update
            c.execute("""UPDATE server SET ip = ?, uptime = ?
                           WHERE name = ?;""",
                      (str(self.server.ip),
                       str(self.server.uptime),
                       str(self.server.name)))

        else:
            # On insère un nouveau serveur
            c.execute("""INSERT INTO server (name, ip , uptime)
                           VALUES (?, ?, ?);""",
                      (str(self.server.name),
                       str(self.server.ip),
                       str(self.server.uptime)))


        # Insertion des autres données
        c.execute("""INSERT INTO stat (server_name,
                                        cpu_used,
                                        ram_used,
                                        ram_total,
                                        swap_used,
                                        swap_total,
                                        processes_count,
                                        zombies_count,
                                        users_count,
                                        timestamp)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (str(self.server.name),
                   str(self.cpu.used),
                   str(self.ram.used),
                   str(self.ram.total),
                   str(self.swap.used),
                   str(self.swap.total),
                   str(self.count_p),
                   str(self.count_z),
                   str(self.count_u),
                   now))


        for d in self.disks:
            c.execute("""INSERT INTO statDisk (server_name,
                                                mnt,
                                                used,
                                                total,
                                                timestamp)
                          VALUES (?, ?, ?, ?, ?)""",
                      (str(self.server.name),
                       str(d.mnt),
                       str(d.used),
                       str(d.total),
                       now))


        pickleusers = sqlite3.Binary(pickle.dumps(self.users, pickle.HIGHEST_PROTOCOL))

        c.execute("""INSERT INTO user (server_name, users_list, timestamp) VALUES (?, ?, ?)""",
                  (str(self.server.name),
                   sqlite3.Binary(pickleusers),
                   now))

        pickleprocesses = pickle.dumps(self.processes, pickle.HIGHEST_PROTOCOL)

        c.execute("""INSERT INTO process (server_name, greedy_list, timestamp) VALUES (?, ?, ?)""",
                    (str(self.server.name),
                     sqlite3.Binary(pickleprocesses),
                     now))

        conn.commit()
        conn.close()


    # Cette fonction permet de supprimer les données anciennes de la BDD
    def nettoyage_bdd(self):
        conn = sqlite3.connect(PATH)
        c = conn.cursor()

        # Pour chaque table, on obtient le nombre d'enregistrements et on supprime les anciens
        tables = ["stat", "statDisk", "user", "process"]
        for table in tables:

            # Nombre d'enregistrements
            count = c.execute("SELECT COUNT(*) FROM " + table + " WHERE server_name = ?",
                              [self.server.name]).next()[0]

            # On supprime les derniers X, pour laisser juste la quantité configurée
            maxRows = Config().get("db/max_rows")

            for i in range(int(maxRows), int(count)):
                timestampDelete = c.execute("SELECT MIN(timestamp) FROM " + table + " WHERE server_name = ?",
                                            [self.server.name]).next()[0]

                c.execute("DELETE FROM " + table
                          + " WHERE timestamp = ? "
                          + "     AND server_name = ?", [timestampDelete, self.server.name])
                conn.commit()

        conn.close()




#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    try :
        print "Stockage : Démarrage du service. Ctrl+C pour arrêter."
        while True:
            try:
                # On parcourt les fichiers télechargés, en cherchant par le
                # modèle de nom qu'ils doivent avoir.
                for f in glob.glob(FILES_PATTERN):
                    print "Stockage : Traitement du fichier " + f
                    s = Stockage()
                    s.parse_xml(f)
                    s.stockage_bdd()
                    os.remove(f)

                    # On vérifie la quantité d'enregistrements dans la table et on
                    # supprime les plus anciens
                    s.nettoyage_bdd()

                # Puis on attend quelques secondes
                time.sleep(DELAY)

            except Exception, e:
                print "Stockage : ", e

    except KeyboardInterrupt:
        print ""

    #cmdargs = (sys.argv)
    #c = Stockage()
    #c.parse_xml(cmdargs[1])
    #c.stockage_bdd()

if __name__=='__main__':
    main()

