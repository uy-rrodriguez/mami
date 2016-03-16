#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Webservice :                                                           #
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
#    Webservice. Classe principale du module.                               #
#############################################################################


class Webservice:
    def __init__(self):
        print "Webservice";



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Webservice()

if __name__=='__main__':
    main()

