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

    def pickle_fix(self):
        #ArrayDataObject.data[id(self)] = {}
        pass

    def __getinitargs__(self):
        ArrayDataObject.data[id(self)] = {}
        return ()

    def __getstate__(self):
        return ArrayDataObject.data[id(self)]

    def __setstate__(self, state):
        ArrayDataObject.data[id(self)] = state

    def __getattr__(self, att):
        # Fixes pour utiliser pickle
        if att == "__setstate__":
            return self.__setstate__

        elif att == "__getstate__":
            return self.__getstate__

        elif att == "__getinitargs__":
            return self.__getinitargs__

        return ArrayDataObject.data[id(self)][att]

    def __setattr__(self, att, value):
        ArrayDataObject.data[id(self)][att] = value

    def __str__(self):
        return str(ArrayDataObject.data[id(self)])

    def __del__(self):
        del ArrayDataObject.data[id(self)]
