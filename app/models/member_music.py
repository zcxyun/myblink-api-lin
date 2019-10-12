from sqlalchemy import Column, Integer, SmallInteger
from .base import Base


class MemberMusic(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    music_id = Column(Integer, comment='音乐表id 外键')
    like_status = Column(SmallInteger, comment='是否点赞')

