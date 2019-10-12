from sqlalchemy import Column, Integer, SmallInteger
from .base import Base


class MemberEpisode(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    episode_id = Column(Integer, comment='句子表id 外键')
    like_status = Column(SmallInteger, comment='是否点赞')

