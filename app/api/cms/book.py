from flask import jsonify, request
from lin import route_meta, group_required, login_required
from lin.exception import Success, NotFound
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.book import Book
from app.validators.cms.book_forms import CreateOrUpdateBookForm

book_api = Redprint('book')


@book_api.route('/<bid>', methods=['GET'])
@login_required
def get_book(bid):
    book = Book.get_model(bid, err_msg='相关书籍不存在')
    return jsonify(book)


@book_api.route('', methods=['GET'])
@login_required
def get_books():
    start, count = paginate()
    q = request.args.get('q', '')
    books = Book.get_books(q, start, count)
    return jsonify(books)


# @book_api.route('', methods=['POST'])
# @login_required
# def create_book():
#     form = CreateOrUpdateBookForm().validate_for_api()
#     Book.new_model(form.data, err_msg='相关书籍已存在')
#     return Success(msg='新建图书成功')


# @book_api.route('/<bid>', methods=['PUT'])
# @login_required
# def update_book(bid):
#     form = CreateOrUpdateBookForm().validate_for_api()
#     Book.edit_model(bid, form.data, err_msg='相关书籍不存在')
#     return Success(msg='更新图书成功')


# @book_api.route('/<bid>', methods=['DELETE'])
# @route_meta(auth='删除图书', module='图书')
# @group_required
# def delete_book(bid):
#     Book.remove_model(bid, err_msg='相关书籍不存在')
#     return Success(msg='删除图书成功')
