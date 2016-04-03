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
        self.browser = False

        # Connexion BD
        self.conn = sqlite3.connect("../data/sonde_info.db")
        self.conn.row_factory = dict_factory
        self.c = self.conn.cursor()

        self.c.execute("SELECT name, ip, uptime FROM server")
        servers = self.c.fetchall()

        for s in servers:
            print s["name"]
            self.c.execute("""SELECT cpu_used, ram_used, ram_total, swap_used, swap_total
                              FROM stat
                              WHERE server_name LIKE ?""", [s["name"]])
            info_CPU_RAM = self.c.fetchall()
            print info_CPU_RAM

        dates = [
                datetime(2013, 1, 2, 12, 0),
                datetime(2013, 1, 12, 14, 30, 45),
                datetime(2013, 2, 2, 6),
                datetime(2013, 2, 22, 9, 45)
                ]
        cpu = [5, 30, 18, 1]
        ram = [20, 80, 50, 15]
        swap = [2, 15, 5, 0]
        self.fileName = "cpu_ram.svg"
        self.render_cpu_ram_chart(dates, cpu, ram, swap)

        users = [2, 3, 1, 5]
        procs = [6, 10, 2, 20]
        zombies = [0, 0, 1, 1]
        self.fileName = "users_procs.svg"
        self.render_users_process_chart(dates, users, procs, zombies)

        disksUse = {}
        disksUse["sda0"] = [30, 31, 40, 29]
        disksUse["sda1"] = [10, 9, 15, 35]
        self.fileName = "disks_use.svg"
        self.render_disks_use_chart(dates, disksUse)

        useDisk0 = [15, 18, 30, 12]
        self.fileName = "single_disk.svg"
        self.render_single_disk_chart("GB sda0", dates, useDisk0)


    def date_formatter(self, dt):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    def render_chart(self, chart):
        if (self.browser == True):
            chart.render_in_browser()
        else:
            chart.render_to_file(self.fileName)


    def render_cpu_ram_chart(self, dates = [], cpu = [], ram = [], swap = []):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = "Utilisation de CPU, RAM et Swap (%)"
        chart.x_labels = map(self.date_formatter, dates)
        chart.add("CPU", cpu)
        chart.add("RAM", ram)
        chart.add("Swap", swap)
        self.render_chart(chart)

    def render_users_process_chart(self, dates = [], users = [], procs = [], zombies = []):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = "Nombre d'utilisateurs et processus"
        chart.x_labels = map(self.date_formatter, dates)
        chart.add("Utilisateurs", users)
        chart.add("Processus", procs)
        chart.add("Zombies", zombies)
        self.render_chart(chart)

    def render_disks_use_chart(self, dates = [], disksInfo = {}):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = "Utilisation des disques (%)"
        chart.x_labels = map(self.date_formatter, dates)
        for disk in disksInfo:
            chart.add(disk, disksInfo[disk])
        self.render_chart(chart)

    def render_single_disk_chart(self, mount, dates = [], used = []):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = "Utilisation d'un seul disk (GB)"
        chart.x_labels = map(self.date_formatter, dates)
        chart.add(mount, used)
        self.render_chart(chart)



#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    Interface()

if __name__=='__main__':
    main()

