#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowMenu :                                                           #
#        Implémente le menu principal de l'interface.                       #
#        Pour gérer les différentes actions qui peuvent être exécutés       #
#        dans cette fenêtre, on implémente le modèle de programmation       #
#        State. De cette manière on gère les différentes situations de      #
#        simple. Par exemple, on aura un état pour parcourir les menus,     #
#        un autre pour afficher les serveurs, ou pour la configuration.     #
#                                                                           #
#############################################################################

import curses
from lxml import etree as ET

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from objets.arraydataobject import ArrayDataObject
from window import *


#############################################################################
#    BaseState. Classe de base pour tous les états.                         #
#############################################################################

# Abstraite
import abc
class BaseState():
    __metaclass__ = abc.ABCMeta
    inst = None

    def __init__(self, context):
        self.context = context

        # Lecture du fichier avec les titres et descriptifs des menus
        f = open("interface.xml", "r")
        self.contents = f.read()
        self.root = ET.fromstring(self.contents)
        f.close()

    def change_to(self):
        self.context.state = self

    @classmethod
    def instance(cls, context):
        if cls.inst == None:
            cls.inst = cls(context)
        return cls.inst

    @abc.abstractmethod
    def handle_key(self, key):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass


#############################################################################
#    BaseMenuState. Classe de base pour les états qui ont des menus.        #
#############################################################################

class Link():
    def __init__(self, name, label):
        self.name = name
        self.label = label

class BaseMenuState(BaseState):
    def __init__(self, context):
        super(BaseMenuState, self).__init__(context)
        self.title = ""
        self.text = ""
        self.links = []
        self.selected = 0

        # Premier menu
        self.load_menu("main")

    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10:
            win_name = self.links[self.selected].name

            # Changement d'état
            if win_name == "win_servers":
                ServersState.instance(self.context).change_to()
            elif win_name == "win_crises_params":
                ConfigCrisisState.instance(self.context).change_to()
            elif win_name == "win_emails_addr":
                ConfigEmailAddrState.instance(self.context).change_to()
            elif win_name == "win_emails_temp":
                ConfigEmailTempState.instance(self.context).change_to()
            elif win_name == "win_emails_test":
                ConfigEmailTestState.instance(self.context).change_to()
            else:
                self.load_menu(win_name)

    def update(self):
        pass

    def render(self):
        self.context.println(self.title)
        self.context.println("-------------------------------------")
        self.context.print_long(self.text)
        self.context.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.context.hasFocus:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_SELECTED)
            else:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_NOSELECTED)

        self.context.println()

    def load_menu(self, win):
        if win != "main":
            win = "windows/" + win

        self.links = []
        self.selected = 0

        data = self.root.find(win)
        self.title = data.find("title").text
        self.text = data.find("text").text
        for c in list(data.find("links")):
            self.links.append(Link(c.tag, c.text))


#############################################################################
#    ServersState. État pour gérer la liste de serveurs.                    #
#############################################################################

class ServersState(BaseState):
    def __init__(self, context):
        super(ServersState, self).__init__(context)
        self.title = self.root.find("./windows/win_servers/title").text
        self.text = self.root.find("./windows/win_servers/text").text
        self.servers = []
        self.links = []
        self.selected = 0

    def change_to(self):
        super(ServersState, self).change_to()

        # Chargement des serveurs (lecture de la BD)
        self.servers = []
        self.links = []
        for elem in self.context.db.get_all("server"):
            s = ArrayDataObject()
            s.name = elem["name"]
            s.ip = elem["ip"]
            s.uptime = elem["uptime"]
            self.servers.append(s)
            self.links.append(Link(s.name, s.name))

        # Option pour aller en arrière
        self.links.append(Link("back", "Retour"))

    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10:
            # Changement d'état
            if self.links[self.selected].name == "back":
                BaseMenuState.instance(self.context).change_to()
            else:
                self.context.select_server(self.servers[self.selected])

    def update(self):
        pass

    def render(self):
        self.context.println(self.title)
        self.context.println("-------------------------------------")
        self.context.print_long(self.text)
        self.context.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.context.hasFocus:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_SELECTED)
            else:
                self.context.println(self.links[i].label,
                                     self.context.COLOR_NOSELECTED)

        self.context.println()


#############################################################################
#    WindowMenu.                                                            #
#############################################################################

class WindowMenu(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowMenu, self).__init__(parent, stdscr, height, width, y, x)
        self.db = dataBaseInstance
        self.state = BaseMenuState.instance(self)

    def set_servers(self, servers):
        self.servers = servers

    def action_change_menu(self, attribs):
        if attribs[0] == ACTION_MAIN:
            self.load_menu(WINDOW_MAIN)
        else:
            self.load_menu(BASE_WINDOWS + attribs[0])

    def select_server(self, server):
        self.interface.change_server(server)


    def handle_key(self, key):
        if not self.hasFocus:
            return
        self.state.handle_key(key)

    def update(self):
        self.state.update()

    def render(self):
        self.clear()
        self.state.render()
