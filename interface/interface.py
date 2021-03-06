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
import os
import random

#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from objets.arraydataobject import ArrayDataObject
from dbaccess import DBAccess
from windowmenu import WindowMenu
from windowstats import WindowStats
from windowprocess import WindowProcess


#############################################################################
#    Interface. Classe principale du module.                                #
#############################################################################

Y = 0
X = 1
MIN_HEIGHT = 20
MIN_HEIGHT_PROCS = 15
HEIGHT_FOOT = 1
MIN_WIDTH = 120
KEY_CHANGE_WIN = 9    # TAB


class Interface:


# ================================  CONSTRUCTEURS ET DESTRUCTEURS  ================================ #

    def __init__(self):
        # Initialisation de curses
        self.init_curse()

        # Connexion a la BD
        self.db = DBAccess()

        # Initialisation des fenetres
        dims = self.stdscr.getmaxyx()
        dims = (max(dims[Y], MIN_HEIGHT), max(dims[X], MIN_WIDTH))
        h = dims[Y]/2
        w = dims[X]/2
        hProcs = max(MIN_HEIGHT_PROCS, h)
        self.pad = curses.newpad(h + hProcs, w*2)

        self.menu = WindowMenu(self, self.pad, h, w, 0, 0, self.db)
        self.stats = WindowStats(self, self.pad, h, w, 0, w, self.db)
        self.procs = WindowProcess(self, self.pad, hProcs - HEIGHT_FOOT, w*2, h, 0, self.db)
        self.windows = [self.menu, self.stats, self.procs]
        self.focus_windows = [self.menu, self.stats]

        # Focus de la fenetre principale
        self.focused = 0

        # Initialisation du menu
        self.menu.focus()


    def end(self):
        self.end_curse()

    def init_curse(self):
        os.environ.setdefault('ESCDELAY', '25')  # Reducing delay for ESCAPE key
        self.stdscr = curses.initscr()     # Init curses
        self.stdscr.keypad(1)              # Enable keypad mode (handle keys with curses.KEY_LEFT, etc).
        self.stdscr.nodelay(True)
        curses.start_color()               # Enable colors
        curses.use_default_colors()
        curses.noecho()                    # Disable echoing keys
        curses.cbreak()                    # React to keys instantly, without waiting for Enter
        curses.curs_set(0)                 # Disable cursor

    def end_curse(self):
        self.stdscr.keypad(0);
        curses.echo()
        curses.nocbreak();
        curses.curs_set(1)
        curses.endwin()                    # Restore the terminal to its original operating mode


# =================================== COMMUNICATION ENTRE FENETRES ================================ #

    def change_server(self, server):
        self.stats.change_server(server)
        self.procs.change_server(server)


# =======================================  BOUCLE PRINCIPALE  ===================================== #

    def handle_keys(self):
        k = self.stdscr.getch()

        # After reading one character, we discard the rest of the line
        try: self.stdscr.getstr()
        except: pass

        if k == curses.KEY_F12:
            return False

        elif k == KEY_CHANGE_WIN:
            self.focus_windows[self.focused].unfocus()
            self.focused = (self.focused + 1) % len(self.focus_windows)
            self.focus_windows[self.focused].focus()
        elif k >= 0:
            self.focus_windows[self.focused].handle_key(k)

        return True

    def update(self):
        for w in self.windows:
            w.update()

    def render(self):
        for w in self.windows:
            w.render()

        # Get max dimensions
        dims = self.stdscr.getmaxyx()

        # Render the foot, with info about the command keys
        self.stdscr.addstr(dims[Y]-1, 0,
            "[Tab] Changer de fenêtre \t [Entrer] Accepter \t [Esc] Retourner \t [F12] Sortir")

        # Refresh screen
        self.pad.noutrefresh(0, 0, 0, 0, dims[Y]-1, dims[X]-1)
        #curses.doupdate()

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

