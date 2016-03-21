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
conn = sqlite3.connect('sonde_info.db')

c = conn.cursor()
c= c.execute('''CREATE TABLE IF NOT EXISTS  server
             ( name VARCHAR(50),ip VARCHAR(10), uptime VARCHAR(10))''')

c= c.execute('''CREATE TABLE IF NOT EXISTS stat
             ( server_name VARCHAR(50) PRIMARY KEY, 
             	   date VARCHAR(10),
             	   cpu_used float ,
             	   ram_used integer,
             	   ram_total integer,
             	   swap_used integer,
             	   swap_total integer,
             	   processes_count integer,
             	   zombies_count integer,
             	   users_count integer,
             	   FOREIGN KEY (server_name) REFERENCES server(name))''')
c=c.execute('''CREATE TABLE IF NOT EXISTS statDisk
             ( server_name VARCHAR(50) PRIMARY KEY, 
             	   date VARCHAR(10),
             	   mnt VARCHAR(20) ,
             	   used integer,
             	   total integer,
             	   FOREIGN KEY (server_name) REFERENCES server(name))''')

c=c.execute('''CREATE TABLE IF NOT EXISTS user
             ( server_name VARCHAR(50) PRIMARY KEY, 
             	   users_list text,
             	   FOREIGN KEY (server_name) REFERENCES server(name))''')

c=c.execute('''CREATE TABLE IF NOT EXISTS process
             ( server_name VARCHAR(50) PRIMARY KEY, 
             	   greedy_list text,
             	   FOREIGN KEY (server_name) REFERENCES server(name))   ''')

conn.commit
