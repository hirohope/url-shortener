from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from myShortener.database import Base

from random import choice
import string, datetime

class Shortened(Base):
	__tablename__ = "shortened"
	id = Column(Integer, primary_key=True)
	url = Column(String(256), unique=True)
	short = Column(String(64), unique=True)
	logs = relationship('Log', backref='shortened', lazy='dynamic')


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

class Log(Base):
	__tablename__ = "log"
	id = Column(Integer, primary_key=True)
	date = Column(DateTime, default=datetime.datetime.now)
	short_id = Column(Integer, ForeignKey('shortened.id'))

	def __init__(self, short=None):
		self.short_id = short.id

	def __repr__(self):
		return 'Log url %r %r %r' % (self.id, self.date, self.short_id)