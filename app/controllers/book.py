from flask import request
from flask_restful import Resource
from pydantic import ValidationError
from app.serializers.book import BookSchema
from app import db

class BookList(Resource):
    def get(self):
        books = Book.query.all()
        return [BookSchema.from_orm(book).dict() for book in books]

# Resource to manipulate a single book
class Book(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if book:
            return BookSchema.from_orm(book).dict()
        else:
            return {"error": "Book not found"}, 404

    def post(self):
        try:
            book = BookSchema(**request.json)
            new_book = Book(title=book.title, author=book.author)
            db.session.add(new_book)
            db.session.commit()
            return BookSchema.from_orm(new_book).dict(), 201
        except ValidationError as e:
            return {"error": str(e)}, 400

    def put(self, id):
        book = Book.query.get(id)
        if book:
            try:
                updated_book = BookSchema(**request.json)
                book.title = updated_book.title
                book.author = updated_book.author
                db.session.commit()
                return BookSchema.from_orm(book).dict()
            except ValidationError as e:
                return {"error": str(e)}, 400
        else:
            return {"error": "Book not found"}, 404

    def delete(self, id):
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return '', 204
        else:
            return {"error": "Book not found"}, 404