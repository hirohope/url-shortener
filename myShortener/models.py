from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship, backref
from myShortener.database import Base

from random import choice
import string, datetime

myShorts = Table('myShorts',
				Base.metadata,
				Column('short_id', Integer, ForeignKey('shortened.id')),
				Column('user_id', Integer, ForeignKey('user.id'))
			)

class Shortened(Base):
	__tablename__ = 'shortened'
	id = Column(Integer, primary_key=True)
	url = Column(String(256))
	short = Column(String(64), unique=True)
	custom = Column(Boolean, default=False)
	logs = relationship('Log', backref='shortened', lazy='dynamic')

	def __init__(self, url=None, short=None):
		self.url = url
		if short == None:
			self.short = self.getShortURL(url)
			length = 3
			while Shortened.query.filter(Shortened.short==self.short).first() != None:
				self.short = self.getShortURL(url,length)
				if length < 6:
					length+=1
		else:
			self.custom = True
			self.short = short

	def __repr__(self):
		return 'Shortened url %r %r %r %r' % (self.id, self.url, self.short, self.custom)

	def getShortURL(self, url, length = 3):
		return ''.join(choice(string.lowercase+string.digits) for i in range(length))

class Log(Base):
	__tablename__ = 'log'
	id = Column(Integer, primary_key=True)
	date = Column(DateTime, default=datetime.datetime.now)
	short_id = Column(Integer, ForeignKey('shortened.id'))

	def __init__(self, short=None):
		self.short_id = short.id

	def __repr__(self):
		return 'Log url %r %r %r' % (self.id, self.date, self.short_id)



class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	username = Column(String(256), unique=True)
	email = Column(String(256), unique=True)
	oauth_token_secret = Column(String(256))

	date = Column(DateTime, default=datetime.datetime.now)
	active = Column(Boolean, default=True)

	shorts = relationship('Shortened', secondary=myShorts, lazy='dynamic')

	def __init__(self, user_id, username, email, oauth_token_secret):
		self.id = user_id
		self.username = username
		self.email = email
		self.oauth_token_secret = oauth_token_secret

	def __repr__(self):
		return 'User %r %r %r %r %r' % (self.id, self.username, self.email, self.date, self.active)

class Profile(Base):
	__tablename__ = 'profile'
	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	oauth_token = Column(String(200)) 
	oauth_secret = Column(String(200))

	def __init__(self, user_id, oauth_token, oauth_secret):
		self.user_id = user_id
		self.oauth_token = oauth_token
		self.oauth_secret = oauth_secret

	def __repr__(self):
		return "Profile %r %r %r %r" % (self.id, self.user_id, self.oauth_token, self.oauth_secret)


