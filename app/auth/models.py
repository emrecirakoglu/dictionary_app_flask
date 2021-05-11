from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))

    def __repr__(self) -> str:
      return f"{self.username}"