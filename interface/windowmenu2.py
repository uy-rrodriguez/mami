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
from window import *
from lxml import etree as ET


#############################################################################
#    BaseState et autres classes State concrètes.                           #
#############################################################################

# Abstraite
import abc
class BaseState():
    __metaclass__ = abc.ABCMeta
    instance = None

    def __init__(self, context):
        self.context = context

    @classmethod
    def instance(cls, context):
        instance = cls(context)

    @abc.abstractmethod
    def change_to(self):
        pass

    @abc.abstractmethod
    def handle_key(self, key):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass


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

         # Lecture du fichier
        f = open("interface.xml", "r")
        self.contents = f.read()
        self.root = ET.fromstring(self.contents)
        f.close()

        # First menu
        self.load_menu("main")

    def instance(self):
        if self.instance == None:
            self.instance = BaseMenuState()
        return self.instance

    def change_to(cls):
        pass

    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10:
            win_name = self.links[self.selected].name

            # Changement d'état
            if win_name == "servers":
                ServersState.instance().change_to()
            elif win_name == "win_crises_params":
                ConfigCrisisState.instance().change_to()
            elif win_name == "win_emails_addr":
                ConfigEmailAddrState.instance().change_to()
            elif win_name == "win_emails_temp":
                ConfigEmailTempState.instance().change_to()
            elif win_name == "win_emails_test":
                ConfigEmailTestState.instance().change_to()
            else:
                self.load_menu(win_name)

    def update(self):
        pass

    def render(self):
        self.println(self.title)
        self.println("-------------------------------------")
        self.print_long(self.text)
        self.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.context.hasFocus:
                self.println(self.links[i].label,
                             self.context.COLOR_SELECTED)
            else:
                self.println(self.links[i].label,
                             self.context.COLOR_NOSELECTED)

        self.println()

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
#    WindowMenu.                                                            #
#############################################################################

BASE_WINDOWS = "windows/"
WINDOW_MAIN = "main"

ACTION_MAIN = "main"
ACTION_EXIT = "exit"
ACTION_SERVER = "server"

ELEM_TEXT = "text"
ELEM_LINKS = "links"
ELEM_SERVERS = "servers"

LINK_ACTION = "action"
LINK_LABEL = "label"

class WindowMenu(Window):
    def __init__(self, parent, stdscr, height, width, y, x):
        super(WindowMenu, self).__init__(parent, stdscr, height, width, y, x)
        self.state = BaseMenuState.instance()

    def set_servers(self, servers):
        self.servers = servers

    def action_change_menu(self, attribs):
        if attribs[0] == ACTION_MAIN:
            self.load_menu(WINDOW_MAIN)
        else:
            self.load_menu(BASE_WINDOWS + attribs[0])

    def action_select_server(self, attribs):
        self.interface.change_server(attribs[0])


    def handle_key(self, key):
        if not self.hasFocus:
            return
        self.state.handle_key(key)

    def update(self):
        self.state.update()

    def render(self):
        self.clear()
        self.state.render()
