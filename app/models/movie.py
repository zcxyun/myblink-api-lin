from lin.exception import ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String

from app.libs.error_code import MovieNotFound


class Movie(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, comment='电影标题')
    summary = Column(String(50), nullable=False, comment='电影简介')
    img_id = Column(Integer, comment='电影图片id 文件表外键')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary']

    @classmethod
    def get_detail(cls, id):
        movie = cls.query.filter_by(id=id, delete_time=None).first()
        if not movie:
            raise MovieNotFound()
        return movie

    @classmethod
    def get_all(cls):
        movies = cls.query.filter_by(delete_time=None).all()
        if not movies:
            raise MovieNotFound()
        return movies

    @classmethod
    def search(cls, q):
        movies = cls.query.filter(cls.title.ilike('%' + q + '%'), cls.delete_time == None).all()
        if not movies:
            raise MovieNotFound()
        return movies

    @classmethod
    def new_movie(cls, form):
        movie = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if movie:
            raise ParameterException(msg='图书已存在')
        cls.create(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.imgId.data,
            commit=True
        )
        return True

    @classmethod
    def edit_movie(cls, id, form):
        movie = cls.query.filter_by(id=id, delete_time=None).first()
        if not movie:
            raise MovieNotFound()
        movie.update(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.imgId.data,
            commit=True
        )
        return True

    @classmethod
    def remove_movie(cls, id):
        movie = cls.query.filter_by(id=id, delete_time=None).first()
        if not movie:
            raise MovieNotFound()
        movie.delete(commit=True)
        return True
