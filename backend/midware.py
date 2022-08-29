import psycopg2
import os
from backend.db import cur, connection

def checkuser(username,password):
    username,hashed_password = cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username,password))
    unhashed_password = 1 # unhash
    if username and password:
        if password ==  unhashed_password:
            return True
        else:
            return False
    else:
        return False

def register(username,password):
    try:
        obj = cur.execute("INSERT INTO users.person (username,password) values(%s,%s)", (username,password))
        return True
    except:
        print("not able to insert person")

def createBooking(userId,eventId,eventName): # include later, timeSlot
    obj = cur.execute("UPDATE events SET usesid=%s WHERE id=%s AND name=%s", (userId,eventId,eventName))
    connection.commit()

# get page details
def pageApi(eventName):
    cur.execute("SELECT * FROM events WHERE name=%s",(eventName,))
    return cur.fetchone()  # You can also use curr.fetchall() if you have multiple output rows 
    
def pageApis():
    cur.execute('SELECT id,name FROM events')
    obj = cur.fetchall()
    return obj

cur.execute('SELECT id FROM vendor WHERE token=%s',('hvz1QMGwW1rrRln-FYeruHOSwYEdXpEDB1mzOecSXrw',))
a = cur.fetchall()
print(a[0][0])

