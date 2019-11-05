"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from pprint import pprint

from lin.core import Group, User, Auth
from lin.db import db
from sqlalchemy import func, text, desc

from app.app import create_app
from app.libs.enum import ClassicType
from app.models.book import Book
from app.models.classic import Classic
from app.models.episode import Episode
from app.models.movie import Movie
from app.models.music import Music

app = create_app()


# 管理员相关
def group():
    group = Group()
    group.name = '普通分组'
    group.info = '就是一个分组而已'
    db.session.add(group)
    db.session.flush()

    user = User()
    user.nickname = 'pedro'
    user.password = '123456'
    user.email = '123456780000@qq.com'
    db.session.add(user)

    auth = Auth()
    auth.auth = '删除图书'
    auth.module = '图书'
    auth.group_id = group.id
    db.session.add(auth)


# 句子相关
def delete_episodes():
    episodes = Episode.query.filter(Episode.delete_time != None).all()
    for episode in episodes:
        # episode.delete()
        episode.hard_delete()


# 音乐相关
def delete_musics():
    musics = Music.query.filter(Music.delete_time != None).all()
    for music in musics:
        music.update(
            delete_time=None
        )
        db.session.add(music)


# 电影相关
def delete_movies():
    movies = Movie.query.filter(Movie.delete_time != None).all()
    for movie in movies:
        movie.update(
            delete_time=None
        )
        db.session.add(movie)


def get_movies():
    pass


# 书籍相关
def delete_books():
    # q = ('%'+'韩寒'+'%').encode('utf-8')
    # books = Book.query.filter(or_(Book.title.ilike(q), Book._author.ilike(q))).all()
    books = Book.query.all()
    for book in books:
        book.hard_delete()
        # book.delete()


def get_books():
    start = 40
    count = 10
    books = Book.query.filter().offset(start).limit(count).all()
    pprint(books)


# 期刊相关
def get_classic():
    models = db.session.query(
        Classic.type, func.count(Classic.type).label('nums')
    ).group_by('type').order_by(desc('nums')).all()
    pprint(models)


with app.app_context():
    get_classic()
    with db.auto_commit():
        pass
