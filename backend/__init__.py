from flask import Flask
from flask_cors import CORS
from flask_session import Session

import secrets
import redis

from backend.db import connect

# creates a flask app instance and sets the secret key for session management

app = Flask(__name__, template_folder='../content/templates')
r = redis.Redis(host='localhost', port=6379, db=0)

app.secret_key = 'super secret key'
cur, connection = connect()

"""app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')"""


session = Session(app)

# cors stuff
CORS(app)

from . import routes
from api import vendor
# later rate limiter