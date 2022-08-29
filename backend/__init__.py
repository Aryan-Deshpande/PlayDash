from flask import Flask
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#CORS(app)
Session(app)

from backend import routes
from Api import api_gen
# later rate limiter