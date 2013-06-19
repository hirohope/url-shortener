from sqlalchemy import Column, Integer, String
from database import Base
from random import choice
import string

class Shortened(Base):
    __tablename__ = 'shortens'
    id = Column(Integer, primary_key=True)
    url = Column(String(256), unique=True)
    short = Column(String(64), unique=True)

    def __init__(self, url=None):
        self.url = url
        self.short = self.getShortURL(url)

    def __repr__(self):
        return '<Shortened url %r %r>' % (self.url, self.short)

    def getShortURL(self, url):
    	length = 3
    	return ''.join(choice(string.lowercase) for i in range(length))

    