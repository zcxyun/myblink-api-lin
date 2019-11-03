from flask import jsonify, request
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.enum import ClassicType
from app.libs.jwt_api import get_current_member
from app.libs.utils import paginate
from app.models.book import Book
from app.models.comment import Comment
from app.models.keyword import Keyword
from app.models.like import Like
from app.validators.v1.book_forms import BookSummaryForm, NewBookShortComment

book_api = Redprint('book')


@book_api.route('/<int:id>/detail', methods=['GET'])
def get_book(id):
    book = Book.get_model(id)
    return jsonify(book)


@book_api.route('/hot_list', methods=['GET'])
def get_hot_list():
    start, count = paginate()
    books = Book.get_paginate_models(start, count, err_msg='相关书籍不存在')
    for book in books['models']:
        book._fields = ['author', 'id', 'image', 'title']
    return jsonify(books)


@book_api.route('/search', methods=['GET'])
def search():
    form = BookSummaryForm().validate_for_api()
    start, count = paginate()
    q = request.args.get('q', None)
    books = Book.get_paginate_models(start, count, q, err_msg='相关书籍不存在')
    # 搜索关键字次数加1
    Keyword.add(q)
    if form.summary.data == '1':
        for book in books['models']:
            book._fields = ['author', 'id', 'image', 'isbn', 'price', 'title']
    return jsonify(books)


@book_api.route('/hot_keyword', methods=['GET'])
def get_hot_keyword():
    hots = Keyword.get_hots()
    return jsonify(hots)


@book_api.route('/<int:book_id>/short_comment', methods=['GET'])
def get_short_comment(book_id):
    comment = Comment.get_comments_for_type(ClassicType.BOOK.value, book_id)
    return jsonify({
        'book_id': book_id,
        'comment': comment
    })


@book_api.route('/favor/count', methods=['GET'])
def get_favor_count():
    # member_id = get_current_member().id
    fav_nums = Like.get_like_count_by_member_type(1, ClassicType.BOOK.value)
    return jsonify({'count': fav_nums})


@book_api.route('/<int:book_id>/favor', methods=['GET'])
def get_favor(book_id):
    # member_id = get_current_member().id
    like = Like.get_like(ClassicType.BOOK.value, book_id, 1)
    return jsonify(like)


@book_api.route('/add/short_comment', methods=['POST'])
def create_short_comment():
    form = NewBookShortComment().validate_for_api()
    # member_id = get_current_member().id
    data = {
        'member_id': 1,
        'type': ClassicType.BOOK.value,
        'content_id': form.book_id.data,
        'short_comment': form.content.data
    }
    Comment.new_model(data, err_msg='相关短评已存在')
    return Success(msg='输入短评成功')
