#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Crisis :                                                               #
#        Petite classe qui sert comme module de ddétection de crises.       #
#        On utilise la configuration pour reconnaître une situation de      #
#        crise. À ce moment là on envoie un mail à l'administrateur         #
#        configuré.                                                         #
#        On impose un délai de 30 secondes entre chaque vérification.       #
#                                                                           #
#############################################################################

import os
import time

#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from objets.arraydataobject import ArrayDataObject
from objets.server import Server
from dbaccess import DBAccess
from config import Config
from mail import Mail


#############################################################################
#    Crisis.                                                                #
#############################################################################

class Crisis:
    DELAY = 30

    def __init__(self):
        # Connexion a la BD
        self.db = DBAccess()

        # On charge la configuration actuelle
        self.config = Config()

    def run(self):
        try:
            while True:
                # Les conditions de crises sont prises de la configuration
                maxCPU = self.config.get("crisis/max_cpu")
                maxRAM = self.config.get("crisis/max_ram")
                maxSwap = self.config.get("crisis/max_swap")
                maxDisk = self.config.get("crisis/max_disk")


                # On cherche les serveurs dans la BDD
                for s in self.db.get_all("server"):
                    server = Server(s["name"], s["ip"], s["uptime"])

                    # Obtention de la date la plus actuelle
                    lastDate = self.db.get_last_date(server.name).next()[0]

                    # Obtention des stats
                    res = self.db.get_by_fields("stat",
                                                ["server_name", "date"],
                                                [server.name, lastDate]).next()

                    resDisks = self.db.get_by_fields("statDisk",
                                                     ["server_name", "date"],
                                                     [server.name, lastDate])

                    # Création d'objets à partir des données
                    cpu = ArrayDataObject();
                    cpu.used = float(res["cpu_used"])

                    ram = ArrayDataObject();
                    ram.total = int(res["ram_total"]);
                    ram.used = float(res["ram_used"])

                    swap = ArrayDataObject();
                    swap.total = int(res["swap_total"]);
                    swap.used = float(res["swap_used"])

                    disks = []
                    for line in resDisks:
                        d = ArrayDataObject()
                        d.mnt = line["mnt"]
                        d.total = int(line["total"])
                        d.used = float(line["used"])
                        disks.append(d)


                    # Détection de situation de crise
                    ramPercent = ram.used * 100 / ram.total
                    swapPercent = ram.used * 100 / ram.total

                    disksTotalUsed = 0
                    disksTotal = 0
                    for d in disks:
                        disksTotalUsed += d.used
                        disksTotal += d.total

                    disksPercent = disksTotalUsed * 100 / disksTotal

                    if (cpu.used >= float(maxCPU)
                        or ramPercent >= float(maxRAM)
                        or swapPercent >= float(maxSwap)
                        or disksPercent >= float(maxDisk)):

                        # Classe pour envoyer des mails
                        mail = Mail()
                        mail.set_param("server.name", server.name)
                        mail.set_param("server.ip", server.ip)
                        mail.set_param("cpu.used",        "{:.1f}".format(cpu.used))
                        mail.set_param("ram.percent",     "{:.1f}".format(ramPercent))
                        mail.set_param("swap.percent",    "{:.1f}".format(swapPercent))
                        mail.set_param("disks.percent",   "{:.1f}".format(disksPercent))

                        mail.send(self.config.get("email/address"), self.config.get("email/subject"),
                                  self.config.get("email/template_html"), self.config.get("email/template_txt"))

                        print "Crise détectée. Un email a été envoyé à " + self.config.get("email/address")

                # Fin for

                time.sleep(self.DELAY)

                # Recharge de la configuration
                self.config.recharger()

            # Fin while

        except Exception, e:
            raise



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    try:
        print "Démarrage du service d'envoie d'alertes. Ctrl+C pour arrêter."
        c = Crisis()
        c.run()
    except KeyboardInterrupt:
        print ""

if __name__=='__main__':
    main()

