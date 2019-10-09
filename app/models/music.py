from lin.exception import ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String

from app.libs.error_code import MusicNotFound


class Music(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, comment='音乐标题')
    summary = Column(String(50), nullable=False, comment='音乐简介')
    img_id = Column(Integer, comment='音乐图片id 文件表外键')
    url_id = Column(Integer, comment='音乐链接id 文件表外键')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary']

    @classmethod
    def get_detail(cls, id):
        music = cls.query.filter_by(id=id, delete_time=None).first()
        if not music:
            raise MusicNotFound()
        return music

    @classmethod
    def get_all(cls):
        musics = cls.query.filter_by(delete_time=None).all()
        if not musics:
            raise MusicNotFound()
        return musics

    @classmethod
    def search(cls, q):
        musics = cls.query.filter(cls.title.ilike('%' + q + '%'), cls.delete_time == None).all()
        if not musics:
            raise MusicNotFound()
        return musics

    @classmethod
    def new_music(cls, form):
        music = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if music:
            raise ParameterException(msg='音乐已存在')
        cls.create(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.imgId.data,
            url_id=form.urlId.data,
            commit=True
        )
        return True

    @classmethod
    def edit_music(cls, id, form):
        music = cls.query.filter_by(id=id, delete_time=None).first()
        if not music:
            raise MusicNotFound()
        music.update(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.imgId.data,
            url_id=form.urlId.data,
            commit=True
        )
        return True

    @classmethod
    def remove_music(cls, id):
        music = cls.query.filter_by(id=id, delete_time=None).first()
        if not music:
            raise MusicNotFound()
        music.delete(commit=True)
        return True
