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
import os

bd = "/home/etudiants/inf/uapv1601663/sonde_info.db"
try: os.remove(bd)
except: pass

conn = sqlite3.connect(bd)
conn.close()

conn = sqlite3.connect(bd)
c = conn.cursor()

sql = '''
    CREATE TABLE IF NOT EXISTS server(
        name VARCHAR(50),
        ip VARCHAR(10),
        uptime VARCHAR(10)
    )'''
print sql
c.execute(sql)
conn.commit()

sql = '''
    CREATE TABLE IF NOT EXISTS stat(
        server_name VARCHAR(50),
        date VARCHAR(10),
        cpu_used float ,
        ram_used integer,
        ram_total integer,
        swap_used integer,
        swap_total integer,
        processes_count integer,
        zombies_count integer,
        users_count integer,
        FOREIGN KEY (server_name) REFERENCES server(name),
        PRIMARY KEY (server_name, date)
    )'''
print sql
c.execute(sql)
conn.commit()

sql = '''
    CREATE TABLE IF NOT EXISTS statDisk(
        server_name VARCHAR(50),
        date VARCHAR(10),
        mnt VARCHAR(20) ,
        used integer,
        total integer,
        PRIMARY KEY (server_name, date, mnt)
        FOREIGN KEY (server_name, date) REFERENCES stat(server_name, date)
    )'''
print sql
c.execute(sql)
conn.commit()

sql = '''
    CREATE TABLE IF NOT EXISTS user(
        server_name VARCHAR(50) PRIMARY KEY,
        users_list text,
        FOREIGN KEY (server_name) REFERENCES server(name)
    )'''
print sql
c.execute(sql)
conn.commit()

sql = '''
    CREATE TABLE IF NOT EXISTS process(
        server_name VARCHAR(50) PRIMARY KEY,
        greedy_list text,
        FOREIGN KEY (server_name) REFERENCES server(name)
    )'''
print sql
c.execute(sql)
conn.commit()