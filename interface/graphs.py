#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Graphs :                                                               #
#        Cette classe implémente plusieurs methodes qui permettent la       #
#        generation des graphiques d'evolution des donnees.                 #
#                                                                           #
#############################################################################

import os
import subprocess
import pygal
from datetime import datetime


#############################################################################
#    Graphs.                                                                #
#############################################################################


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Graphs:
    def __init__(self, dataBaseInstance):
        # Connexion BD
        self.db = dataBaseInstance

    def date_formatter(self, dt):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    def create_html(self, chart, fileName):
        content = chart.render_data_uri()
        pathHTML = "tmp/chart.html"
        f = open(pathHTML, "w")
        f.write("""<html><head><title>""" + fileName + """</title></head><body>
                       <embed width='100%' height='100%' src='""" + content + """'/>
                </body></html>""")
        f.close()
        return pathHTML

    def save_or_display_chart(self, chart, fileName, browser = True):
        # Pour desactiver la console
        devnull = open(os.devnull, "w")

        # Affichage
        if browser:
            html = self.create_html(chart, fileName)
            subprocess.Popen(["firefox", html], stdout=devnull, stderr=devnull)
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
        self.db.execute("""SELECT date, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()
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
        self.db.execute("""SELECT date, users_count, processes_count, zombies_count
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()
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
        self.db.execute("""SELECT DISTINCT(date)
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        dates = [ res["date"] for res in self.db.fetchall() ]

        self.db.execute("""SELECT DISTINCT(mnt)
                               FROM statDisk
                               WHERE server_name LIKE ?""", [server])
        disks = [ res["mnt"] for res in self.db.fetchall() ]
        infoDisks = {}

        for disk in disks:
            self.db.execute("""SELECT stat.date, used, total
                                   FROM stat
                                       LEFT OUTER JOIN statDisk USING (server_name, date)
                                   WHERE server_name = ? AND mnt = ?""",
                                   [server, disk])
            info = self.db.fetchall()
            #print disk
            #print info

            infoDisks[disk] = []

            for line in info:
                if (line["used"] == ""):
                    infoDisks[disk].append(0)
                else:
                    infoDisks[disk].append(line["used"] * 100 / line["total"])


        self.fileName = "disks_use.svg"
        self.render_time_chart("Utilisation des disques (%)", dates, infoDisks)

    def render_single_disk_chart(self, dates = []):
        self.db.execute("""SELECT date, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()

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
    g = Graphs()
    g.cursor.execute("SELECT name, ip, uptime FROM server")
    servers = g.cursor.fetchall()

    dates = [
        datetime(2013, 1, 2, 12, 0),
        datetime(2013, 1, 12, 14, 30, 45),
        datetime(2013, 2, 2, 6),
        datetime(2013, 2, 22, 9, 45)
    ]

    for s in servers:
        #print s["name"]
        g.render_cpu_ram_chart(s["name"])
        g.render_users_process_chart(s["name"])
        g.render_disks_use_chart(s["name"])
        #g.render_single_disk_chart(dates)


if __name__=='__main__':
    main()

