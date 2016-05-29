#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowStats :                                                          #
#        Implémente la fenêtre avec les stats d'un serveur.                 #
#                                                                           #
#############################################################################

import curses
import time

#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import util
from objets.arraydataobject import ArrayDataObject
from graphs import Graphs
from window import *
from mail import *


#############################################################################
#    WindowStats                                                            #
#############################################################################

UPDATE_INTERVAL = 30 # sec
OPTION_LABEL = 0
OPTION_ACTION = 1

class WindowStats(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowStats, self).__init__(parent, stdscr, height, width, y, x)
        self.server = None
        self.cpu = None
        self.ram = None
        self.swap = None
        self.disks = None
        self.lastDate = None

        self.lastUpdate = None

        # Connexion BD
        self.db = dataBaseInstance

        # Gestion de graphiques
        self.graphs = Graphs(self.db)

        # Gestion des boutons de la fenetre
        self.selected = 0
        self.options = [("Evolution CPU et RAM", self.graphs.render_cpu_ram_chart),
                        ("Evolution disques", self.graphs.render_disks_use_chart),
                        ("Processus et utilisateurs", self.graphs.render_users_process_chart)]


    # Quand on recoit un message de l'interafce en disant que l'tuilisateur à changé
    # de serveur, il faut aller chercher les données et les afficher.
    def change_server(self, server):
        self.server = server
        self.update_data()

    # Fonction qui cherche dans la BDD les données associées au serveur sélecctionné
    def update_data(self):
        self.lastDate = self.db.get_last_date(self.server.name).next()[0]
        res = self.db.get_by_fields("stat",
                                    ["server_name", "date"],
                                    [self.server.name, self.lastDate]).next()

        resDisks = self.db.get_by_fields("statDisk",
                                         ["server_name", "date"],
                                         [self.server.name, self.lastDate])

        self.cpu = ArrayDataObject();
        self.cpu.used = float(res["cpu_used"])
        self.ram = ArrayDataObject();
        self.ram.total = int(res["ram_total"]);
        self.ram.used = float(res["ram_used"])
        self.swap = ArrayDataObject();
        self.swap.total = int(res["swap_total"]);
        self.swap.used = float(res["swap_used"])

        self.disks = []
        for line in resDisks:
            d = ArrayDataObject()
            d.mnt = line["mnt"]
            d.total = int(line["total"])
            d.used = float(line["used"])
            self.disks.append(d)

        self.lastUpdate = time.time()


    def handle_key(self, key):
        if key == curses.KEY_DOWN and self.selected < len(self.options) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            # On exécute l'action de l'option sélectionnée
            self.options[self.selected][OPTION_ACTION](self.server.name)

    # Cette fonction est appelé à chaque boucle de l'application principale.
    # On va contrôler le temps qui est passé entre la dernière fois qu'on est
    # allé chercher les données dans la BDD. Si ce temps est supérieur au temps
    # de mise à jour configuré, on lit les données.
    def update(self):
        if self.server != None and (time.time() - self.lastUpdate >= UPDATE_INTERVAL):
            self.update_data()

            self.lastUpdate = time.time()

            #self.cpu.used = (self.cpu.used + 0.005) % 100
            #self.ram.used = (self.ram.used + 50) % self.ram.total
            #self.swap.used = (self.swap.used + 20) % self.swap.total
            #self.disks[0].used = (self.disks[0].used + 10) % self.disks[0].total
            #self.disks[1].used = (self.disks[1].used + 5) % self.disks[1].total


    # Affichage des options pour créer des graphes
    def render_options(self):
        title = "Graphiques  "
        y = self.dims[self.Y] - len(self.options) - 1
        x = self.minx + len(title)
        self.move(y, self.minx)
        self._print(title)

        for i in range(0, len(self.options)):
            self.move(y+i, x)
            color = self.COLOR_NOSELECTED
            if i == self.selected and self.hasFocus:
                color = self.COLOR_SELECTED
            self.println("{:30s}".format("[ " + self.options[i][OPTION_LABEL]) + " ]", color)


    # Affichage des données
    def render(self):
        self.clear()
        if self.server != None:
            self.println(self.server.name + "  (" + self.server.ip + ")\t Uptime: " + self.server.uptime)
            self.println("Derniere date: " + self.lastDate)
            self.println()
            self.println("CPU: " + "{:.1f}".format(self.cpu.used) + "%")
            self._print("RAM: total " + util.stringify_bytes(self.ram.total))
            self.println("\t\t utilise " + "{:.1%}".format(self.ram.used / self.ram.total))
            self._print("Swap: total " + util.stringify_bytes(self.swap.total))
            self.println("\t\t utilise " + "{:.1%}".format(self.swap.used / self.swap.total))
            self.println()

            self.println("Disks:")
            for d in self.disks:
                self._print(d.mnt + " => ")
                self._print("total " + util.stringify_bytes(d.total))
                self._print("\t utilise " + "{:.1%}".format(d.used / d.total))
                self.println()

            self.render_options()
