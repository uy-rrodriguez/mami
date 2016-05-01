#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    Stockage :                                                             #
#        Script création base de donnée                                     #
#                                                                           #
#                                                                           #
#                                                                           #
#                                                                           #
#############################################################################


import sqlite3

conn = sqlite3.connect('/home/etudiants/inf/uapv1601663/sonde_info.db')
c = conn.cursor()

c.executescript("""
    DELETE FROM statDisk;
    DELETE FROM stat;
    DELETE FROM server;
    DELETE FROM process;
""")


date1 = "2015-12-01"
date2 = "2015-12-20"
date3 = "2016-01-15"
date4 = "2016-02-08"
date5 = "2016-03-18"
date6 = "2016-04-05"

c.executescript("""
    INSERT INTO server (name, ip, uptime)
    VALUES
        ('Server 1', '192.168.151.1', '"""+date1+"""'),
        ('Server 2', '192.168.151.2', '2016-02-25');
""")


c.executescript("""
    INSERT INTO stat (server_name, date, cpu_used, ram_used, ram_total, swap_used,
                      swap_total, processes_count, zombies_count, users_count)
    VALUES
        ('Server 1', '"""+date1+"""', 30, 1000, 4000, 200, 2000, 5, 0, 2),
        ('Server 1', '"""+date2+"""', 70, 3000, 4000, 1000, 2000, 5, 1, 5),
        ('Server 1', '"""+date3+"""', 10, 500, 4000, 150, 2000, 5, 0, 1),
        ('Server 1', '"""+date4+"""', 90, 3800, 4000, 1500, 2000, 5, 0, 8),
        ('Server 1', '"""+date5+"""', 5, 2000, 4000, 500, 2000, 5, 0, 2),
        ('Server 1', '"""+date6+"""', 6, 2200, 4000, 200, 2000, 5, 0, 2),

        ('Server 2', '"""+date1+"""', 30, 1000, 4000, 200, 2000, 5, 0, 2),
        ('Server 2', '"""+date2+"""', 70, 3000, 4000, 1000, 2000, 5, 1, 5),
        ('Server 2', '"""+date3+"""', 10, 500, 4000, 150, 2000, 5, 0, 1),
        ('Server 2', '"""+date4+"""', 90, 3800, 4000, 1500, 2000, 5, 0, 8),
        ('Server 2', '"""+date5+"""', 5, 2000, 4000, 500, 2000, 5, 0, 2),
        ('Server 2', '"""+date6+"""', 6, 2200, 4000, 200, 2000, 5, 0, 2);
""")


c.executescript("""
    INSERT INTO statDisk (server_name, date, mnt, used, total)
    VALUES
        ('Server 1', '"""+date1+"""', 'sda0', 15000, 40000),

        ('Server 1', '"""+date2+"""', 'sda0', 18000, 40000),

        ('Server 1', '"""+date3+"""', 'sda0', 25000, 40000),
        ('Server 1', '"""+date3+"""', 'sda1', 10000, 20000),

        ('Server 1', '"""+date4+"""', 'sda0', 20000, 40000),
        ('Server 1', '"""+date4+"""', 'sda1', 10000, 20000),

        ('Server 1', '"""+date5+"""', 'sda0', 23000, 40000),
        ('Server 1', '"""+date5+"""', 'sda1', 12000, 20000),

        ('Server 1', '"""+date6+"""', 'sda0', 25000, 40000),
        ('Server 1', '"""+date6+"""', 'sda1', 10000, 20000),


        ('Server 2', '"""+date1+"""', 'sda0', 15000, 40000),

        ('Server 2', '"""+date2+"""', 'sda0', 18000, 40000),

        ('Server 2', '"""+date3+"""', 'sda0', 25000, 40000),
        ('Server 2', '"""+date3+"""', 'sda1', 10000, 20000),

        ('Server 2', '"""+date4+"""', 'sda0', 20000, 40000),
        ('Server 2', '"""+date4+"""', 'sda1', 10000, 20000),

        ('Server 2', '"""+date5+"""', 'sda0', 23000, 40000),
        ('Server 2', '"""+date5+"""', 'sda1', 12000, 20000),

        ('Server 2', '"""+date6+"""', 'sda0', 25000, 40000),
        ('Server 2', '"""+date6+"""', 'sda1', 10000, 20000);

""")


procs = """
    <greedy>
        <process>
            <pid>4040</pid>
            <command>firefox</command>
            <username>uapv1601663</username>
            <cpu>6.4</cpu>
            <ram>568233984</ram>
        </process>
        <process>
            <pid>3847</pid>
            <command>compiz</command>
            <username>uapv1601663</username>
            <cpu>5.7</cpu>
            <ram>228220928</ram>
        </process>
        <process>
            <pid>1818</pid>
            <command>Xorg</command>
            <username>root</username>
            <cpu>5.5</cpu>
            <ram>93159424</ram>
        </process>
        <process>
            <pid>4294</pid>
            <command>LightTable</command>
            <username>uapv1601663</username>
            <cpu>2.8</cpu>
            <ram>135430144</ram>
        </process>
        <process>
            <pid>16435</pid>
            <command>gnome-system-monitor</command>
            <username>uapv1601663</username>
            <cpu>3.7</cpu>
            <ram>81625088</ram>
        </process>
        <process>
            <pid>4223</pid>
            <command>LightTable</command>
            <username>uapv1601663</username>
            <cpu>0.2</cpu>
            <ram>98181120</ram>
        </process>
        <process>
            <pid>1</pid>
            <command>init</command>
            <username>root</username>
            <cpu>0.0</cpu>
            <ram>7061504</ram>
        </process>
        <process>
            <pid>2</pid>
            <command>kthreadd</command>
            <username>root</username>
            <cpu>0.0</cpu>
            <ram>0</ram>
        </process>
        <process>
            <pid>3</pid>
            <command>ksoftirqd/0</command>
            <username>root</username>
            <cpu>0.0</cpu>
            <ram>0</ram>
        </process>
        <process>
            <pid>5</pid>
            <command>kworker/0:0H</command>
            <username>root</username>
            <cpu>0.0</cpu>
            <ram>0</ram>
        </process>
    </greedy>
"""
c.executescript("""
    INSERT INTO process (server_name, greedy_list)
    VALUES
        ('Server 1', '""" + procs + """'),
        ('Server 2', '""" + procs + """');
""")
