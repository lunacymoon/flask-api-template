from sqlalchemy import Integer, String

from app import db

class Book(db.Model):
    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(100), nullable=False)
    author = db.Column(String(100), nullable=False)

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author})"