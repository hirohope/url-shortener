import os
from flask import Flask, request, render_template
from sqlite3 import dbapi2 as sqlite
from models import Shortened
from database import db_session


app = Flask(__name__)
if app.debug is not True:   
	import logging
	from logging.handlers import RotatingFileHandler
	file_handler = RotatingFileHandler('python.log', maxBytes=1024 * 1024 * 100, backupCount=20)
	file_handler.setLevel(logging.ERROR)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	file_handler.setFormatter(formatter)
	app.logger.addHandler(file_handler)	


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/short', methods=['POST', 'GET'])
def short():
	error = None
	url = None
	short = None
	if request.method == 'GET':
		if 'url' in request.args:
			url = request.args['url']
			s = Shortened.query.filter(Shortened.url == url).first()
			if s == None:
				s = Shortened(url)
				db_session.add(s)
				db_session.commit()
			short = s.short
		else:
			error = "There's no url"
	return render_template('short.html', error=error, url=url, short=short)

@app.route('/links')
def links():
	shorts = Shortened.query.all()
	return "<br>".join(map(lambda x: str(x), shorts))


