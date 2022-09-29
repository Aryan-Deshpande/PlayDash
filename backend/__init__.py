from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='../content/templates')

from flask import Flask, render_template, redirect, request, session
from flask_session import Session

# session stuff
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

CORS(app)
Session(app)

from backend import routes
from api import api_gen
# later rate limiter