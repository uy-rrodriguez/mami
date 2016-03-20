#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Process :                                                              #
#        Classe contenant l'information d'un processus.                     #
#                                                                           #
#                                                                           #
#############################################################################

from arraydataobject import *


class Process(ArrayDataObject):

    def __init__(self):
        super(Process, self).__init__()

    def __cmp__(self, other):
        return (self.percent_ram + self.cpu) - (other.percent_ram + other.cpu)
