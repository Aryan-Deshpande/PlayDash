import psycopg2
import os
from backend import cur, connection #added backend.db

# 
def checkuser(username,password):
    if username and password:
        cur.execute("SELECT id FROM uses WHERE name=%s AND password=%s", (username,password))
        id = cur.fetchone()[0]
        
        if id is not None:
            print(id, 'id displayed')
            cur.execute("SELECT name FROM uses WHERE name=%s AND password=%s", (username,password))

            # unhash the password
            unhpassword = password
            if password == unhpassword:
                return id
            else:
                return False
        else:
            return False
    return False

# registers a user
def register(username,password):
    cur.execute('SELECT name FROM uses WHERE name=%s',(username,))
    if cur.fetchone() is None:
        try:
            obj = cur.execute("INSERT INTO uses (name,password) values (%s,%s)", (username,password))
            connection.commit()

            cur.execute('SELECT id FROM uses WHERE name=%s', (username,))
            print(cur.fetchone(),"None")
            return cur.fetchone()[0]
        except:
            print('exception')
            return False
    return False

# creates a booking by mapping user to the event id
def createBooking(userId,eventId,eventName): # include later, timeSlot
    # check if user has event already booked
    
    """cur.execute("SELECT id FROM uses WHERE name=%s",(userId,))
    query1 = cur.fetchone()
    print(cur.fetchone())
    userId = query1.item()"""

    cur.execute('SELECT id FROM events WHERE name=%s',(eventName,))
    item = cur.fetchone()

    print(item, ' item ')

    try:
        print(userId)
        
        obj = cur.execute("UPDATE events SET usesid=%s WHERE id=%s AND name=%s", (userId,eventId,eventName))
        connection.commit()
        return True
    except:
        return False


# get page details
def pageFunc(eventName):
    cur.execute("SELECT * FROM events WHERE name=%s",(eventName,))
    result = cur.fetchone()
    return result  # You can also use curr.fetchall() if you have multiple output rows 
    
def pageFuncs():
    cur.execute('SELECT id,name FROM events')
    obj = cur.fetchall()
    return obj

def checkbooking(userId, eventId):
    try:
        cur.execute('SELECT usesid FROM events WHERE id=%s',(eventId,))
        if cur.fetchone()[0] is not None:
            if cur.fetchone()[0] == userId:
                return True
            else:
                return {"recipient":False} 
        else:
            return False
    except:
        return False


"""cur.execute('SELECT id FROM vendor WHERE token=%s',('hvz1QMGwW1rrRln-FYeruHOSwYEdXpEDB1mzOecSXrw',))
a = cur.fetchall()
print(a[0][0])"""

