#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    WindowProcess :                                                        #
#        Implémente la fenêtre avec les processus greedy.                   #
#                                                                           #
#############################################################################

import curses
import time

from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import util
from objets.arraydataobject import ArrayDataObject
from window import *


#############################################################################
#    WindowProcess                                                          #
#############################################################################

TAB = "\t\t"
UPDATE_INTERVAL = 2 # sec

class WindowProcess(Window):
    def __init__(self, parent, stdscr, height, width, y, x, dataBaseInstance):
        super(WindowProcess, self).__init__(parent, stdscr, height, width, y, x)
#         proc = {"pid": 125,
#                 "command": "firefox",
#                 "username": "ricardo",
#                 "cpu": 2,
#                 "ram": 250,
#                 "pram": 12}
        #self.greedies = [proc for i in range(0, 10)]

        self.server = None
        self.greedies = []

        self.lastUpdate = None

        # Connexion BD
        self.db = dataBaseInstance


    def change_server(self, server):
        self.server = server
        self.update_data()

    def update_data(self):
        #print >> sys.stderr, 'update_data'
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
        """
        if key == curses.KEY_DOWN and self.selected < len(self.links) - 1:
            self.selected += 1
        elif key == curses.KEY_UP and self.selected > 0:
            self.selected -= 1
        elif key == 10 and self.selected >= 0:
            self.changeMenu = True
        """

    def update(self):
        if self.server != None and (time.time() - self.lastUpdate >= UPDATE_INTERVAL):
            #self.update_data()
            self.lastUpdate = time.time()

            for p in self.greedies:
                p["cpu"] += 1.0001
                p["ram"] += 2.0005

    def render(self):
        width = self.dims[X] - 2*self.minx
        frmt = "{:" + str(width) + "s}"

        self.clear()
        self.println(frmt.format("Liste de processus greedy"), COLOR_TITLE)
        self.println();

        listPosX = []
        self._print("pid" + TAB, COLOR_TITLE);             listPosX.append(self.screen.getyx()[X])
        self._print("command" + TAB + TAB, COLOR_TITLE);   listPosX.append(self.screen.getyx()[X])
        #self._print("username" + TAB, COLOR_TITLE);        listPosX.append(self.screen.getyx()[X])
        self._print("CPU %" + TAB, COLOR_TITLE);             listPosX.append(self.screen.getyx()[X])
        self.println("RAM" + TAB, COLOR_TITLE);            #listPosX.append(self.screen.getyx()[X])
        #self.println("% RAM", COLOR_TITLE)

        for x in range(width):
            self.screen.addch(curses.ACS_HLINE, curses.color_pair(COLOR_TITLE))
        self.println()

        i = 0
        for p in self.greedies:
            self._print(p["pid"]);          self.move(self.posy, listPosX[i]); i+=1;
            self._print(p["command"]);      self.move(self.posy, listPosX[i]); i+=1;
            #self._print(p["username"]);     self.move(self.posy, listPosX[i]); i+=1;
            self._print("{:.1f}".format(p["cpu"]));     self.move(self.posy, listPosX[i]); i=0;
            self._print(util.stringify_bytes(p["ram"]));     #self.move(self.posy, listPosX[i]); i=0;
            #self._print(str(p["pram"]))
            self.println()
            if self.posy > self.screen.getmaxyx()[Y]:
                break
