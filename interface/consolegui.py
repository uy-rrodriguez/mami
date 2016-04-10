#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    ConsoleGUI :                                                           #
#        Une classe pour créer des interfaces simples en console.           #
#        Permet la définition des élements affichés dans un fichier xml.    #
#        Ceci permet de séparer la logique d'affichage du contenu statique  #
#                                                                           #
#############################################################################

import curses
from time import sleep
from lxml import etree as ET


#############################################################################
#    ConsoleGUI.                                                            #
#############################################################################

SPACE = "\n"
LINE = "----------------------------------------------------\n"

BASE_WINDOWS = "windows/"
WINDOW_MAIN = "main"

ACTION_MAIN = "main"
ACTION_EXIT = "exit"

ELEM_TEXT = "text"
ELEM_LINKS = "links"

LINK_ACTION = "action"
LINK_LABEL = "label"

MENU_OPTION_COLOR = curses.COLOR_RED

class ConsoleGUI:
    def __init__(self, pathDataScreen):
        # Init screen
        self.init_curses()
        self.screen = self.stdscr
        #self.screen = self.stdscr.subwin(40, 100, 0, 0)
        self.dims = self.screen.getmaxyx()

        # Init local screen vars
        self.posx = self.posy = 0
        self.minx = 2
        self.miny = 1

        f = open(pathDataScreen, "r")
        self.contents = f.read()
        self.root = ET.fromstring(self.contents)
        f.close()

        # Charge des options initiales
        self.option = 0
        self.text = ""
        self.links = [{LINK_ACTION: ACTION_MAIN, LINK_LABEL: "Main"}]

        self.errors = ""

    def init_curses(self):
        # Init curses
        self.stdscr = curses.initscr()
        curses.start_color()
        # Disable echoing keys
        curses.noecho()
        # React to keys instantly, without waiting for Enter
        curses.cbreak()
        # Enable keypad mode, each special key (arrow, home) will be handled with curses.KEY_LEFT, etc.
        self.stdscr.keypad(1)
        # Disable cursor
        curses.curs_set(0)

    def exit_curses(self):
        curses.nocbreak();
        self.stdscr.keypad(0);
        curses.echo()
        curses.curs_set(1)
        # Restore the terminal to its original operating mode
        curses.endwin()

    def is_exit(self):
        return self.links[self.option][LINK_ACTION] == ACTION_EXIT

    def move(self, y, x):
        self.screen.move(y, x)
        self.posy = y
        self.posx = x

    def clear(self):
        self.screen.clear()
        self.screen.box()
        self.move(self.miny, self.minx)


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
                    #if posSpace > 0:
                    toPrint = toPrint[:posSpace]

                self.println(toPrint)
                #self.screen.refresh()
                #sleep(2)
                buff = buff[len(toPrint)+1:]


    def println(self, text="", color=None):
        if color == None:
            self.screen.addstr(text)
        else:
            self.screen.addstr(text, color)

        # We calculate the next line according to the break lines in the text
        self.move(self.posy + 1, self.minx)


    def read_str(self, text):
        # Refresh before pausing for input
        #self.screen.refresh()

        # Then, we wait for a string.
        self.screen.addstr(text)
        c = self.screen.getstr()
        return c


    def read_char(self):
        # We wait for a character.
        #self.screen.addstr(text)
        c = self.screen.getch()
        return c


    def read_option(self):
        self.option = None
        selected = 0
        lastSelected = 0
        yOptions = self.posy - len(self.links) - 1

        self.println("Selectionez une option...")

        while self.option == None:
                self.move(yOptions + selected, self.minx)
                self.println(self.links[selected][LINK_LABEL],
                             curses.color_pair(curses.color_pair(1)))
                self.screen.refresh()
            #try:
                #self.option = self.read_str("Selectionez une option : ")
                #self.option = int(self.option) - 1
                #assert(self.option < len(self.links))

                arrow = self.read_char()
                if arrow == curses.KEY_DOWN and selected < len(self.links) - 1:
                    selected += 1
                elif arrow == curses.KEY_UP and selected > 0:
                    selected -= 1
                elif arrow in (curses.KEY_ENTER, 10)  and selected >= 0:
                    #self.println(str(selected))
                    self.option = selected

                self.move(yOptions + lastSelected, self.minx)
                self.println(self.links[lastSelected][LINK_LABEL])

                lastSelected = selected

            #except ValueError:
            #    self.println()
            #    self.println("Not a number.")
            #except AssertionError:
            #    self.option = None
            #    self.println()
            #    self.println("Incorrect option.")


    def update(self):
        action = self.links[self.option][LINK_ACTION]
        if action == ACTION_MAIN:
            xPath = WINDOW_MAIN
        else:
            xPath = BASE_WINDOWS + action

        self.links = []
        self.option = 0
        self.text = ""
        self.errors = ""

        window = self.root.find(xPath)
        for elem in list(window):
            if elem.tag == ELEM_TEXT:
                self.text = elem.text
            elif elem.tag == ELEM_LINKS:
                children = list(elem)
                for i in range(0, len(children)):
                    self.links.append({LINK_ACTION: children[i].tag,
                                       LINK_LABEL:  "(" + str(i+1) + ") " + children[i].text})
            else:
                self.errors += "\nUnknown element '" + elem.tag + "'."

    def render(self):
        self.clear()
        self.print_long(self.text)
        self.println()
        for link in self.links:
            self.println(link[LINK_LABEL])

        self.println()

        #self.screen.addstr(str(self.screen.w))



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    gui = ConsoleGUI("interface.xml")
    try:
        while not gui.is_exit():
            gui.update()
            gui.render()
            gui.read_option()
        gui.exit_curses()

    finally:
        gui.exit_curses()


if __name__=='__main__':
    main()

