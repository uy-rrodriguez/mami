#!/usr/bin/python
# -*- coding: utf-8 -*-

#############################################################################
#    DBAccess :                                                             #
#        Classe pour acceder à la BD.                                       #
#        Implémente des méthodes qui simplifient l'accès.                   #
#                                                                           #
#############################################################################

import sqlite3
import sys



#############################################################################
#    Constantes.                                                            #
#############################################################################

PATH = "data/sonde_info.db"



#############################################################################
#    DBAccess.                                                              #
#############################################################################

class DBAccess:
    def __init__(self):
        self.conn = sqlite3.connect(PATH)
        self.conn.row_factory = sqlite3.Row     # Permets la recuperation dans des tableaux associatifs
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def get_all(self, table):
        return self.cursor.execute("SELECT * FROM " + table)

    def get_by(self, table, field, value):
        return self.cursor.execute("SELECT * FROM " + table + " WHERE " + field + " = ?", [value])

    def get_by_fields(self, table, fields, values):
        sql = "SELECT * FROM " + table + " WHERE " + fields[0] + " = ? "
        for i in range(1, len(fields)):
            sql += " AND " + fields[i] + " = ?"
        return self.cursor.execute(sql, values)

    def get_last_date(self, server):
        return self.cursor.execute("SELECT MAX(timestamp) FROM stat WHERE server_name = ?", [server])

    def execute(self, sql, params = []):
        return self.cursor.execute(sql, params)

    def fetchall(self):
        return self.cursor.fetchall()


#############################################################################
#    Main pour tester le module.                                            #
#############################################################################

def main():
    print("DBAccess")

if __name__=='__main__':
    main()
