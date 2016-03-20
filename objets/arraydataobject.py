#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    BaseObject :                                                           #
#        Classe de laquelle héritent tous les objets du système.            #
#        Définit certains méthodes utiles un peu partout.                   #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################

from baseobject import *


class ArrayDataObject(BaseObject):
    data = {}

    def __init__(self):
        ArrayDataObject.data[id(self)] = {}

    def __getattr__(self, att):
        return ArrayDataObject.data[id(self)][att]

    def __setattr__(self, att, value):
        ArrayDataObject.data[id(self)][att] = value

    def __str__(self):
        return str(ArrayDataObject.data[id(self)])

    def __del__(self):
        del ArrayDataObject.data[id(self)]
