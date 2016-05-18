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

class Window(object):
    Y = 0
    X = 1
    COLOR_NOSELECTED = 0
    COLOR_SELECTED = 1
    COLOR_TITLE = 2
    COLOR_BORDER = 3
    COLOR_DEFAULT = 4

    #boxV = 0
    #boxH = 0

    def __init__(self, interface, parent, height, width, y, x):
        self.interface = interface
        self.parent = parent
        self.screen = parent.subwin(height, width, y, x)
        self.border = parent.subwin(height, width, y, x)

        #self.screen.scrollok(True)
        #self.screen.idlok(True)
        self.topleft = (y, x)
        self.dims = (height, width)
        self.posy, self.posx = 0, 0
        self.miny, self.minx = 1, 2
        self.hasFocus = False

        # Initializing colors
        curses.init_pair(self.COLOR_SELECTED, curses.COLOR_WHITE, curses.COLOR_BLUE);
        curses.init_pair(self.COLOR_NOSELECTED, curses.COLOR_WHITE, -1);
        curses.init_pair(self.COLOR_TITLE, curses.COLOR_CYAN, -1);
        curses.init_pair(self.COLOR_BORDER, curses.COLOR_BLUE, -1);

    def handle_key(self, key):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def unfocus(self):
        self.hasFocus = False
        self.border.bkgd(' ', curses.color_pair(self.COLOR_NOSELECTED))

    def focus(self):
        self.hasFocus = True
        self.border.bkgd(' ', curses.color_pair(self.COLOR_BORDER))

    def clear(self):
        self.screen.erase()
        self.border.border(0)
        #self.screen.box(self.boxV, self.boxH)
        self.move(self.miny, self.minx)

    def move(self, y, x):
        try:
            self.screen.move(y, x)
            self.posy = y
            self.posx = x
        except:
            pass

    def _print(self, ligne="", color=None, pos=None):
        # Conversion de chiffres à string, et traitement de strings en UTF8.
        text = ligne
        if type(text) is unicode:
            text = bytes(text.encode('utf-8'))
        elif not type(text) is str:
            text = str(text)

        # Curses ajoute un deuxième byte pour chaque caractère ASCII-extended.
        # Pour éviter des problèmes d'affichage, on ajoute un espace à la fin pour
        # chacun de ces caractères.
        #count = 0;
        #for i in range(len(ligne)):
        #    if ord(ligne[i]) > 128:
        #        count += 1
        #text += '' * count

        # Affichage du texte
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
