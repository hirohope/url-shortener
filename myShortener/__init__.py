from __future__ import with_statement
from contextlib import closing
from flask import Flask

#configuration
#DATABASE = 'sqlite:////tmp/flasktest.db'

#base produccion
DATABASE = 'postgres://hekujbkpoqpvlh:eUl2ZCB_6yZxsZtuecrIxMrRo8@ec2-23-23-214-251.compute-1.amazonaws.com:5432/d73lnbdmkeki55'

#base de prueba
#DATABASE = 'postgres://ozurdipdktghmd:wj1PDha64vao_Ekf5NvuJpYV_0@ec2-54-225-96-191.compute-1.amazonaws.com:5432/d6c9qd41ct33l5'

DEBUG = True
SECRET_KEY = 'llavepatitoamarillo278344h23nd923d239'
USERNAME = 'admin'
PASSWORD = 'admin'

#twitter
CONSUMER_KEY='M2eOi6OXTb6vAGkH5IUDWg'
CONSUMER_SECRET='MKct3sDdldAaMSpK7WIYdEnLarANH7AElo26Yk07GM'
REQUEST_TOKEN_URL='https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL='https://api.twitter.com/oauth/access_token'
AUTHORIZE_URL='https://api.twitter.com/oauth/authorize'
AUTHENTICATE_URL='https://api.twitter.com/oauth/authenticate'
CALLBACK_URL = 'http://test.wn.cl/_callback'


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

from myShortener.database import db_session
@app.teardown_request
def teardown_request(exception):
  db_session.remove()