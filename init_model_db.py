import sqlite3

conn = sqlite3.connect("database_models.db")
cursor = conn.cursor()
count = 3

createtable = False
filltable = False

# creating table
if createtable:
    cursor.execute("""CREATE TABLE models
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    path TEXT NOT NULL,
                    database TEXT NOT NULL)
                   """)

if filltable:
    cursor.execute("INSERT INTO models (title, path, database) VALUES (?, ?, ?)",
                ('First neural network training model', 'model/model', 'database1')
                )
    conn.commit()

with conn:
    cur = conn.cursor()
    cur.execute("SELECT * FROM models")
    rows = cur.fetchall()

    for row in rows:
        print(row[0])
        print(row[1])
        print(row[2])
        print(row[3])

conn.close()
#exit(0)

#print (check_fu(0.00632, 18.0, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1.0, 296.0, 15.3, 369.90, 4.98, 131.89399999999998))