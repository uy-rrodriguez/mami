#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowStats :                                                          #
#        Implémente la fenêtre avec les stats d'un serveur.                 #
#                                                                           #
#############################################################################

import curses
import time

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import util
from objets.arraydataobject import ArrayDataObject
from graphs import *
from window import *


#############################################################################
#    WindowStats                                                            #
#############################################################################

UPDATE_INTERVAL = 2 # sec

class WindowStats(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowStats, self).__init__(parent, stdscr, height, width, y, x)
        self.server = None
        self.cpu = None
        self.ram = None
        self.swap = None
        self.disks = None
        self.db = dataBaseInstance
        self.lastUpdate = None

        # Gestion des boutons de la fenetre
        self.selected = 0
        self.options = ["CPU", "RAM", "Swap", "Disques"]

        # Gestion de graphiques
        self.graphs = grephs.Graphs()


    def change_server(self, server):
        self.server = server
        self.update_data()

    def update_data(self):
        last = self.db.get_last_date(self.server.name).next()[0]
        res = self.db.get_by_fields("stat", ["server_name", "date"], [self.server.name, last]).next()
        resDisks = self.db.get_by_fields("statDisk", ["server_name", "date"], [self.server.name, last])

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
        if key == curses.KEY_RIGHT and self.selected < len(self.options) - 1:
            self.selected += 1
        elif key == curses.KEY_LEFT and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            pass #self.changeMenu = True

    def update(self):
        if self.server != None and (time.time() - self.lastUpdate >= UPDATE_INTERVAL):
            #self.update_data()

            self.lastUpdate = time.time()

            self.cpu.used = (self.cpu.used + 0.005) % 100
            self.ram.used = (self.ram.used + 50) % self.ram.total
            self.swap.used = (self.swap.used + 20) % self.swap.total
            self.disks[0].used = (self.disks[0].used + 10) % self.disks[0].total
            self.disks[1].used = (self.disks[1].used + 5) % self.disks[1].total


    def render_options(self):
        y = self.dims[Y] - 2
        self.move(y, self.minx)
        self._print("Historiques : ")
        for i in range(0, len(self.options)):
            if i == self.selected and self.hasFocus:
                self._print(" " + self.options[i] + " ", color=COLOR_SELECTED)
            else:
                self._print(" " + self.options[i] + " ", color=COLOR_NOSELECTED)
        self.println()

    def render(self):
        self.clear()
        if self.server != None:
            self.println(self.server.name + "\t\t" + self.server.ip + "\t\t uptime: " + self.server.uptime)
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
