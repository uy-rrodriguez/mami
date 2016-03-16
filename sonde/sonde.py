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

'''
    FORMAT XML
    -------------------------------------------------------------------------
    <data timestamp=”timestamp_unix”>
        <server>
            <name></name>
            <ip></ip>
            <uptime></uptime>
        </server>
        <cpu>
                <used></used>
        </cpu>
        <ram>
            <total></total>
            <used></used>
        </ram>
        <disks>
            <disk>
                <mnt></mnt>
                <total></total>
                <used></used>
            </disk>
        <disks>
        <swap>
            <total></total>
            <used></used>
        </swap>
        <users>
            <user>
                <name></name>
                <uid></uid>
                <gid></gid>
                <isroot></isroot>
                <gname></gname>
                <login_time></login_time>
            </user>
        </users>
        <processes>
                <count></count>
                <zombies></zombies>
            <greedy>
                <process>
                    <pid></pid>
                    <cpu></cpu>
                    <ram></ram>
                    <command></command>
                </process>
            </greedy>
        </processes>
    </data>
'''


#############################################################################
#    Sonde. Classe principale du module.                                    #
#############################################################################


class Sonde:
    def __init__(self):
        print "Sonde";



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Sonde()

if __name__=='__main__':
    main()

