from flask_restful import Api
from app.controllers.book import BookList, Book
from app.main.errors import errors

# Flask API Configuration
api = Api(
    catch_all_404s=True,
    errors=errors,
    prefix='/api'
)

api.add_resource(BookList, '/books')
api.add_resource(Book, '/books/<int:id>')