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
#    Stockage. Classe principale du module.                                 #
#############################################################################


class Stockage:
    def __init__(self):
        print "Stockage";



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Stockage()

if __name__=='__main__':
    main()

