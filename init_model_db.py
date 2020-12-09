import sqlite3

conn = sqlite3.connect("database_models.db")
cursor = conn.cursor()
count = 3

createtable = not True
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
                ('First default neural network training model', 'model/model1', 'database1')
                )

    cursor.execute("INSERT INTO models (title, path, database) VALUES (?, ?, ?)",
                    ('Second default neural network training model', 'model/model2', 'database2')
                    )

    cursor.execute("INSERT INTO models (title, path, database) VALUES (?, ?, ?)",
                    ('Third default neural network training model', 'model/model3', 'database3')
                    )
    conn.commit()


max_id = cursor.execute('SELECT max(id) FROM models').fetchone()[0]
print("-----", max_id)

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