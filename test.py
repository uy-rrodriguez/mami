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
    f = open('test.xml', 'r')
    xml = f.read()

    print "Test serveur:"
    s = Server()
    s.parseObjetXML(xml, "./server", ["name", "ip", "uptime"])
    print s.name, " ", s.ip, " ", s.uptime

    print "Test CPU:"
    c = CPU()
    c.parseObjetXML(xml, "./cpu", ["used"])
    print c.used

    print "Test RAM:"
    ram = ArrayDataObject()
    ram.parseObjetXML(xml, "./ram", ["used", "total"])
    print ram.used, " ", ram.total, " ", int(ram.used) * 100 / int(ram.total), "%"

    print "\nTest disques"
    disques = ArrayDataObject.parseListXML(ArrayDataObject, xml, "./disks", ["used", "total"])
    for d in disques:
        print d.used, " ", d.total

    print "\nTest utilisateurs"
    users = User.parseListXML(User, xml, "./users", ["name", "uid", "groupid", "isroot", "gname", "logintime"])
    for d in users:
        print d.name, " ", d.uid, " ", d.groupid, " ", d.isroot, " ", d.gname, " ", d.logintime

    print "\nTest swap"
    swap = Swap()
    swap.parseObjetXML(xml, "./swap", ["used", "total"])
    print swap.used, " ", swap.total

    print "\nTest processus"
    proc = Process()
    proc.parseObjetXML(xml, "./processes", ["count", "zombies"])
    print proc.count, " ", proc.zombies

    print "\nTest greedy"
    greedies = Process.parseListXML(Process, xml, "./processes/greedy", ["pid", "cpu", "ram", "command"])
    for g in greedies:
        print g.pid, " ", g.cpu, " ", g.ram, " ", g.command

if __name__=="__main__":
    main()






