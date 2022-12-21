from backend import app, cur, connection
from flask import jsonify, request, abort, render_template
from werkzeug.exceptions import BadRequest, HTTPException

import json
import secrets
from functools import wraps

'''@app.errorhandler(Exception)
def handle_badreq(w):
    #response = w.get_response()
    #response.data = json.dumps({ 'error':{'status':w.code, 'content': w.description }})

    return "respons"
'''
# generate api key, and token to get access to the API
# api key for vendors

## The Vendor Requires A password & username created at agreement

# Added a custom exception handler & responder
def req_api_key(func):
    
    @wraps(func)

    def check_api_key(*args,**kwargs):
        # this statement retrieves the api key from the req headers and checks if it exists
        exists = request.headers.get('X_API_KEY')
        
        if exists:
            try:
                # this sql query checks if the api key exists in the database
                cur.execute('SELECT * FROM v WHERE token=%s',(request.headers['X_API_KEY'],))
                obj = cur.fetchone()

                # if it does not exist, it returns an error
                if obj is None:
                    return jsonify({'error':'api key is invalid'})

            except:
                return abort(404, 'oops something is wrong with the server sorry !')

        else:
            # if none is found in the query result, then it returns an error
            return jsonify({'error':'api key is required'})

        # if the api key is valid, then it returns the function
        return func(*args,**kwargs)
    return check_api_key
        

# this function is used to generate an API key for the vendor
@app.route('/api/v1/gen',methods=['POST'])
def gen_api_key():
        
        # checks if request param username, password are not empty
        if (request.json['username'] is not None) and (request.json['password'] is not None):
            uname = request.json['username']
            password = request.json['password']

            # sql query checks which vendor has both password and username
            cur.execute('SELECT id FROM v WHERE uname=%s AND password=%s',(uname,password))

            if cur.fetchone() is not None:
                # creates a token of 32 bytesa
                apiKey = secrets.token_urlsafe(32)

                # creates and updates api key to the vendor
                cur.execute('UPDATE v SET token=%s WHERE uname=%s',(apiKey, uname))
                connection.commit()

                return jsonify(apiKey)
            
            # need to create a custom non-exception response
            return abort(405,'Vendor does not exist')

        return abort(406,'Enter your username and password')

# api for the particular vendor, to retrieve data partaining to their event
@app.route('/api/v1/getdata', methods=['GET'])
@req_api_key
def getdata():

    # checks if api key exists in the header
    if request.headers['X_API_KEY']:

        data = {}

        # retrieves the api key from the header
        token = request.headers['X_API_KEY']

        # sql query to check if the api key exists
        cur.execute('SELECT * FROM v WHERE token=%s',(token,))
        obj = cur.fetchone()

        # if it does not exist, it returns an error
        if obj is None:
            return jsonify({'error':'create a token first'})

        else:
            # nests the sql query to format users that are registered for the event
            vid = obj[0]

            # sql query to get the event based on the vendor id
            cur.execute('SELECT * FROM e WHERE vid=%s', (vid,))
            obj = [cur.fetchone()]
            print(obj)

            for i,event in enumerate(obj):

                # retrieving the event id
                id = event[0] 
                
                # sql query to get the users that are registered for the event
                cur.execute('SELECT id,name FROM u WHERE eventid=%s', (id,))
                data[i] = [{"event":event},{"user":cur.fetchone()}]

            return jsonify({'Registered':data})

    else:
        return jsonify( {'error':'Resource denied'},403 ) # or abort(403, 'resource denied')

#vendor event creation
@app.route('/api/v1/create/event',methods=['POST'])
@req_api_key
def eventcreate():

    # api key will be sent through, axios from the frontend
    key = str(request.headers.get('X_API_KEY'))
    print(key, 'this is the key')
    eventname = request.args.get('eventn')
    eventtime = request.args.get('eventt')
        
    if key is None:    
        return jsonify({"error":"provide an apikey"})

    try:
        
        # sql query to check if the api key exists
        cur.execute('SELECT id FROM v WHERE token=%s', (key,))

    except Exception as e:
        # if there is an error, it will rollback the changes
        connection.rollback()
        print(e)

        return jsonify({'error':'server side'})

    vendorid= cur.fetchone()[0]
    #print(vendorid)

    # sql query to insert the event into the database
    cur.execute('INSERT INTO e (name,date,vid) values(%s,%s,%s)',(eventname,eventtime,vendorid))
    connection.commit()

    return jsonify({'result':True})



################ fix schema ################