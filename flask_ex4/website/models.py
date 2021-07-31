from enum import unique
from . import db 

from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    
    posts = db.relationship('Post',backref=db.backref('author', lazy=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    title = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer,  db.ForeignKey('user.id'),nullable=False)
    
