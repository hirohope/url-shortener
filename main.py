import os
from flask import Flask, request, render_template, abort, redirect
from sqlite3 import dbapi2 as sqlite
from models import db, Shortened, Log


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)
db.app = app
db.create_all()

