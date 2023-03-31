import sqlite3

conn1 = sqlite3.connect('users.db')
c = conn1.cursor()

conn2 = sqlite3.connect('files.db')
c = conn2.cursor()

c.execute('''CREATE TABLE users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT,
              password TEXT)''')

c.execute('''CREATE TABLE files
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              filename TEXT,
              status TEXT)''')
conn1.commit()
conn1.close()
conn2.commit()
conn2.close()