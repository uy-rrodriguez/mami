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

import requests
import sys
#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from objets import cpu, disk, process, ram, server, swap, user, arraydataobject



#############################################################################
#    Constantes.                                                            #
#############################################################################


# Path et nom de base pour le fichier à générer, par rapport à l'addresse de
# ce fichier. Après le nom du fichier on ajoutera un suffix (genre, le nom
# du serveur et le timestamp) plus l'extension xml.
#DEFAULT_FILEPATH = "data/data_.xml"
URL = "http://localhost:5000"


#############################################################################
#    Sonde. Classe principale du module.                                    #
#############################################################################


class Requeteur(object):

    def __init__(self):
        pass

    def post_xml(self, file):
        requests.post(URL + "/upload", files = {'data.xml': open(file, 'rb')})


#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    cmdargs = (sys.argv)

    r = Requeteur()
    r.post_xml(cmdargs[1])


if __name__=='__main__':
    main()

