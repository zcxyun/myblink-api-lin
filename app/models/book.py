"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
import json

from lin import db
from lin.exception import ParameterException
from sqlalchemy import Column, String, Integer, or_

from app.libs.error_code import BookNotFound
from app.libs.spider import BookSpider
from app.libs.utils import is_isbn_or_key
from .base import Base
from app.app import cache


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False, unique=True, comment='书名(标题)')
    subtitle = Column(String(200), comment='子标题')
    _author = Column('author', String(200), default='未名', comment='书籍作者(多个以逗号分割)')
    summary = Column(String(1000), comment='书籍摘要')
    category = Column(String(30), comment='书籍分类')
    binding = Column(String(20), comment='装帧风格')
    publisher = Column(String(100), comment='出版社')
    price = Column(String(20), comment='价格')
    pages = Column(Integer, comment='页数')
    pubdate = Column(String(30), comment='出版时间')
    isbn = Column(String(15), nullable=False, unique=True)
    _translator = Column('translator', String(100), comment='翻译者(多个以逗号分割)')
    image = Column(String(100), comment='书籍封面来自外部链接')
    img_id = Column(Integer, default=0, comment='用户主动上传的图片id')

    @property
    def author(self):
        res = self._author if self._author else '[]'
        return json.loads(res)

    @author.setter
    def author(self, value):
        res = value if value else []
        self._author = json.dumps(res, ensure_ascii=False)

    @property
    def translator(self):
        res = self._translator if self._translator else '[]'
        return json.loads(res)

    @translator.setter
    def translator(self, value):
        res = value if value else []
        self._translator = json.dumps(res, ensure_ascii=False)

    @classmethod
    def get_book(cls, bid):
        book = cls.query.filter_by(id=bid, delete_time=None).first()
        if book is None:
            raise BookNotFound()
        return book

    @classmethod
    def get_books(cls, q='', start=0, count=15):
        """搜索图书, 搜索不到时从网上API寻找并存入数据库"""
        cache_total_key = q + '_total'  # 搜索结果(来自网络API)总数据缓存key
        search_key = '%{}%'.format(q)    # 搜索关键字
        data = {
            'start': start,
            'count': count,
            'total': 0,
            'books': None
        }
        statement = cls.query.filter_by(delete_time=None)
        if q:
            statement = statement.filter(or_(cls.title.ilike(search_key), cls._author.ilike(search_key)))
        books = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        total = statement.count()
        data['books'] = books
        data['total'] = total
        if not books and q:
            res = cls.get_books_from_api(q, start, count)
            cls.__new_books_from_api(res['books'])
            data['books'] = res['books']
            data['total'] = res['total']
            # 在第一次从网络API搜索时,就将结果总数据值缓存
            cache.set(cache_total_key, res['total'])
        # 搜索结果(来自网络API)总数据缓存value
        cache_total_value = cache.get(cache_total_key)
        # 前端搜索结果并切换页时如果网络api总数据缓存值有且大于数据库中相关总数据, 就将返回结果总数据置为网络API总数据,
        # 使得前端显示网络api总数据, 使得前端可以切换更多的页, 前端切换页时后端会先从数据库中寻找相关数据,
        # 找到就显示数据库中的数据, 否则会继续从网络API寻找数据并存入数据库, 最后返回搜索结果.
        if q and cache_total_value and cache_total_value > total:
            data['total'] = cache_total_value
        return data

    @classmethod
    def get_books_from_api(cls, q, start, count):
        search_type = is_isbn_or_key(q)
        if search_type == 'isbn':
            res = BookSpider.search_by_isbn(q)
        else:
            res = BookSpider.search_by_keyword(q, start, count)
        if not res['books']:
            raise BookNotFound()
        return res

    @classmethod
    def __new_books_from_api(cls, data):
        with db.auto_commit():
            for book_dict in data:
                book = Book()
                book.set_attrs(book_dict)
                if hasattr(book, 'summary'):
                    book.summary = cls._handle_new_line(book.summary)
                db.session.add(book)

    @classmethod
    def new_book(cls, form):
        book = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if book is not None:
            raise ParameterException(msg='图书已存在')

        Book.create(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            summary=form.summary.data,
            category=form.category.data,
            binding=form.binding.data,
            publisher=form.publisher.data,
            price=form.price.data,
            pages=form.pages.data,
            pubdate=form.pubdate.data,
            isbn=form.isbn.data,
            translator=form.translator.data,
            image=form.image.data,
            commit=True
        )
        return True

    @classmethod
    def edit_book(cls, bid, form):
        book = cls.query.filter_by(id=bid, delete_time=None).first()
        if book is None:
            raise BookNotFound()
        book.update(
            id=bid,
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            summary=form.summary.data,
            category=form.category.data,
            binding=form.binding.data,
            publisher=form.publisher.data,
            price=form.price.data,
            pages=form.pages.data,
            pubdate=form.pubdate.data,
            isbn=form.isbn.data,
            translator=form.translator.data,
            image=form.image.data,
            commit=True
        )
        return True

    @classmethod
    def remove_book(cls, bid):
        book = cls.query.filter_by(id=bid, delete_time=None).first()
        if book is None:
            raise BookNotFound()
        # 删除图书，软删除
        book.delete(commit=True)
        return True
