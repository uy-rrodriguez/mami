#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Serveur :                                                              #
#        Classe contenant l'information d'un serveur.                       #
#                                                                           #
#    Format XML :                                                           #
#    -------------------------------------------------------------------    #
#        <data>                                                             #
#        ...                                                                #
#            <server>                                                       #
#                <name></name>                                              #
#                <ip></ip>                                                  #
#                <uptime></uptime>                                          #
#            </server>                                                      #
#        ...                                                                #
#        </data>                                                            #
#                                                                           #
#############################################################################

from arraydataobject import *


class Server(ArrayDataObject):

    def __init__(self, name="", ip="", uptime=""):
        super(Server, self).__init__()
        self.name     = name
        self.ip       = ip
        self.uptime   = uptime


def main():
    f = open('../test.xml', 'r')
    xml = f.read()

    print "Test parseObjetXML"
    s = Server()
    s.parseObjetXML(xml, "./server", ["name", "ip", "uptime"])
    print s.name, " ", s.ip, " ", s.uptime

    print "\nTest parseListXML"
    liste = Server.parseListXML(Server, xml, "./servers", ["name", "ip", "uptime"])
    for serv in liste:
        print serv.name, " ", serv.ip, " ", serv.uptime

    print "\nTest writeObjetXML"
    s.name = "Autre nom de serveur"
    s.ip = "xxx.xxx.xxx.yyy"
    s.uptime = "00 heures 00 minutes"
    print s.writeObjetXML(xml, "./server", ["name", "ip", "uptime"])

    print "\nTest writeListXML"
    for serv in liste:
        serv.name += "-MODIF"
        serv.ip += ":255"
        serv.uptime += " 20 seconds"
    print Server.writeListXML(liste, xml, "./servers", ["name", "ip", "uptime"])

if __name__=="__main__":
    main()






