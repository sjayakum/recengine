import sqlite3

con = sqlite3.connect('stock.db')
cursor = con.cursor()
cursor.execute("SELECT * from details")
print  cursor.fetchone()