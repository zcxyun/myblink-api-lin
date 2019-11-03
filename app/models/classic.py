from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, SmallInteger, func

from app.libs.enum import ClassicType, IsClassic
from app.models.episode import Episode
from app.models.like import Like
from app.models.movie import Movie
from app.models.music import Music
from .base import Base


class Classic(Base):
    index = Column(Integer, primary_key=True, comment='期刊号')
    classic_id = Column(Integer, comment='期刊在数据中序号，电影,音乐,句子的id 外键')
    type = Column(SmallInteger, comment='期刊类型,这里的类型分为: 100 电影 200 音乐 300 句子 400 书籍')

    def _set_fields(self):
        self._fields = ['index', 'type', 'classic_id']

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
    def get_latest(cls):
        """查询最近的期刊"""
        classic = cls.query.filter_by(delete_time=None).order_by(cls.index.desc()).first()
        if not classic:
            raise NotFound(msg='找不到指定期刊')
        res = cls._get_single_data(classic)
        return res

    @classmethod
    def get_next(cls, index):
        classic = cls.query.filter_by(index=(index+1), delete_time=None).first()
        if not classic:
            raise NotFound(msg='找不到指定期刊')
        res = cls._get_single_data(classic)
        return res

    @classmethod
    def get_previous(cls, index):
        classic = cls.query.filter_by(index=index-1, delete_time=None).first()
        if not classic:
            raise NotFound(msg='找不到指定期刊')
        res = cls._get_single_data(classic)
        return res

    @classmethod
    def get_detail(cls, type, id):
        classic = cls.query.filter_by(delete_time=None, type=type, classic_id=id).first()
        if not classic:
            raise NotFound(msg='找不到指定期刊')
        res = cls._get_single_data(classic)
        return res

    @classmethod
    def get_favor(cls, member_id, start, count):
        likes = Like.get_likes_by_member(member_id)
        movie_ids = []
        music_ids = []
        episode_ids = []
        if likes:
            movie_ids = [like.content_id for like in likes if like.type_enum == ClassicType.MOVIE]
            music_ids = [like.content_id for like in likes if like.type_enum == ClassicType.MUSIC]
            episode_ids = [like.content_id for like in likes if like.type_enum == ClassicType.EPISODE]
        classic_movies = cls.query.filter(
            cls.delete_time == None,
            cls.classic_id.in_(movie_ids),
            cls.type_enum == ClassicType.MOVIE
        ).all()
        classic_musics = cls.query.filter(
            cls.delete_time == None,
            cls.classic_id.in_(music_ids),
            cls.type_enum == ClassicType.MUSIC
        ).all()
        classic_episodes = cls.query.filter(
            cls.delete_time == None,
            cls.classic_id.in_(episode_ids),
            cls.type_enum == ClassicType.EPISODE
        ).all()
        classics = classic_movies + classic_musics + classic_episodes
        if not classics:
            raise NotFound(msg='还没有喜欢的期刊')
        data = cls._get_data(classics)
        return {
            'start': start,
            'count': count,
            'total': len(data),
            'models': data[start, start+count]
        }

    @classmethod
    def _get_single_data(cls, classic):
        model = cls._find_relate_model(classic)
        if not model:
            raise NotFound(msg='找不到和指定期刊关联的资源')
        fav_nums = Like.get_like_count_by_type(classic.type_enum, model.id)
        res = cls._combine_single_data(classic, model, fav_nums)
        return res

    @classmethod
    def _get_data(cls, classics):
        res = cls._find_relate_models(classics)
        movies = cls._combine_data(res['classic_movies'], res['movies'], res['movies_like_counts'])
        musics = cls._combine_data(res['classic_musics'], res['musics'], res['musics_like_counts'])
        episodes = cls._combine_data(res['classic_episodes'], res['episodes'], res['episodes_like_counts'])
        data = movies + musics + episodes
        if not data:
            raise NotFound(msg='期刊相关资源不存在')
        data.sort(key=lambda x: x.index, reverse=True)
        return data

    @classmethod
    def _find_relate_model(cls, classic):
        """根据指定的期刊查询相关联的资源"""
        if classic.type_enum == ClassicType.MOVIE:
            model = Movie.get_model_with_img(classic.classic_id)
        elif classic.type_enum == ClassicType.MUSIC:
            model = Music.get_model_with_img_voice(classic.classic_id)
        elif classic.type_enum == ClassicType.EPISODE:
            model = Episode.get_model_with_img(classic.classic_id)
        return model

    @classmethod
    def _find_relate_models(cls, classics):
        """查询多个期刊相关联的多个资源"""
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
        # 获取期刊相关的资源
        movies = Movie.get_models_by_ids_with_img(movie_ids)
        musics = Music.get_models_by_ids_with_img_voice(music_ids)
        episodes = Episode.get_models_by_ids_with_img(episode_ids)
        # 获取期刊相关资源点赞数量
        movies_like_counts = Like.get_like_counts_by_type(ClassicType.MOVIE, movie_ids)
        musics_like_counts = Like.get_like_counts_by_type(ClassicType.MUSIC, music_ids)
        episodes_like_counts = Like.get_like_counts_by_type(ClassicType.EPISODE, episode_ids)

        return {
            'classic_movies': classic_movies,
            'classic_musics': classic_musics,
            'classic_episodes': classic_episodes,
            'movies': movies,
            'musics': musics,
            'episodes': episodes,
            'movies_like_counts': movies_like_counts,
            'musics_like_counts': musics_like_counts,
            'episodes_like_counts': episodes_like_counts
        }

    @classmethod
    def get_paginate_models(cls, start, count, q=None, *, err_msg=None):
        """查询分页数据"""
        statement = cls.query
        total = statement.count()
        classics = statement.order_by(cls.index.desc()).offset(start).limit(count).all()
        if not classics:
            raise NotFound(msg='相关期刊不存在')
        data = cls._get_data(classics)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': data
        }

    @classmethod
    def _combine_single_data(cls, classic_model, model, fav_nums):
        """合并单个查询数据"""
        if classic_model.classic_id == model.id:
            model.fav_nums = fav_nums
            model.index = classic_model.index
            model.type = classic_model.type
            model.pubdate = classic_model._create_time.strftime('%Y-%m-%d')
            model._fields.extend(['index', 'type', 'pubdate', 'fav_nums'])
            return model
        return None

    @classmethod
    def _combine_data(cls, classic_models, models, models_like_counts):
        """合并多个查询数据"""
        for classic_model in classic_models:
            for model in models:
                for model_like_count in models_like_counts:
                    if classic_model.classic_id == model.id and model.id == model_like_count[0]:
                        cls._combine_single_data(classic_model, model, model_like_count[1])
        return models

    @classmethod
    def new_or_edit_classic(cls, data):
        """添加或插入期刊"""
        with db.auto_commit():
            classic = cls.query.filter_by(**data).first()
            if classic:
                if classic.delete_time is None:
                    raise ParameterException(msg='期刊已存在, 不能再加入')
                else:
                    classic.update(delete_time=None)
            else:
                classic = cls.create(**data)
            cls._update_is_classic(classic, IsClassic.YES.value)
        return True

    @classmethod
    def remove_classic(cls, data):
        """删除期刊"""
        with db.auto_commit():
            classic = cls.query.filter_by(**data).first()
            if classic:
                if classic.delete_time is None:
                    cls._update_is_classic(classic, IsClassic.NO.value)
                    classic.delete()
                else:
                    raise ParameterException(msg='期刊已删除, 不能再删除')
            else:
                raise NotFound(msg='相关期刊不存在')
        return True

    @classmethod
    def _update_is_classic(cls, classic, is_classic):
        """更新期刊相关资源的 is_classic 属性"""
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
