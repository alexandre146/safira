# -*- coding: utf-8 -*-
import sys
import sqlite3

sqlite_file = 'safira.sqlite3'    # name of the sqlite database file

# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute("UPDATE programacao_alunosubmissaoexerciciopratico SET avaliacao=50 WHERE id=1")

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
