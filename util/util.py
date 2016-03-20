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
        return str(value) + " B"
    elif value <= math.pow(1024,2):
        return str(value / 1024) + " KB"
    elif value <= math.pow(1024,3):
        return str(value / 1024 / 1024) + " MB"
    else:
        return str(round(value / 1024.0 / 1024.0 / 1024.0, 2)) + " GB"
