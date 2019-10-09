from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.book import Book
from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm

book_api = Redprint('book')


@book_api.route('/<bid>', methods=['GET'])
@login_required
def get_book(bid):
    book = Book.get_detail(bid)
    return jsonify(book)


@book_api.route('/', methods=['GET'])
@login_required
def get_books():
    books = Book.get_all()
    return jsonify(books)


@book_api.route('/search', methods=['GET'])
@login_required
def search():
    form = BookSearchForm().validate_for_api()
    books = Book.search_by_keywords(form.q.data)
    return jsonify(books)


@book_api.route('/', methods=['POST'])
@login_required
def create_book():
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.new_book(form)
    return Success(msg='新建图书成功')


@book_api.route('/<bid>', methods=['PUT'])
@login_required
def update_book(bid):
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.edit_book(bid, form)
    return Success(msg='更新图书成功')


@book_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='删除图书', module='图书')
@group_required
def delete_book(bid):
    Book.remove_book(bid)
    return Success(msg='删除图书成功')
