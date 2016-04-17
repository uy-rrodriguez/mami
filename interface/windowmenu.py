#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowMenu :                                                           #
#        Implémente le menu de l'interface.                                 #
#                                                                           #
#############################################################################

import curses
from window import *
from lxml import etree as ET


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

class Link():
    def __init__(self, label, action, attribs):
        self.label = label
        self.action = action
        self.attribs = attribs

    def execute(self):
        self.action(self.attribs)

class WindowMenu(Window):
    def __init__(self, parent, stdscr, height, width, y, x, pathDataScreen):
        super(WindowMenu, self).__init__(parent, stdscr, height, width, y, x)

        # Lecture du fichier
        f = open(pathDataScreen, "r")
        self.contents = f.read()
        self.root = ET.fromstring(self.contents)
        f.close()

        # Charge des valeurs initiales
        self.text = ""
        self.option = 0
        self.selected = 0
        self.links = [{LINK_ACTION: ACTION_MAIN, LINK_LABEL: "Main"}]
        self.changeMenu = False
        self.load_menu(WINDOW_MAIN)

    def set_servers(self, servers):
        self.servers = servers

    def load_menu(self, xPath):
        self.text = ""
        self.option = 0
        self.selected = 0
        self.links = []

        menu = self.root.find(xPath)
        for elem in list(menu):
            if elem.tag == ELEM_TEXT:
                self.text = elem.text

            elif elem.tag == ELEM_LINKS:
                for c in list(elem):
                    self.links.append(Link(c.text, self.action_change_menu, [c.tag]))

            elif elem.tag == ELEM_SERVERS:
                for s in self.servers:
                    self.links.append(Link(s.name, self.action_select_server, [s]))

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
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            #self.changeMenu = True
            self.links[self.selected].execute()

    def update(self):
        #super(WindowMenu, self).update()
        if self.changeMenu:
            self.changeMenu = False
            self.option = self.selected

            # Load new content
            action = self.links[self.option][LINK_ACTION]
            if action == ACTION_MAIN:
                xPath = WINDOW_MAIN
            elif action == ACTION_SERVER:
                self.interface.change_server(self.links[self.option][LINK_LABEL])
            else:
                xPath = BASE_WINDOWS + action

            if action != ACTION_SERVER:
                self.text = ""
                self.option = 0
                self.selected = 0
                self.links = []

                window = self.root.find(xPath)
                for elem in list(window):
                    if elem.tag == ELEM_TEXT:
                        self.text = elem.text

                    elif elem.tag == ELEM_LINKS:
                        children = list(elem)
                        for i in range(0, len(children)):
                            self.links.append({LINK_ACTION: children[i].tag,
                                               LINK_LABEL:  children[i].text})

                    elif elem.tag == ELEM_SERVERS:
                        for s in self.servers:
                            self.links.append({LINK_ACTION: ACTION_SERVER,
                                               LINK_LABEL:  s.name})

    def render(self):
        self.clear()
        self.print_long(self.text)
        self.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.hasFocus:
                self.println(self.links[i].label,
                             COLOR_SELECTED)
            else:
                self.println(self.links[i].label,
                             COLOR_NOSELECTED)

        self.println()
