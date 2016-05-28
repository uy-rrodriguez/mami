#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Config :                                                               #
#        Classe pour gérer la configuration de l'application.               #
#                                                                           #
#############################################################################

from lxml import etree as ET


#############################################################################
#    Config.                                                                #
#############################################################################

class Config:
    PATH_CONFIG = "config.xml"

    def __init__(self):
        self.recharger()

    def recharger(self):
        f = open(self.PATH_CONFIG, "r")
        self.config_root = ET.fromstring(f.read())
        f.close()

    def save(self):
        self.indent_xml(self.config_root)
        content = '<?xml version="1.0" encoding="UTF-8"?>\n' \
                    + ET.tostring(self.config_root)
        f = open(self.PATH_CONFIG, "w")
        f.write(content)
        f.close()

    def indent_xml(self, elem, level=0):
        i = "\n" + level*"    "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "    "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent_xml(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def get(self, key):
        return self.config_root.find(key).text

    def set(self, key, value):
        self.config_root.find(key).text = value
