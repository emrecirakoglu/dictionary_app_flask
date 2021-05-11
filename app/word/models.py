from re import search
from sqlalchemy.orm import backref
from app import db

class Word(db.Model):
  __tablename__ = "word"
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 
  name = db.Column(db.String(80))
  definitions = db.relationship('Definition', backref='word', lazy=True)
  practising_point = db.Column(db.Integer, default=0)
  searched_count = db.Column(db.Integer, default=0)
  appeared_count = db.Column(db.Integer, default=0)

  def __init__(self, name, user):
    self.name = name
    self.user_id = user.id
 
  def __repr__(self):
    return f"{self.name}"

class Definition(db.Model):
  __tablename__ = "definition"
  id = db.Column(db.Integer, primary_key=True)
  word_id = db.Column(db.Integer, db.ForeignKey('word.id'))
  content = db.Column(db.String(512))

  def __repr__(self) -> str:
      return f"{self.content}"
