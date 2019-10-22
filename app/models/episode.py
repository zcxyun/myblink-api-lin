from lin import db
from lin.core import File
from lin.exception import ParameterException
from sqlalchemy import Column, Integer, String

from app.libs.error_code import EpisodeNotFound, FileNotFound
from .base import Base


class Episode(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True, comment='句子标题')
    summary = Column(String(50), nullable=False, comment='句子摘要')
    img_id = Column(Integer, comment='句子图片id 文件表外键')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary']

    @classmethod
    def get_episode(cls, id):
        episode, img_relative_url, img_id = db.session.query(Episode, File.path, File.id).filter(
            Episode.img_id == File.id,
            Episode.id == id,
            Episode.delete_time == None
        ).first()
        if episode is None:
            raise EpisodeNotFound()
        episode.img_url = cls._get_file_url(img_relative_url)
        episode.img_id = img_id
        episode._fields.extend(['img_url', 'img_id'])
        return episode

    @classmethod
    def get_episodes(cls, q='', start=0, count=15):
        search_key = '%{}%'.format(q)
        statement = db.session.query(Episode, File.path, File.id).filter(
            Episode.img_id == File.id,
            Episode.delete_time == None
        )
        if q:
            statement = statement.filter(Episode.title.ilike(search_key))
        total = statement.count()
        res = statement.order_by(Episode.id.desc()).offset(start).limit(count).all()
        if not res:
            raise EpisodeNotFound()
        episodes = cls._get_models_with_img(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'episodes': episodes
        }

    @classmethod
    def new_episode(cls, form):
        episode = cls.query.filter_by(title=form.title.data, delete_time=None).first()
        if episode is not None:
            raise ParameterException(msg='句子已存在')
        cls.create(
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            commit=True
        )
        return True

    @classmethod
    def edit_episode(cls, id, form):
        episode = cls.query.filter_by(id=id, delete_time=None).first()
        if episode is None:
            raise EpisodeNotFound(msg='没有找到相关句子')
        episode.update(
            id=id,
            title=form.title.data,
            summary=form.summary.data,
            img_id=form.img_id.data,
            commit=True
        )
        return True

    @classmethod
    def remove_episode(cls, id):
        episode = cls.query.filter_by(id=id, delete_time=None).first()
        if episode is None:
            raise EpisodeNotFound(msg='没有找到相关句子')
        # 删除图书，软删除
        episode.delete(commit=True)
        return True
