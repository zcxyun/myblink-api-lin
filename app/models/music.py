from lin import db
from lin.core import File
from lin.exception import ParameterException
from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import aliased

from app.libs.error_code import MusicNotFound


class Music(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, comment='音乐标题')
    summary = Column(String(50), nullable=False, comment='音乐简介')
    img_id = Column(Integer, comment='音乐图片id 文件表外键')
    voice_id = Column(Integer, comment='音乐链接id 文件表外键')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary']

    @classmethod
    def get_music(cls, id):
        Image = aliased(File)
        Voice = aliased(File)
        music, img_relative_url, voice_relative_url, img_id, voice_id = db.session.query(
            Music, Image.path, Voice.path, Image.id, Voice.id).filter(
                Music.img_id == Image.id,
                Music.voice_id == Voice.id,
                Music.id == id,
                Music.delete_time == None
            ).first()
        if music is None:
            raise MusicNotFound()
        music.img_url = cls._get_file_url(img_relative_url)
        music.voice_url = cls._get_file_url(voice_relative_url)
        music.img_id = img_id
        music.voice_id = voice_id
        music._fields.extend(['img_url', 'img_id', 'voice_url', 'voice_id'])
        return music

    @classmethod
    def get_musics_with_img_voice(cls, data):
        res = []
        for model, img_relative_url, img_id, voice_relative_url, voice_id in data:
            model.img_url = cls._get_file_url(img_relative_url)
            model.img_id = img_id
            model.voice_url = cls._get_file_url(voice_relative_url)
            model.voice_id = voice_id
            model._fields.extend(['img_url', 'img_id', 'voice_url', 'voice_id'])
            res.append(model)
        return res

    @classmethod
    def get_musics(cls, q=None, start=0, count=15):
        Image = aliased(File)
        Voice = aliased(File)
        statement = db.session.query(Music, Image.path, Image.id, Voice.path, Voice.id).filter(
            Music.img_id == Image.id,
            Music.voice_id == Voice.id,
            Music.delete_time == None
        )
        if q:
            statement = statement.filter(Music.title.ilike('%' + q + '%'))
        total = statement.count()
        res = statement.offset(start).limit(count).all()
        if not res:
            raise MusicNotFound()
        musics = cls.get_musics_with_img_voice(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'musics': musics
        }

    @classmethod
    def new_music(cls, form):
        music = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if music is not None:
            raise ParameterException(msg='相关音乐已存在')
        cls.create(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            voice_id=form.voice_id.data,
            commit=True
        )
        return True

    @classmethod
    def edit_music(cls, id, form):
        music = cls.query.filter_by(id=id, delete_time=None).first()
        if music is None:
            raise MusicNotFound(msg='没有找到相关音乐')
        music.update(
            id=id,
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            voice_id=form.voice_id.data,
            commit=True
        )
        return True

    @classmethod
    def remove_music(cls, id):
        music = cls.query.filter_by(id=id, delete_time=None).first()
        if music is None:
            raise MusicNotFound(msg='没有找到相关音乐')
        # 删除图书，软删除
        music.delete(commit=True)
        return True
