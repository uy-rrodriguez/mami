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

from lxml import etree as ET


#############################################################################
#    BaseObject. Classe mère de tous les objets du système                  #
#############################################################################


class BaseObject(object):
    def __init__(self):
        pass

    def parse_objet_xml(self, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        child = root.find(path)
        for att in attribs:
            setattr(self, att, child.find(att).text)


    @classmethod
    def parse_list_xml(cls, stringXML, path, attribs):
        result = []
        root = ET.fromstring(stringXML)
        rootList = root.find(path)
        for child in rootList:
            obj = cls()
            result.append(obj)
            for att in attribs:
                setattr(obj, att, child.find(att).text)
        return result


    def write_objet_xml(self, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        child = find_or_create_element(root, path)
        for att in attribs:
            attributElement = find_or_create_element(child, att)
            attributElement.text = str(getattr(self, att))

        indent(root)
        return ET.tostring(root)


    @classmethod
    def write_list_xml(cls, listObj, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        rootList = find_or_create_element(root, path)
        rootList.clear()

        for obj in listObj:
            child = ET.SubElement(rootList, obj.__class__.__name__.lower())
            for att in attribs:
                subelement = ET.SubElement(child, att)
                subelement.text = str(getattr(obj, att))

        indent(root)
        return ET.tostring(root)



#############################################################################
#    Fonctions utiles pour modifier un texte XML.                           #
#############################################################################

'''
    Cree toute une branche a partir du chemin donne et retourne le dernier fils
'''
def find_or_create_element(root, path):
    child = None
    parent = root
    parts = path.split("/")
    for part in parts:
        child = parent.find(part)
        if child == None:
            child = ET.SubElement(parent, part)
        parent = child
    return child


def indent(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
