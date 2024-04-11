import unittest
import json
from app import app, db, Book

class TestBookAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_books.db'  # SQLite test database
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_post_book(self):
        data = {'title': 'Test Book', 'author': 'Test Author'}
        response = self.app.post('/books', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data), {'id': 1, 'title': 'Test Book', 'author': 'Test Author'})

    def test_get_all_books(self):
        book1 = Book(title='Book 1', author='Author 1')
        book2 = Book(title='Book 2', author='Author 2')
        db.session.add(book1)
        db.session.add(book2)
        db.session.commit()

        response = self.app.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), [{'id': 1, 'title': 'Book 1', 'author': 'Author 1'},
                                                      {'id': 2, 'title': 'Book 2', 'author': 'Author 2'}])

    def test_get_book_by_id(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'id': 1, 'title': 'Test Book', 'author': 'Test Author'})

    def test_update_book(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        data = {'title': 'Updated Book', 'author': 'Updated Author'}
        response = self.app.put('/books/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'id': 1, 'title': 'Updated Book', 'author': 'Updated Author'})

    def test_delete_book(self):
        book = Book(title='Test Book', author='Test Author')
        db.session.add(book)
        db.session.commit()

        response = self.app.delete('/books/1')
        self.assertEqual(response.status_code, 204)