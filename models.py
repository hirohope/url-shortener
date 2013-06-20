from random import choice
import string
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Shortened(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	url = db.Column(db.String(256), unique=True)
	short = db.Column(db.String(64), unique=True)
	logs = db.relationship('Log', backref='shortened', lazy='dynamic')


	def __init__(self, url=None):
		self.url = url
		self.short = self.getShortURL(url)
		length = 3
		while Shortened.query.filter(Shortened.short==self.short).first() != None:
			self.short = self.getShortURL(url,length)
			if length < 6:
				length+=1

	def __repr__(self):
		return 'Shortened url %r %r %r' % (self.id, self.url, self.short)

	def getShortURL(self, url, length = 3):
		return ''.join(choice(string.lowercase+string.digits) for i in range(length))

class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, default=datetime.datetime.now)
	short_id = db.Column(db.Integer, db.ForeignKey('shortened.id'))

	def __init__(self, short=None):
		self.short_id = short.id

	def __repr__(self):
		return 'Log url %r %r %r' % (self.id, self.date, self.short_id)