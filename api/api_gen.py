from functools import wraps
import json
import secrets

from flask import jsonify, request, abort
from backend import app, cur, connection

from werkzeug.exceptions import BadRequest, HTTPException

@app.errorhandler(Exception)
def handle_badreq(w):
    response = w.get_response()
    response.data = json.dumps({ 'error':{'status':w.code, 'content': w.description }})

    return response

# generate api key, and token to get access to the API
# api key for vendors

## The Vendor Requires A password & username created at agreement

# Added a custom exception handler & responder
def requires_apikey(func):
    
    @wraps(func)

    def check_apikey(*args,**kwargs):
        exists = request.headers.get('HTTP_X_API_KEY')
        
        if exists:
            
            try:
                cur.execute('SELECT * FROM vendor WHERE token=%s',(request.headers['HTTP_X_API_KEY'],))
                obj = cur.fetchone()

                if obj is None:
                    abort(404,'apiKey does not exist, create a token first')

            except:
                return abort(404, 'oops something is wrong with the server sorry !')
        return func(*args,**kwargs)
    return check_apikey
        

            
@app.route('/api/v1/gen',methods=['POST','GET'])
def genaapikey(apiKey):
        if (request.json['username'] is not None) and (request.json['password'] is not None):
            uname = request.json['username']
            password = request.json['password']

            cur.execute('SELECT id FROM vendor WHERE uname=%s AND password=%s',(uname,password))
            if cur.fetchone() is not None:
                # creates and updates api key to the vendor

                apiKey = secrets.token_urlsafe(32) # creates a token of 32 bytes
                cur.execute('UPDATE vendor SET token=%s WHERE uname=%s',(apiKey, uname))
                connection.commit()

                return jsonify(apiKey)
            
            # need to create a custom non-exception response
            return abort(405,'Vendor does not exist')

        return abort(406,'Enter your username and password')

# api for the particular vendor
@app.route('/api/v1/getdata', methods=['GET'])
@requires_apikey
def getdata():
    if request.headers['HTTP_X_API_KEY']:
        data = {}
        token = request.headers['HTTP_X_API_KEY']

        cur.execute('SELECT * FROM vendor WHERE token=%s',(token,))
        obj = cur.fetchone()

        if obj is None:
            return jsonify('create a token first')

        else:
            vid = obj[0][0]
            cur.execute('SELECT * FROM events WHERE vid=%s', (vid,))
            obj = [cur.fetchone()]

            for i,event in enumerate(obj):
                id = event[2]
                cur.execute('SELECT id,name FROM uses WHERE id=%s', (id,))
                data[i] = [{"event":event},{"user":cur.fetchone()}]

            return jsonify(data)

    else:
        return jsonify( {'Resource denied'},403 ) # or aboort(403, 'resource denied')

################ fix schema ################