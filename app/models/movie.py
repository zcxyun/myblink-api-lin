from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class Movie(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True, comment='电影标题')
    summary = Column(String(50), nullable=False, comment='电影摘要')
    img_id = Column(Integer, comment='电影图片id 文件表外键')
    _is_classic = Column('is_classic', Boolean, default=False, comment='是否已加入期刊')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary', '_is_classic']
