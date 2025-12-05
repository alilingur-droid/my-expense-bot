import sqlite3

conn = sqlite3.connect('mydatabase.db')

cursor = conn.cursor()


cursor.execute('''
CREATE TABLE noone(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               sum REAL NOT NULL,
               category TEXT NOT NULL,
               description TEXT DEFAULT ""
)
''')

conn.commit()
conn.close()