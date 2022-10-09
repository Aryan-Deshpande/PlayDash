import os
import psycopg2

def connect():
    connection = psycopg2.connect(
    host=os.environ.get('DB_HOST'),
    database=os.environ.get('DB_NAME'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS'),
    port=os.environ.get('DB_PORT')
    )
    cur = connection.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS vendor (id SERIAL PRIMARY KEY, uname VARCHAR(50), password VARCHAR(50), token VARCHAR(50))')
    cur.execute('CREATE TABLE IF NOT EXISTS events (id SERIAL PRIMARY KEY, vid INTEGER, uid INTEGER, event VARCHAR(50))')
    cur.execute('CREATE TABLE IF NOT EXISTS uses (id SERIAL PRIMARY KEY, name VARCHAR(50))')
    connection.commit()

    return cur, connection


# used by server.py, mw.py
# use cursor to perform database operations