from flask import jsonify
from lin.redprint import Redprint

from app.models.book import Book
from app.validators.forms import BookSearchForm

book_api = Redprint('book')


@book_api.route('/<bid>', methods=['GET'])
def get_book(bid):
    book = Book.get_detail(bid)
    return jsonify(book)


@book_api.route('/', methods=['GET'])
def get_books():
    books = Book.get_all()
    return jsonify(books)


@book_api.route('/search', methods=['GET'])
def search():
    form = BookSearchForm().validate_for_api()
    books = Book.search_by_keywords(form.q.data)
    return jsonify(books)

