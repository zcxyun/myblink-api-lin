from lin import db
from lin.core import File
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import aliased

from .base import Base


class Music(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True, comment='音乐标题')
    summary = Column(String(50), nullable=False, comment='音乐摘要')
    img_id = Column(Integer, comment='音乐图片id 文件表外键')
    voice_id = Column(Integer, comment='音乐链接id 文件表外键')
    _is_classic = Column('is_classic', Boolean, default=False, comment='是否已加入期刊')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary', '_is_classic']

    @classmethod
    def get_model_with_img_voice(cls, id):
        Image = aliased(File)
        Voice = aliased(File)
        model, img_relative_url, voice_relative_url, img_id, voice_id = db.session.query(
            cls, Image.path, Voice.path, Image.id, Voice.id).filter(
                cls.img_id == Image.id,
                cls.voice_id == Voice.id,
                cls.id == id,
                cls.delete_time == None
            ).first()
        if model is None:
            return None
        model.img_url = cls._get_file_url(img_relative_url)
        model.voice_url = cls._get_file_url(voice_relative_url)
        model.img_id = img_id
        model.voice_id = voice_id
        model._fields.extend(['img_url', 'img_id', 'voice_url', 'voice_id'])
        return model

    @classmethod
    def get_paginate_models_with_img_voice(cls, start, count, q=None):
        Image = aliased(File)
        Voice = aliased(File)
        statement = db.session.query(cls, Image.path, Image.id, Voice.path, Voice.id).filter(
            cls.img_id == Image.id,
            cls.voice_id == Voice.id,
            cls.delete_time == None
        )
        if q:
            search_key = '%{}%'.format(q)
            statement = statement.filter(cls.title.ilike(search_key))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            return None
        models = cls._add_img_voice_to_model(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_models_by_ids_with_img_voice(cls, ids):
        Image = aliased(File)
        Voice = aliased(File)
        res = db.session.query(cls, Image.path, Image.id, Voice.path, Voice.id).filter(
            cls.img_id == Image.id,
            cls.voice_id == Voice.id,
            cls.id.in_(ids),
            cls.delete_time == None
        ).all()
        if not res:
            return None
        models = cls._add_img_voice_to_model(res)
        return models

    @classmethod
    def _add_img_voice_to_model(cls, data):
        res = []
        for model, img_relative_url, img_id, voice_relative_url, voice_id in data:
            model.img_url = cls._get_file_url(img_relative_url)
            model.img_id = img_id
            model.voice_url = cls._get_file_url(voice_relative_url)
            model.voice_id = voice_id
            model._fields.extend(['img_url', 'img_id', 'voice_url', 'voice_id'])
            res.append(model)
        return res
