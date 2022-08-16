import os
import psycopg2

connection = psycopg2.connect(
    host='localhost',
    database='flasksql',
    user='postgres',
    password='aryan2002',
)
cur = connection.cursor()

# used by server.py, mw.py
# use cursor to perform database operations

