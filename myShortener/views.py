from myShortener import app
from myShortener.database import db_session
from myShortener.models import Shortened, Log
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

@app.route('/')
def index():
	return render_template('index.html', url = request.args.get('url', ''), custom = request.args.get('custom', ''))

@app.route('/<short>')
def unfold(short):
	s = Shortened.query.filter(Shortened.short == short).first()
	if s == None:
		abort(404)
	else:
		time = Log(s)
		db_session.add(time)
		db_session.commit()
		return redirect(s.url)

@app.route('/_short', methods=['POST', 'GET'])
def short():
	error = None
	url = None
	short = None
	if request.method == 'GET':
		if 'url' in request.args:
			url = request.args['url']
			if 'custom' in request.args and request.args['custom']:
				short = request.args['custom']
				s = Shortened.query.filter(Shortened.url == url)
				if s != None and Shortened.query.filter(Shortened.short == short).first() != None:
					flash("Custom URL already taken")
					return redirect("/?url={}&custom={}".format(url,short))
				else:
					short = s.short
			else:
				s = Shortened.query.filter(Shortened.url == url).first()
				if s == None:
					s = Shortened(url)
					db_session.add(s)
					db_session.commit()
			short = s.short
			
		else:
			error = "There's no url"
	return render_template('short.html', error=error, url=url, short=short)

@app.route('/_links')
def links():
	shorts = Shortened.query.all()
	return "<br>".join(map(lambda x: str(x), shorts))

@app.route('/_times')
def times():
	logs = Log.query.all()
	return "<br>".join(map(lambda x: str(x), logs))


