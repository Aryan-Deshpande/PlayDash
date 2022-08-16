import json
import secrets
from flask import jsonify, request
from backend import app
from backend.db import cur, connection
# generate api key, and token to get access to the API
# api key for vendors

@app.route('/api/v1/gen',methods=['POST','GET'])
def genaapikey():
        apiKey = secrets.token_urlsafe(32)
        cur.execute('INSERT INTO vendor (token) values (%s)',(apiKey,))
        connection.commit()
    #else:
        return jsonify(apiKey)

# api for the particular vendor
@app.route('/api/v1/getdata', methods=['GET'])
def getdata():
    if request.headers['HTTP_X_API_KEY']:
        data = {}
        token = request.headers['HTTP_X_API_KEY']

        cur.execute('SELECT id FROM vendor WHERE token=%s',(token,))
        obj = cur.fetchone()

        if obj is None:
            return jsonify('create a token first')

        else:
            vid = obj[0]
            cur.execute('SELECT * FROM events WHERE vid=%s', (vid,))
            obj = [cur.fetchone()]

            for i,event in enumerate(obj):
                id = event[2]
                cur.execute('SELECT id,name FROM uses WHERE id=%s', (id,))
                data[i] = [{"event":event},{"user":cur.fetchone()}]

            return jsonify(data)

    else:
        return jsonify({'Resource denied'},403)


print(secrets.token_urlsafe(32))

################ fix schema ################