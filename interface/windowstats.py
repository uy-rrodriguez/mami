#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowStats :                                                          #
#        Implémente la fenêtre avec les stats d'un serveur.                 #
#                                                                           #
#############################################################################

import curses
from window import *


#############################################################################
#    WindowStats                                                            #
#############################################################################

class WindowStats(Window):
    def __init__(self, parent, stdscr, height, width, x, y):
        super(WindowStats, self).__init__(parent, stdscr, height, width, x, y)
        self.server = {"name":"server-01254-m", "ip":"192.168.5.1", "uptime":"5d 3h 12m"}
        self.cpu = 0.5
        self.ram = (15000.0, 1500.0)
        self.swap = (1200.0, 200.0)
        self.disks = [{"mount":"/sda1", "total":50000.0, "used":2000.0},
                      {"mount":"/sda2", "total":20000.0, "used":5000.0}]

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
        self.cpu = (self.cpu + 0.00005) % 1
        self.ram = (self.ram[0], (self.ram[1] + 0.5) % self.ram[0])
        self.swap = (self.swap[0], (self.swap[1] + 0.02) % self.swap[0])
        self.disks[0]["used"] = (self.disks[0]["used"] + 10) % self.disks[0]["total"]
        self.disks[1]["used"] = (self.disks[1]["used"] + 5) % self.disks[1]["total"]

    def render(self):
        self.clear()
        self.println(self.server["name"] + "    " + self.server["ip"] + "    uptime: " + self.server["uptime"])
        self.println("CPU: " + "{:.1%}".format(self.cpu))
        self.println("RAM: total " + str(self.ram[0]) + ", used " + "{:.1%}".format(self.ram[1] / self.ram[0]))
        self.println("Swap: total " + str(self.swap[0]) + ", used " + "{:.1%}".format(self.swap[1] / self.swap[0]))
        self.println()

        self.println("Disks:")
        for d in self.disks:
            self._print(d["mount"] + " => ")
            self._print("total " + str(d["total"]))
            self._print(", used " + "{:.1%}".format(d["used"] / d["total"]))
            self.println()

        self.screen.refresh()
