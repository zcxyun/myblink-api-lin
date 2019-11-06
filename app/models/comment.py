from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, SmallInteger, String, func, text, desc

from app.libs.enum import ClassicType
from app.models.book import Book
from app.models.episode import Episode
from app.models.member import Member
from app.models.movie import Movie
from app.models.music import Music
from .base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    content_id = Column(Integer, comment='类型id 外键')
    type = Column(SmallInteger, comment='类型分为: 100 电影 200 音乐 300 句子 400 书籍')
    short_comment = Column(String(12), nullable=False, comment='短评内容')

    def _set_fields(self):
        self._exclude = ['update_time', 'delete_time']

    @property
    def type_enum(self):
        try:
            res = ClassicType(self.type)
        except ValueError:
            return None
        return res

    @type_enum.setter
    def type_enum(self, data):
        if type(data) != ClassicType:
            raise ParameterException(msg='期刊类型不正确')
        self.type = data.value

    @classmethod
    def get_comments_for_type_one(cls, classic_type, content_id, start=0, count=8):
        """分页显示某一期刊的短评分组统计数量, 按统计数量倒序排序"""
        cls.validate_classic_type(classic_type)
        comments = db.session.query(
            cls.short_comment.label('content'),
            func.count(cls.short_comment).label('nums')
        ).filter(
            cls.delete_time == None,
            cls.type == classic_type,
            cls.content_id == content_id
        ).group_by(
            cls.short_comment
        ).order_by(
            desc('nums')
        ).offset(start).limit(count).all()
        comments = [{'content': content, 'nums': nums} for content, nums in comments]
        return comments

    @classmethod
    def get_paginate_models(cls, start, count, classic_type=None, q=None, *, err_msg=None):
        if q:
            q = '%{}%'.format(q)
        if classic_type == ClassicType.MOVIE.value:
            statement = db.session.query(cls, Member, Movie.title).filter(cls.content_id == Movie.id)
            if q:
                statement = statement.filter(Movie.title.ilike(q))
        elif classic_type == ClassicType.MUSIC.value:
            statement = db.session.query(cls, Member, Music.title).filter(cls.content_id == Music.id)
            if q:
                statement = statement.filter(Music.title.ilike(q))
        elif classic_type == ClassicType.EPISODE.value:
            statement = db.session.query(cls, Member, Episode.title).filter(cls.content_id == Episode.id)
            if q:
                statement = statement.filter(Episode.title.ilike(q))
        elif classic_type == ClassicType.BOOK.value:
            statement = db.session.query(cls, Member, Book.title).filter(cls.content_id == Book.id)
            if q:
                statement = statement.filter(Book.title.ilike(q))
        else:
            raise ParameterException(msg='期刊类型不正确')
        statement = statement.filter(
            cls.member_id == Member.id,
            cls.delete_time == None
        )
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._combine_data(res)
        return {
            'total': total,
            'start': start,
            'count': count,
            'models': models
        }

    @classmethod
    def _combine_data(cls, res):
        models = []
        for comment, member, title in res:
            comment.nickName = member.nickName
            comment.avatarUrl = member.avatarUrl
            comment.title = title
            comment._fields.extend(['nickName', 'avatarUrl', 'title'])
            models.append(comment)
        return models


    @classmethod
    def new_model(cls, data, *, err_msg=None):
        """添加短评"""
        model = cls.query.filter_by(**data, delete_time=None).first()
        if model is not None:
            if err_msg is None:
                return False
            else:
                raise ParameterException(msg=err_msg)
        cls.create(**data, commit=True)
        return True
