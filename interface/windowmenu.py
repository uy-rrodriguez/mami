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

ELEM_TEXT = "text"
ELEM_LINKS = "links"

LINK_ACTION = "action"
LINK_LABEL = "label"

class WindowMenu(Window):
    def __init__(self, parent, stdscr, height, width, x, y, pathDataScreen):
        super(WindowMenu, self).__init__(parent, stdscr, height, width, x, y)

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
        self.changeMenu = True


    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            self.changeMenu = True

    def update(self):
        if self.changeMenu:
            self.changeMenu = False
            self.option = self.selected

            # Load new content
            action = self.links[self.option][LINK_ACTION]
            if action == ACTION_MAIN:
                xPath = WINDOW_MAIN
            else:
                xPath = BASE_WINDOWS + action

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
                                           LINK_LABEL:  "(" + str(i+1) + ") " + children[i].text})

    def render(self):
        self.clear()
        self.print_long(self.text)
        self.println()

        # Render options
        for i in range(0, len(self.links)):
            if i == self.selected and self.hasFocus:
                self.println(self.links[i][LINK_LABEL], curses.color_pair(curses.color_pair(COLOR_SELECTED)))
            else:
                self.println(self.links[i][LINK_LABEL], curses.color_pair(curses.color_pair(COLOR_NOSELECTED)))

        self.println()
        self.screen.refresh()
