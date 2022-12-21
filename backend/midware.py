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

    cur.execute('SELECT id FROM e WHERE name=%s',(str(eventName),) )
    item = cur.fetchone()

    print(item, ' item ')

    try:
        print(userId)
        
        obj = cur.execute("UPDATE u SET eventid=%s WHERE id=%s", (eventId,userId))
        connection.commit()
        return True

    except Exception as e:
        connection.rollback()
        print(e)
        return False


# get page details
def pageFunc(eventName):
    cur.execute("SELECT * FROM e WHERE name=%s",(str(eventName),) )
    result = cur.fetchone()
    return result  # You can also use curr.fetchall() if you have multiple output rows 
    
def pageFuncs():
    cur.execute("SELECT id,name,date FROM e")
    obj = cur.fetchall()
    return obj

def checkbooking(userId, eventId):
    try:
        cur.execute('SELECT eventid FROM u WHERE id=%s',(userId,))
        result = cur.fetchone()
        print(result, "result")
        print(eventId, "eventId")

        if result[0] is not None:

            if result[0] == eventId:
                return True

            else:
                return False
        else:
            return False

    except Exception as e:
        connection.rollback()  
        print(e)
        return False


