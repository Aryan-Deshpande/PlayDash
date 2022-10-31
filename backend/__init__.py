from flask import Flask
from flask_session import Session
from flask_cors import CORS

from backend.db import connect

# creates a flask app instance and sets the secret key for session management
app = Flask(__name__, template_folder='../content/templates')

cur, connection = connect()

# session stuff
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# cors stuff
CORS(app)

from . import routes
from api import api_gen
# later rate limiter