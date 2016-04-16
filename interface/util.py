#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    util.py :                                                              #
#        Fichier contenant plusieurs fonctions utiles.                      #
#                                                                           #
#                                                                           #
#############################################################################

import math


'''
    Retourne un string representant le numero en bytes recu, avec B, KB, MB
    ou GB a la fin, dependant de la longeur du numero.
'''
def stringify_bytes(value):
    if value <= 1024:
        return "{:.2f}".format(value) + " B"
    elif value <= math.pow(1024,2):
        return "{:.2f}".format(value / 1024) + " KB"
    elif value <= math.pow(1024,3):
        return "{:.2f}".format(value / 1024 / 1024) + " MB"
    else:
        return "{:.2f}".format(round(value / 1024.0 / 1024.0 / 1024.0, 2)) + " GB"
