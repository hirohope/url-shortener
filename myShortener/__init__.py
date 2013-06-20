from __future__ import with_statement
from contextlib import closing
from myShortener.database import db_session
from flask import Flask

import config

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


if app.debug is not True:   
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
	file_handler.setLevel(logging.ERROR)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.addHandler(file_handler)	

import views

@app.teardown_request
def teardown_request(exception):
  db_session.remove()