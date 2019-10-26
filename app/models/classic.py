from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, SmallInteger

from app.libs.enum import ClassicType, IsClassic
from app.models.episode import Episode
from app.models.movie import Movie
from app.models.music import Music
from .base import Base


class Classic(Base):
    index = Column(Integer, primary_key=True, comment='期刊号')
    classic_id = Column(Integer, comment='期刊在数据中序号，电影,音乐,句子的id 外键')
    type = Column(SmallInteger, comment='期刊类型,这里的类型分为: 100 电影 200 音乐 300 句子')

    def _set_fields(self):
        self._fields = ['index', '_type', 'classic_id']

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
    def get_paginate_models(cls, start, count, q=None, *, err_msg=None):
        statement = cls.query
        total = statement.count()
        classics = statement.order_by(cls.index.desc()).offset(start).limit(count).all()
        if not classics:
            raise NotFound(msg='相关期刊不存在')
        movie_ids = []
        music_ids = []
        episode_ids = []
        classic_movies = []
        classic_musics = []
        classic_episodes = []
        for classic in classics:
            if classic.type_enum == ClassicType.MOVIE:
                movie_ids.append(classic.classic_id)
                classic_movies.append(classic)
            elif classic.type_enum == ClassicType.MUSIC:
                music_ids.append(classic.classic_id)
                classic_musics.append(classic)
            elif classic.type_enum == ClassicType.EPISODE:
                episode_ids.append(classic.classic_id)
                classic_episodes.append(classic)

        movies = Movie.get_models_by_ids_with_img(movie_ids)
        episodes = Episode.get_models_by_ids_with_img(episode_ids)
        musics = Music.get_models_by_ids_with_img(music_ids)

        movies = cls._combine_data(classic_movies, movies)
        musics = cls._combine_data(classic_musics, musics)
        episodes = cls._combine_data(classic_episodes, episodes)
        data = movies + musics + episodes
        if not data:
            raise NotFound(msg='期刊原数据不存在')
        data.sort(key=lambda x: x.index, reverse=True)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': data
        }

    @classmethod
    def _combine_data(cls, classic_models, models):
        for classic_model in classic_models:
            for model in models:
                if classic_model.classic_id == model.id:
                    model.index = classic_model.index
                    model.type = classic_model.type
                    model._fields.extend(['index', 'type'])
        return models

    @classmethod
    def new_or_edit_classic(cls, data):
        with db.auto_commit():
            classic = cls.query.filter_by(**data).filter(cls.delete_time != None).first()
            if classic:
                classic.update(delete_time=None)
            else:
                classic = cls.create(**data)
            cls._update_is_classic(classic, IsClassic.YES)
        return True

    @classmethod
    def remove_classic(cls, data):
        with db.auto_commit():
            classic = cls.query.filter_by(**data, delete_time=None).first()
            if not classic:
                raise NotFound(msg='相关期刊不存在')
            cls._update_is_classic(classic, IsClassic.NO)
            classic.delete()
        return True

    @classmethod
    def _update_is_classic(cls, classic, is_classic):
        if classic.type_enum == ClassicType.MOVIE:
            movie = Movie.get_model(id=classic.classic_id)
            if not movie:
                raise NotFound(msg='相关电影不存在')
            movie.update(is_classic=is_classic)
        elif classic.type_enum == ClassicType.MUSIC:
            music = Music.get_model(id=classic.classic_id)
            if not music:
                raise NotFound(msg='相关音乐不存在')
            music.update(is_classic=is_classic)
        elif classic.type_enum == ClassicType.EPISODE:
            episode = Episode.get_model(id=classic.classic_id)
            if not episode:
                raise NotFound(msg='相关句子不存在')
            episode.update(is_classic=is_classic)
