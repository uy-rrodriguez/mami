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

import sqlite3
import pygal
from datetime import datetime


#############################################################################
#    Interface. Classe principale du module.                                #
#############################################################################


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Interface:
    def __init__(self):
        self.fileName = "chart.svg"
        self.browser = True

        # Connexion BD
        self.conn = sqlite3.connect("../data/sonde_info.db")
        self.conn.row_factory = dict_factory
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT name, ip, uptime FROM server")
        servers = self.cursor.fetchall()

        for s in servers:
            print s["name"]
            #self.render_cpu_ram_chart(s["name"])
            #self.render_users_process_chart(s["name"])
            self.render_disks_use_chart(s["name"])
            #self.render_single_disk_chart(dates)

        dates = [
                datetime(2013, 1, 2, 12, 0),
                datetime(2013, 1, 12, 14, 30, 45),
                datetime(2013, 2, 2, 6),
                datetime(2013, 2, 22, 9, 45)
                ]


    def date_formatter(self, dt):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    def save_or_display_chart(self, chart):
        if (self.browser == True):
            chart.render_in_browser()
        else:
            chart.render_to_file(self.fileName)

    def render_time_chart(self, title, dates=[], linesInfo={}):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = title
        #chart.x_labels = map(self.date_formatter, dates)
        chart.x_labels = dates
        for label in linesInfo:
            chart.add(label, linesInfo[label])
        self.save_or_display_chart(chart)

    def render_cpu_ram_chart(self, server):
        self.cursor.execute("""SELECT date, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.cursor.fetchall()
        dates, cpu, ram, swap = [], [], [], []

        for line in info:
            dates.append(line["date"])
            cpu.append(line["cpu_used"])
            ram.append(line["ram_used"] * 100 / line["ram_total"])
            swap.append(line["swap_used"] * 100 / line["swap_total"])

        self.fileName = "cpu_ram.svg"
        self.render_time_chart("Utilisation de CPU, RAM et Swap (%)",
                               dates,
                               {"CPU": cpu, "RAM": ram, "Swap": swap})

    def render_users_process_chart(self, server):
        self.cursor.execute("""SELECT date, users_count, processes_count, zombies_count
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.cursor.fetchall()
        dates, users, procs, zombies = [], [], [], []

        for line in info:
            dates.append(line["date"])
            users.append(line["users_count"])
            procs.append(line["processes_count"])
            zombies.append(line["zombies_count"])

        self.fileName = "users_procs.svg"
        self.render_time_chart("Nombre d'utilisateurs et processus", dates,
                          {"Utilisateurs": users, "Processus": procs, "Zombies": zombies})

    def render_disks_use_chart(self, server):
        self.cursor.execute("""SELECT DISTINCT(date)
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        dates = [ res["date"] for res in self.cursor.fetchall() ]

        self.cursor.execute("""SELECT DISTINCT(mnt)
                               FROM statDisk
                               WHERE server_name LIKE ?""", [server])
        disks = [ res["mnt"] for res in self.cursor.fetchall() ]
        infoDisks = {}

        for disk in disks:
            self.cursor.execute("""SELECT stat.date, used, total
                                   FROM stat
                                       LEFT OUTER JOIN statDisk USING (server_name, date)
                                   WHERE server_name = ? AND mnt = ?""",
                                   [server, disk])
            info = self.cursor.fetchall()
            print disk
            print info

            infoDisks[disk] = []

            for line in info:
                if (line["used"] == ""):
                    infoDisks[disk].append(0)
                else:
                    infoDisks[disk].append(line["used"] * 100 / line["total"])


        self.fileName = "disks_use.svg"
        self.render_time_chart("Utilisation des disques (%)", dates, infoDisks)

    def render_single_disk_chart(self, dates = []):
        self.cursor.execute("""SELECT date, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.cursor.fetchall()

        dates, cpu, ram, swap = [], [], [], []

        for line in info:
            dates.append(line["date"])
            cpu.append(line["cpu_used"])
            ram.append(line["ram_used"] * 100 / line["ram_total"])
            swap.append(line["swap_used"] * 100 / line["swap_total"])
        self.fileName = "single_disk.svg"
        self.render_time_chart("Utilisation d'un seul disk (GB)", dates,
                          {mount: used})



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Interface()

if __name__=='__main__':
    main()

