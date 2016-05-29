#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Graphs :                                                               #
#        Cette classe implémente plusieurs méthodes qui permettent la       #
#        génération des graphiques d'évolution des données.                 #
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
    # Les graphes sont stockés dans un dossier temporaire avant
    # d'être affichés dans le navigateur
    PATH_HTML = "interface/tmp/chart.html"
    PATH_SVG = "interface/tmp/chart.svg"

    # Le graphes sont affichés dans le navigateur ayant le nom dans cette constante
    DEFAULT_BROWSER = "firefox"


    def __init__(self, dataBaseInstance):
        # Connexion BD
        self.db = dataBaseInstance


    def date_formatter(self, dt):
        return dt.strftime("%d-%m-%Y %H:%M:%S")

    # Fonction qui crée un fichier HTML avec un graphe SVG
    def create_html(self, chart, title):
        # On crée le SVG
        chart.render_to_file(self.PATH_SVG)
        f = open(self.PATH_SVG, "r")
        content = f.read()
        f.close()

        # On crée un page HTML
        f = open(self.PATH_HTML, "w")
        f.write("""<html><head><title>""" + title + """</title></head><body>
                       <svg width='100%' height='100%'>""" + content + """</svg>
                </body></html>""")
        f.close()
        return self.PATH_HTML


    # Cette fonction permet l'affichage d'un graphe dans le navigateur ou le stockage en disque
    def save_or_display_chart(self, chart, fileName, browser = True):
        # Pour desactiver la console
        devnull = open(os.devnull, "w")

        # Affichage
        if browser:
            html = self.create_html(chart, fileName)
            subprocess.Popen([self.DEFAULT_BROWSER, html], stdout=devnull, stderr=devnull)
        else:
            chart.render_to_file(fileName)


    # Création d'un graphe de type "Line", avec les données recues
    def render_time_chart(self, title, dates=[], linesInfo={}):
        chart = pygal.Line(x_label_rotation=20)
        chart.title = title
        chart.x_labels = dates
        for label in linesInfo:
            chart.add(label, linesInfo[label])

        self.save_or_display_chart(chart, title)



#############################################################################
#    Fonctions pour créer différents graphes avec les données en BDD        #
#############################################################################

    # Évolution du CPU et de la mémoire dans le temps
    def render_cpu_ram_chart(self, server):
        self.db.execute("""SELECT timestamp, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()
        dates, cpu, ram, swap = [], [], [], []

        for line in info:
            dates.append(line["timestamp"])
            cpu.append(line["cpu_used"])
            ram.append(line["ram_used"] * 100 / line["ram_total"])
            swap.append(line["swap_used"] * 100 / line["swap_total"])

        # On affiche le graphe
        self.render_time_chart("Utilisation de CPU, RAM et Swap (%)",
                               dates,
                               {"CPU": cpu, "RAM": ram, "Swap": swap})


    # Nombre de processus par rapport aux utilisateur connectés
    def render_users_process_chart(self, server):
        self.db.execute("""SELECT timestamp, users_count, processes_count, zombies_count
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()
        dates, users, procs, zombies = [], [], [], []

        for line in info:
            dates.append(line["timestamp"])
            users.append(line["users_count"])
            procs.append(line["processes_count"])
            zombies.append(line["zombies_count"])

        # On affiche le graphe
        self.render_time_chart("Nombre d'utilisateurs et processus", dates,
                          {"Utilisateurs": users, "Processus": procs, "Zombies": zombies})


    # Évolution de l'utilisation de disque dans le temps
    def render_disks_use_chart(self, server):
        self.db.execute("""SELECT DISTINCT(timestamp)
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        dates = [ res["timestamp"] for res in self.db.fetchall() ]

        self.db.execute("""SELECT DISTINCT(mnt)
                               FROM statDisk
                               WHERE server_name LIKE ?""", [server])
        disks = [ res["mnt"] for res in self.db.fetchall() ]
        infoDisks = {}

        for disk in disks:
            self.db.execute("""SELECT stat.timestamp, used, total
                                   FROM stat
                                       LEFT OUTER JOIN statDisk USING (server_name, timestamp)
                                   WHERE server_name = ? AND mnt = ?""",
                                   [server, disk])
            info = self.db.fetchall()

            infoDisks[disk] = []

            for line in info:
                if (line["used"] == ""):
                    infoDisks[disk].append(0)
                else:
                    infoDisks[disk].append(line["used"] * 100 / line["total"])

        # On affiche le graphe
        self.render_time_chart("Utilisation des disques (%)", dates, infoDisks)


    # Données d'un seul disque
    def render_single_disk_chart(self, dates = []):
        self.db.execute("""SELECT timestamp, cpu_used, ram_used, ram_total, swap_used, swap_total
                               FROM stat
                               WHERE server_name LIKE ?""", [server])
        info = self.db.fetchall()

        dates, cpu, ram, swap = [], [], [], []

        for line in info:
            dates.append(line["timestamp"])
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

