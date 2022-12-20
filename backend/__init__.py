from flask import Flask
from flask_session import Session
from flask_cors import CORS
import secrets

from backend.db import connect

# creates a flask app instance and sets the secret key for session management
app = Flask(__name__, template_folder='../content/templates')
app.secret_key = secrets.token_urlsafe(16)

cur, connection = connect()

# session stuff
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# cors stuff
CORS(app)

from . import routes
from api import vendor
# later rate limiter