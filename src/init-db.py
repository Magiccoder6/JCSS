import sqlite3

connection = sqlite3.connect('database.db')

connection.commit()
connection.close()