#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Interface :                                                            #
#        Cette classe implémente une interface de visualisation en ligne    #
#        de commande, qui affichera pour chaque serveur le dernier état     #
#        connu, un graphe d’évolution pour les données aillant un           #
#        historique, ainsi que la date depuis la dernière communication.    #
#        Ce package intègre aussi des éléments de contrôle lui permettant   #
#        de détecter une situation de crise et de prévenir l’administrateur #
#        par e-mail.                                                        #
#                                                                           #
#############################################################################


#############################################################################
#    Interface. Classe principale du module.                                #
#############################################################################


class Interface:
    def __init__(self):
        print "Interface";



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Interface()

if __name__=='__main__':
    main()

