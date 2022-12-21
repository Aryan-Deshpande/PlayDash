from flask import Flask
from flask_cors import CORS

import secrets
import redis

from backend.db import connect

# creates a flask app instance and sets the secret key for session management
app = Flask(__name__, template_folder='../content/templates')
r = redis.Redis(host='localhost', port=6379, db=0)

cur, connection = connect()

# cors stuff
CORS(app)

# sessions are implemented using a custom caching feature using redis
# sessions are stored in redis with a key of the sessionId and a value of the session data
# the session data is serialized using json
# the session data is stored in redis for 1 hour
# sessionId is generated using secrets.token_hex(16)
# returnes a sessionId if successful, otherwise returns false

from . import routes
from api import vendor

# later rate limiter