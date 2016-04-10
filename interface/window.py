#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Window     :                                                           #
#        Implémente une fenêtre de basique.                                 #
#                                                                           #
#############################################################################

import curses


#############################################################################
#    Window.                                                                #
#############################################################################

Y = 0
X = 1
COLOR_SELECTED = 1
COLOR_NOSELECTED = 0

class Window(object):
    def __init__(self, parent, stdscr, height, width, x, y):
        self.parent = parent
        self.screen = stdscr.subwin(height, width, x, y)
        self.dims = self.screen.getmaxyx()
        self.posx = 0
        self.posy = 0
        self.minx = 2
        self.miny = 1
        self.hasFocus = False

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
        self.clear()
        self.println("WINDOW")
        self.screen.refresh()

    def unfocus(self):
        self.hasFocus = False

    def focus(self):
        self.hasFocus = True

    def move(self, y, x):
        if y > self.dims[Y]:
            y = self.dims[Y]-1
        if x > self.dims[X]:
            x = self.dims[X]-1
        self.screen.move(y, x)
        self.posy = y
        self.posx = x

    def clear(self):
        self.screen.erase()
        self.screen.box()
        self.move(self.miny, self.minx)

    def _print(self, text="", color=None):
        if color == None:
            self.screen.addstr(text)
        else:
            self.screen.addstr(text, color)

    def println(self, text="", color=None):
        self._print(text, color)
        # We calculate the next line according to the break lines in the text
        self.move(self.posy + 1, self.minx)

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
