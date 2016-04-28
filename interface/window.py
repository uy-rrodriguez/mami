#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Window     :                                                           #
#        Implémente une fenêtre de basique.                                 #
#                                                                           #
#############################################################################

import curses
import sys


#############################################################################
#    Window.                                                                #
#############################################################################

Y = 0
X = 1
COLOR_SELECTED = 1
COLOR_NOSELECTED = 0
COLOR_TITLE = 2
COLOR_TABLE = 3

class Window(object):
    boxV = 0
    boxH = 0

    def __init__(self, interface, parent, height, width, y, x):
        self.interface = interface
        self.parent = parent
        self.screen = parent.subwin(height, width, y, x)
        #self.screen.scrollok(True)
        #self.screen.idlok(True)
        self.topleft = (y, x)
        self.dims = (height, width)
        self.posy, self.posx = 0, 0
        self.miny, self.minx = 1, 2
        self.hasFocus = False

        # Initializing colors
        curses.init_pair(COLOR_SELECTED, curses.COLOR_WHITE, curses.COLOR_BLUE);
        curses.init_pair(COLOR_NOSELECTED, curses.COLOR_WHITE, -1);
        curses.init_pair(COLOR_TITLE, curses.COLOR_CYAN, -1);
        curses.init_pair(COLOR_TABLE, curses.COLOR_BLACK, curses.COLOR_WHITE);

    def handle_key(self, key):
        pass
        """
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            self.changeMenu = True
        """

    def update(self):
        pass

    def render(self):
        pass

    def unfocus(self):
        self.hasFocus = False

    def focus(self):
        self.hasFocus = True

    def clear(self):
        self.screen.erase()
        self.screen.box(self.boxV, self.boxH)
        self.move(self.miny, self.minx)

    def move(self, y, x):
        try:
            self.screen.move(y, x)
            self.posy = y
            self.posx = x
        except:
            pass

    def _print(self, text="", color=None, pos=None):
        if type(text) is unicode:
            text = bytes(text.encode('utf-8'))
        elif not type(text) is str:
            text = str(text)
        try:
            if color == None:
                if pos == None:
                    self.screen.addstr(text)
                else:
                    self.screen.addstr(pos[Y], pos[X], text)
            else:
                if pos == None:
                    self.screen.addstr(text, curses.color_pair(color))
                else:
                    self.screen.addstr(pos[Y], pos[X], text, curses.color_pair(color))
        except curses.error:
            #sys.error.println("ERRROR")
            #sys.error.println(curses.error)
            pass

    def println(self, text="", color=None):
        self._print(text, color)
        self.move(self.posy+1, self.minx)

    def print_long(self, longText):
        maxlen = self.dims[1] - 2*self.minx
        lines = longText.split("\n")
        for line in lines:
            buff = line.strip()
            while len(buff) > 0:
                # Je verifie si je coupe un mot. Dans ce cas, j'extrait jusqu'a avant du dernier espace.
                toPrint = buff[:maxlen]
                if (len(toPrint) == maxlen) and (buff[maxlen:maxlen+1] not in ("", " ", ".", ",", ";")):
                    posSpace = toPrint.rfind(" ")
                    toPrint = toPrint[:posSpace]

                self.println(toPrint)
                buff = buff[len(toPrint)+1:]

    def read_str(self, text):
        self.screen.addstr(text)
        s = self.screen.getstr()
        return s
