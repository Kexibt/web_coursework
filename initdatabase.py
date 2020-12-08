import sqlite3
import random as r
import math as m

conn = sqlite3.connect("database.db")  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
count = 500

def function():
    CRIM = r.random() + r.choice([0, 0, 0, 0, 0, 0, 1, 2]) #часто встречался 0
    ZN = r.randint(0, 100) #
    INDUS = r.randint(0, 2599) / 100 #
    CHAS = r.randint(0, 1) #
    NOX = r.randint(0, 9999) / 10000 #
    RM = r.randint(5000, 8000) / 1000 #
    AGE = r.randint(0,1000) / 10 #
    DIS = r.randint(0, 130000) / 10000 #
    RAD = r.randint(0, 24) #
    TAX = r.randint(200, 500) #
    PTRARIO = r.randint(100, 250) / 10 #
    B = r.choice([r.randint(0, 10000)/100, r.randint(30000, 40000)/100]) #
    LSTAT = r.randint(200, 3000) / 100 #
    PRICE = CRIM * m.sin(m.pi*INDUS) / (ZN + 0.1) + pow(NOX, CHAS) + m.exp(NOX * RM) + AGE / 10
    PRICE = PRICE + DIS * m.log2(TAX) + RAD / 24 * PTRARIO + B / LSTAT
    PRICE = round(PRICE, 2)
    return CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRARIO, B, LSTAT, PRICE

def check_fu(CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRARIO, B, LSTAT, PRICE):
    PRICE1 = CRIM * m.sin(m.pi * INDUS) / (ZN + 0.1) + pow(NOX, CHAS) + m.exp(NOX * RM) + AGE / 10
    PRICE1 = PRICE + DIS * m.log2(TAX) + RAD / 24 * PTRARIO + B / LSTAT
    PRICE1 = round(PRICE, 2)
    return (abs(PRICE - PRICE1))

# Создание таблицы
#cursor.execute("""CREATE TABLE prices
#                  (CRIM real, ZN real, INDUS real,
#                   CHAS real, NOX real, RM real, AGE real,
#                   DIS real, RAD real, TAX real, PTRARIO real,
#                   B real, LSTAT real, PRICE real)
#               """)

# Вставляем данные в таблицу
for i in range(count):
    CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRARIO, B, LSTAT, PRICE = function()
    cursor.execute("""INSERT INTO prices
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                   (CRIM, ZN, INDUS, CHAS, NOX, RM, AGE, DIS, RAD, TAX, PTRARIO, B, LSTAT, PRICE)
                   )
conn.commit()

#with conn:
#    cur = conn.cursor()
#    cur.execute("SELECT * FROM prices")
#    rows = cur.fetchall()

#    for row in rows:
#        print(row[0])

#exit(0)

#print (check_fu(0.00632, 18.0, 2.31, 0.0, 0.538, 6.575, 65.2, 4.0900, 1.0, 296.0, 15.3, 369.90, 4.98, 131.89399999999998))