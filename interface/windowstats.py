#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowStats :                                                          #
#        Implémente la fenêtre avec les stats d'un serveur.                 #
#                                                                           #
#############################################################################

import curses

import util
from window import *


#############################################################################
#    WindowStats                                                            #
#############################################################################

class WindowStats(Window):
    def __init__(self, parent, stdscr, height, width, y, x):
        super(WindowStats, self).__init__(parent, stdscr, height, width, y, x)
        self.server = None
        self.cpu = None
        self.ram = None
        self.swap = None
        self.disks = None


    def change_server(self, statsData):
        self.server = statsData["server"]
        self.cpu = statsData["cpu"]
        self.ram = statsData["ram"]
        self.swap = statsData["swap"]
        self.disks = statsData["disks"]


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
        #super(WindowStats, self).update()
        if self.server != None:
            self.cpu.used = (self.cpu.used + 0.005) % 100
            self.ram.used = (self.ram.used + 50) % self.ram.total
            self.swap.used = (self.swap.used + 20) % self.swap.total
            self.disks[0].used = (self.disks[0].used + 10) % self.disks[0].total
            self.disks[1].used = (self.disks[1].used + 5) % self.disks[1].total

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
