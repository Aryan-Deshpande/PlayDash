import os
import psycopg2

def connect():

    # Connection to the database
    connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    port=os.getenv('DB_PORT')
    )

    # creating a connection cursor to execute SQL commands
    cur = connection.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS v ( id SERIAL PRIMARY KEY, vname VARCHAR(50), uname VARCHAR(50), password VARCHAR(50), token VARCHAR(50))')
    cur.execute('CREATE TABLE IF NOT EXISTS e ( id SERIAL PRIMARY KEY, name VARCHAR(50), vid INTEGER, FOREIGN KEY (vid) REFERENCES v(id))')
    cur.execute('CREATE TABLE IF NOT EXISTS u ( id SERIAL PRIMARY KEY, name VARCHAR(50), password VARCHAR(50), eventid INTEGER, FOREIGN KEY (eventid) REFERENCES e(id))')
    connection.commit()

    return cur, connection


# used by server.py, mw.py
# use cursor to perform database operations