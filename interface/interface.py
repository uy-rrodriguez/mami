#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Interface :                                                            #
#        Cette classe implémente une interface de visualisation en ligne    #
#        de commande, qui affichera pour chaque serveur le dernier état     #
#        connu, un graphe d’évolution pour les données aillant un           #
#        historique, ainsi que la date depuis la dernière communication.    #
#        Ce package intègre aussi des éléments de contrôle lui permettant   #
#        de détecter une situation de crise et de prévenir l’administrateur #
#        par e-mail.                                                        #
#                                                                           #
#############################################################################

import curses
from windowmenu import WindowMenu
from windowstats import WindowStats


#############################################################################
#    Interface. Classe principale du module.                                #
#############################################################################

Y = 0
X = 1
KEY_QUIT = ord("q")
KEY_CHANGE_WIN = 9    # TAB


class Interface:
    def __init__(self):
        self.init_curse()
        self.dims = self.stdscr.getmaxyx()
        h = self.dims[Y]/2
        w = self.dims[X]/2
        self.menu = WindowMenu(     self, self.stdscr, h-1, w-1, 0, 0, "interface.xml" )
        self.stats = WindowStats(   self, self.stdscr, h-1, w-1, 0, w )
        #self.procs = WindowProcess( self.stdscr, h-1, w-1, h, w )
        #self.windows = [self.menu, self.stats, self.procs]
        self.windows = [self.menu, self.stats]
        self.focused = 0
        self.menu.focus()

    def end(self):
        self.end_curse()

    def init_curse(self):
        self.stdscr = curses.initscr()     # Init curses
        self.stdscr.keypad(1)              # Enable keypad mode (handle keys with curses.KEY_LEFT, etc).
        self.stdscr.nodelay(True)
        curses.start_color()               # Enable colors
        curses.noecho()                    # Disable echoing keys
        curses.cbreak()                    # React to keys instantly, without waiting for Enter
        curses.curs_set(0)                 # Disable cursor

    def end_curse(self):
        self.stdscr.keypad(0);
        curses.echo()
        curses.nocbreak();
        curses.curs_set(1)
        curses.endwin()                    # Restore the terminal to its original operating mode

    def handle_keys(self):
        k = self.stdscr.getch()

        # After reading one character, we discard the rest of the line
        try: self.stdscr.getstr()
        except: pass

        if k == KEY_QUIT:
            return False

        elif k == KEY_CHANGE_WIN:
            self.windows[self.focused].unfocus()
            self.focused = (self.focused + 1) % len(self.windows)
            self.windows[self.focused].focus()
        else:
            self.windows[self.focused].handle_key(k)

        return True

    def update(self):
        for w in self.windows:
            w.update()

    def render(self):
        for w in self.windows:
            w.render()

    def run(self):
        try:
            while True:
                self.update()
                self.render()
                curses.napms(50)
                if not self.handle_keys():
                    break
        finally:
            self.end()



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    try:
        i = Interface()
        i.run()
    finally:
        curses.echo()
        curses.nocbreak();
        curses.curs_set(1)
        curses.endwin()

if __name__=='__main__':
    main()

