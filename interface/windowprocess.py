#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowProcess :                                                        #
#        Implémente la fenêtre avec les processus greedy.                   #
#                                                                           #
#############################################################################

import curses
import time

#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import util
from objets.arraydataobject import ArrayDataObject
from window import *


#############################################################################
#    WindowProcess                                                          #
#############################################################################

TAB = "\t\t"
UPDATE_INTERVAL = 30 # sec

class WindowProcess(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowProcess, self).__init__(parent, stdscr, height, width, y, x)

        self.server = None
        self.greedies = []

        self.lastUpdate = None

        # Connexion BD
        self.db = dataBaseInstance


    # Quand on recoit un message de l'interafce en disant que l'tuilisateur à changé
    # de serveur, il faut aller chercher les données et les afficher.
    def change_server(self, server):
        self.server = server
        self.update_data()


    # Fonction qui cherche dans la BDD les données associées au serveur sélecctionné
    def update_data(self):
        self.greedies = []
        req = self.db.get_by_fields("process",
                                    ["server_name"],
                                    [self.server.name])

        res = req.fetchone()
        if req != None:
            xml = res["greedy_list"]
            greediesList = ArrayDataObject.parse_list_xml(xml, ".", ["pid", "cpu", "ram", "command"])
            for g in greediesList:
                self.greedies.append({"pid": g.pid,
                                      "command": g.command,
                                      "cpu": float(g.cpu),
                                      "ram": float(g.ram)})

        self.lastUpdate = time.time()


    def handle_key(self, key):
        pass


    # Cette fonction est appelé à chaque boucle de l'application principale.
    # On va contrôler le temps qui est passé entre la dernière fois qu'on est
    # allé chercher les données dans la BDD. Si ce temps est supérieur au temps
    # de mise à jour configuré, on lit les données.
    def update(self):
        if self.server != None and (time.time() - self.lastUpdate >= UPDATE_INTERVAL):
            self.update_data()
            self.lastUpdate = time.time()

            #for p in self.greedies:
            #    p["cpu"] += 1.0001
            #    p["ram"] += 2.0005


    # Affichage des données
    def render(self):
        width = self.dims[self.X] - 2*self.minx
        frmt = "{:" + str(width) + "s}"

        self.clear()
        self.println(frmt.format("Liste de processus greedy"), self.COLOR_TITLE)
        self.println();

        listPosX = []
        self._print("pid" + TAB, self.COLOR_TITLE);             listPosX.append(self.screen.getyx()[self.X])
        self._print("command" + TAB + TAB, self.COLOR_TITLE);   listPosX.append(self.screen.getyx()[self.X])
        self._print("CPU %" + TAB, self.COLOR_TITLE);           listPosX.append(self.screen.getyx()[self.X])
        self.println("RAM" + TAB, self.COLOR_TITLE);

        for x in range(width):
            self.screen.addch(curses.ACS_HLINE, curses.color_pair(self.COLOR_TITLE))
        self.println()

        i = 0
        for p in self.greedies:
            self._print(p["pid"]);                      self.move(self.posy, listPosX[i]); i+=1;
            self._print(p["command"]);                  self.move(self.posy, listPosX[i]); i+=1;
            self._print("{:.1f}".format(p["cpu"]));     self.move(self.posy, listPosX[i]); i=0;
            self._print(util.stringify_bytes(p["ram"]));
            self.println()

            if self.posy > self.screen.getmaxyx()[self.Y]:
                break
