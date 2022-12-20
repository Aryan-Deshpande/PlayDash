from werkzeug.security import generate_password_hash, check_password_hash

import psycopg2
import os

from backend import cur, connection #added backend.db

def checkuser(username,password):

    if username and password:

        try:
            cur.execute("SELECT * FROM u WHERE name=%s", (str(username),))

        except Exception as e:

            connection.rollback()
            return False 
 
        account = cur.fetchone()
        if account:
            password_res = account[2]
            
            res = check_password_hash(password_res, password)

            if res:
                return account[0]

            else:
                return False

        else:
            return False

    return False

# registers a user
def register(username,password):
    
    print(username, password)

    try:

        cur.execute('SELECT * FROM u WHERE name=%s',(str(username),))
        account = cur.fetchone()
        print(account, "account")

        if account == None:

            password = generate_password_hash(password)
            cur.execute("INSERT INTO u (name,password) values (%s,%s)", (str(username),str(password) ))
            connection.commit()

            cur.execute('SELECT id FROM u WHERE name=%s',(str(username),))
            id = cur.fetchone()[0]

            return id

        else:
            
            return False
    
    except Exception as e:
        connection.rollback()
        print(e)

# creates a booking by mapping user to the event id
def createBooking(userId,eventId,eventName): # include later, timeSlot
    # check if user has event already booked
    
    """cur.execute("SELECT id FROM u WHERE name=%s",(userId,))
    query1 = cur.fetchone()
    print(cur.fetchone())
    userId = query1.item()"""

    cur.execute('SELECT id FROM e WHERE name=%s',(str(eventName,)) )
    item = cur.fetchone()

    print(item, ' item ')

    try:
        print(userId)
        
        obj = cur.execute("UPDATE e SET usesid=%s WHERE id=%s AND name=%s", (userId,eventId,str(eventName)) )
        connection.commit()
        return True
    except:
        return False


# get page details
def pageFunc(eventName):
    cur.execute("SELECT * FROM e;",(str(eventName,)) )
    result = cur.fetchone()
    return result  # You can also use curr.fetchall() if you have multiple output rows 
    
def pageFuncs():
    cur.execute("SELECT id,name,date FROM e")
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


