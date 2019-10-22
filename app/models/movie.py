from lin import db
from lin.core import File
from lin.exception import ParameterException
from .base import Base
from sqlalchemy import Column, Integer, String

from app.libs.error_code import MovieNotFound


class Movie(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True, comment='电影标题')
    summary = Column(String(50), nullable=False, comment='电影摘要')
    img_id = Column(Integer, comment='电影图片id 文件表外键')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary']

    @classmethod
    def get_movie(cls, id):
        movie, img_relative_url, img_id = db.session.query(Movie, File.path, File.id).filter(
            Movie.img_id == File.id,
            Movie.id == id,
            Movie.delete_time == None
        ).first()
        if movie is None:
            raise MovieNotFound()
        movie.img_url = cls._get_file_url(img_relative_url)
        movie.img_id = img_id
        movie._fields.extend(['img_url', 'img_id'])
        return movie

    @classmethod
    def get_movies(cls, q='', start=0, count=15):
        search_key = '%{}%'.format(q)
        statement = db.session.query(Movie, File.path, File.id).filter(
            Movie.img_id == File.id,
            Movie.delete_time == None
        )
        if q:
            statement = statement.filter(Movie.title.ilike(search_key))
        total = statement.count()
        res = statement.order_by(Movie.id.desc()).offset(start).limit(count).all()
        if not res:
            raise MovieNotFound()
        movies = cls._get_models_with_img(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'movies': movies
        }

    @classmethod
    def new_movie(cls, form):
        movie = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if movie is not None:
            raise ParameterException(msg='电影已存在')
        cls.create(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            commit=True
        )
        return True

    @classmethod
    def edit_movie(cls, id, form):
        movie = cls.query.filter_by(id=id, delete_time=None).first()
        if movie is None:
            raise MovieNotFound(msg='没有找到相关电影')
        movie.update(
            id=id,
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            commit=True
        )
        return True

    @classmethod
    def remove_movie(cls, id):
        movie = cls.query.filter_by(id=id, delete_time=None).first()
        if movie is None:
            raise MovieNotFound(msg='没有找到相关电影')
        # 删除图书，软删除
        movie.delete(commit=True)
        return True
