import json
import secrets
from flask import jsonify, request
from backend import app
from backend.db import cur, connection
# generate api key, and token to get access to the API
# api key for vendors

## The Vendor Requires A password & username created at agreement


# Tested, generates a api key that can be used to get data pertaining to the particular event you organized
@app.route('/api/v1/gen',methods=['POST'])
def genaapikey():
        if (request.json['username'] is not None) and (request.json['password'] is not None):
            uname = request.json['username']
            password = request.json['password']

            cur.execute('SELECT * FROM vendor WHERE uname=%s AND password=%s',(uname,password))
            if cur.fetchone() is not None:
                print('in here')
                apiKey = secrets.token_urlsafe(32)
                cur.execute('UPDATE vendor SET token=%s WHERE uname=%s',(apiKey, uname))
                connection.commit()
                return jsonify(apiKey)
            else:
                return jsonify('Access Denied 1')
            
        return jsonify('Access Denied 2')

# Tested, api for the particular vendor, gets data for your event
@app.route('/api/v1/getdata', methods=['GET'])
def getdata():
    if request.headers['HTTP_X_API_KEY'] is not None:
        data = {}
        token = request.headers['HTTP_X_API_KEY']

        cur.execute('SELECT id FROM vendor WHERE token=%s',(token,))
        vid = cur.fetchone()[0]
    
        if vid is None:
            return jsonify('create a token first')

        else:
            cur.execute('SELECT * FROM events WHERE vid=%s', (vid,))
            obj = [cur.fetchone()]

            for i,event in enumerate(obj):
                id = event[2]
                cur.execute('SELECT id,name FROM uses WHERE id=%s', (id,))
                data[i] = [{"event":event},{"user":cur.fetchone()}]

            return jsonify(data)
    else:
        return jsonify({'Resource denied'},403)

# print(secrets.token_urlsafe(32)) # generates a random string

################ fix schema ################