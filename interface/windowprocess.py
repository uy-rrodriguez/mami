#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowProcess :                                                        #
#        Implémente la fenêtre avec les processus greedy.                   #
#                                                                           #
#############################################################################

import curses
from window import *


#############################################################################
#    WindowProcess                                                          #
#############################################################################

TAB = "\t\t"

class WindowProcess(Window):
    def __init__(self, parent, stdscr, height, width, y, x):
        super(WindowProcess, self).__init__(parent, stdscr, height, width, y, x)
        proc = {"pid": 125,
                "command": "firefox",
                "username": "ricardo",
                "cpu": 2,
                "ram": 250,
                "pram": 12}

        self.greedies = [proc for i in range(0, 10)]


    def change_server(self, serverName):
        self.greedies[0]["pid"] = serverName


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
        for p in self.greedies:
            p["cpu"] += 0.0002
            p["ram"] += 0.0005

    def render(self):
        self.clear()
        self.println("Liste de processus greedy")

        listPosX = []
        self._print("pid" + TAB);         listPosX.append(self.screen.getyx()[X])
        self._print("command" + TAB);     listPosX.append(self.screen.getyx()[X])
        self._print("username" + TAB);    listPosX.append(self.screen.getyx()[X])
        self._print("CPU" + TAB);         listPosX.append(self.screen.getyx()[X])
        self._print("RAM" + TAB);         listPosX.append(self.screen.getyx()[X])
        self.println("% RAM")

        self.println("-" * (self.dims[X] - 2*self.minx))

        i = 0
        for p in self.greedies:
            self._print(p["pid"]);          self.move(self.posy, listPosX[i]); i+=1;
            self._print(p["command"]);      self.move(self.posy, listPosX[i]); i+=1;
            self._print(p["username"]);     self.move(self.posy, listPosX[i]); i+=1;
            self._print(str(p["cpu"]));     self.move(self.posy, listPosX[i]); i+=1;
            self._print(str(p["ram"]));     self.move(self.posy, listPosX[i]); i=0;
            self._print(str(p["pram"]))
            self.println()
            if self.posy > self.screen.getmaxyx()[Y]:
                break
