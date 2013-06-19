import os
from flask import Flask
from sqlite3 import dbapi2 as sqlite

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
