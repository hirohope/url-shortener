from myShortener import app
from myShortener.database import db_session
from myShortener.models import Shortened, Log, User, Profile
from flask import Flask, request, session, g, redirect, url_for, \
	abort, render_template, flash

import urlparse
import oauth2 as oauth

@app.route('/')
def index():
	return render_template('index.html', url = request.args.get('url', ''), custom = request.args.get('custom', ''), session=session)

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
	if 'username' in session:
		username = session['username']
	error = None
	url = None
	short = None
	if request.method == 'GET':
		if 'url' in request.args:
			url = request.args['url']
			if 'custom' in request.args and request.args['custom']:
				short = request.args['custom']
				s = Shortened.query.filter(Shortened.short == short).first()
				if s == None:
					s = Shortened(url, short)
					db_session.add(s)
					db_session.commit()

					if 'username' in session:
						user = User.query.filter(User.id == session['user_id']).first()
						if s not in user.shorts:
							user.shorts.append(s)
							db_session.add(user)
							db_session.commit()

				else:
					s = Shortened.query.filter(Shortened.url == url).first()
					if s == None:
						flash("Custom URL already taken")
						return redirect("/?url={}&custom={}".format(url,short))
					elif 'username' in session:
						user = User.query.filter(User.id == session['user_id']).first()
						if s not in user.shorts:
							user.shorts.append(s)
							db_session.add(user)
							db_session.commit()

			else:
				s = Shortened.query.filter(Shortened.url == url).filter(Shortened.custom == False).first()
				if s == None:
					s = Shortened(url)
					db_session.add(s)
					db_session.commit()

					if 'username' in session:
						user = User.query.filter(User.id == session['user_id']).first()
						if s not in user.shorts:
							user.shorts.append(s)
							db_session.add(user)
							db_session.commit()

				elif 'username' in session:
					user = User.query.filter(User.id == session['user_id']).first()
					if s not in user.shorts:
						user.shorts.append(s)
						db_session.add(user)
						db_session.commit()

			short = s.short
			
		else:
			error = "There's no url"
	return render_template('short.html', error=error, url=url, short=short,session=session)

@app.route('/_links/')
def links():
	shorts = Shortened.query.all()
	return "<br>".join(map(lambda x: str(x), shorts))

@app.route('/_times')
def times():
	logs = Log.query.all()
	return "<br>".join(map(lambda x: str(x), logs))


@app.route('/_sign_in/')
def sign_in():
	consumer=oauth.Consumer(app.config['CONSUMER_KEY'],app.config['CONSUMER_SECRET'])
	client=oauth.Client(consumer)
	resp, content = client.request(app.config['REQUEST_TOKEN_URL'], "GET")

	if resp['status'] != '200':
		raise Exception("Invalid response %s." % resp['status'])

	session['request_token'] = dict(urlparse.parse_qsl(content))

	url_twitter = "{}?oauth_token={}".format(app.config['AUTHENTICATE_URL'], session['request_token']['oauth_token'])

	return redirect(url_twitter)
  
@app.route('/_callback', methods= ['GET'])
def callback():
	print request
	if request.method=='GET':

		oauth_token = request.args['oauth_token']
		oauth_verifier = request.args['oauth_verifier']

		token = oauth.Token(session['request_token']['oauth_token'],session['request_token']['oauth_token_secret'])
		token.set_verifier(oauth_verifier)
		
		consumer=oauth.Consumer(app.config['CONSUMER_KEY'],app.config['CONSUMER_SECRET'])
		client = oauth.Client(consumer, token)

		resp, content = client.request(app.config['ACCESS_TOKEN_URL'], "POST")
		
		if resp['status'] != '200':
			raise Exception("Invalid response %s." % resp['status'])
		
		access_token = dict(urlparse.parse_qsl(content))

		# print "------"
		# print access_token
		# print "------"
		# print session
		# print "------"

		user = User.query.filter(User.username == access_token['screen_name']).first()
		if user == None:
			user = User(access_token['user_id'], access_token['screen_name'], access_token['oauth_token_secret'])
			profile = Profile(user.id, access_token['oauth_token'],access_token['oauth_token_secret'])
			db_session.add(user)
			db_session.commit()
			db_session.add(profile)
			db_session.commit()

		session['username'] = user.username
		session['user_id'] = user.id
		return redirect("/")

@app.route('/_logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)

    return redirect("/")

@app.route('/_mylinks/')
def mylinks():
	if 'user_id' in session:
		user = User.query.filter(User.id == session['user_id']).first()
		shorts = user.shorts
		return render_template("mylinks.html", links=shorts,session=session)
	
	else:
		return redirect("/")


@app.route('/_about/')
def about():
	return render_template("about.html")

@app.route('/_contact/')
def contact():
	return render_template("contact.html")





