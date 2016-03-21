#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Test :                                                                 #
#        Fichier pour tester la lecture et écriture XML.                    #
#                                                                           #
#                                                                           #
#############################################################################

from objets import *
from objets.cpu import *
from objets.disk import *
from objets.process import *
from objets.ram import *
from objets.server import *
from objets.swap import *
from objets.user import *


def main():
    f = open("data/test.xml", "r")
    xml = f.read()

    print "Test serveur:"
    s = Server()
    s.parse_objet_xml(xml, "./server", ["name", "ip", "uptime"])
    print s.name, " ", s.ip, " ", s.uptime

    print "Test CPU:"
    c = CPU()
    c.parse_objet_xml(xml, "./cpu", ["used"])
    print c.used

    print "Test RAM:"
    ram = ArrayDataObject()
    ram.parse_objet_xml(xml, "./ram", ["used", "total"])
    print ram.used, " ", ram.total, " ", int(ram.used) * 100 / int(ram.total), "%"

    print "\nTest disques"
    disques = ArrayDataObject.parse_list_xml(xml, "./disks", ["used", "total"])
    for d in disques:
        print d.used, " ", d.total

    print "\nTest utilisateurs"
    users = User.parse_list_xml(xml, "./users", ["name", "uid", "groupid", "isroot", "gname", "logintime"])
    for d in users:
        print d.name, " ", d.uid, " ", d.groupid, " ", d.isroot, " ", d.gname, " ", d.logintime

    print "\nTest swap"
    swap = Swap()
    swap.parse_objet_xml(xml, "./swap", ["used", "total"])
    print swap.used, " ", swap.total

    print "\nTest processus"
    proc = Process()
    proc.parse_objet_xml(xml, "./processes", ["count", "zombies"])
    print proc.count, " ", proc.zombies

    print "\nTest greedy"
    greedies = Process.parse_list_xml(xml, "./processes/greedy", ["pid", "cpu", "ram", "command"])
    for g in greedies:
        print g.pid, " ", g.cpu, " ", g.ram, " ", g.command

if __name__=="__main__":
    main()






