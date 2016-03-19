#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Disk :                                                                 #
#        Classe contenant l'information d'une partition.                    #
#                                                                           #
#                                                                           #
#############################################################################

from arraydataobject import *


class Disk(ArrayDataObject):

    def __init__(self):
        super(Disk, self).__init__()
