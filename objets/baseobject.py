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

    def parseObjetXML(self, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        child = root.find(path)
        for att in attribs:
            setattr(self, att, child.find(att).text)


    def writeObjetXML(self, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        child = root.find(path)
        for att in attribs:
            child.find(att).text = getattr(self, att)
        return ET.tostring(root)


    @staticmethod
    def parseListXML(baseClass, stringXML, path, attribs):
        result = []
        root = ET.fromstring(stringXML)
        rootList = root.find(path)
        for child in rootList:
            obj = baseClass()
            result.append(obj)
            for att in attribs:
                setattr(obj, att, child.find(att).text)
        return result


    @staticmethod
    def writeListXML(listObj, stringXML, path, attribs):
        root = ET.fromstring(stringXML)
        rootList = root.find(path)
        rootList.clear()

        for obj in listObj:
            child = ET.SubElement(rootList, obj.__class__.__name__.lower())
            for att in attribs:
                subelement = ET.SubElement(child, att)
                subelement.text = getattr(obj, att)

        indent(root)
        return ET.tostring(root)


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








