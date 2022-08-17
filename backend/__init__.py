from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

from backend import routes
from Api import api_gen
# later rate limiter