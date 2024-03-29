from lin.exception import NotFound
from sqlalchemy import Column, String, Integer, SmallInteger
from .base import Base
from app.libs.enum import GenderEnum, MemberActive
from app.libs.error_code import GenderStatusException


class Member(Base):
    id = Column(Integer, primary_key=True, comment='会员id')
    openid = Column(String(100), comment='微信用户openid')
    nickName = Column(String(30), nullable=False, comment='会员名')
    avatarUrl = Column(String(500), comment='会员头像')
    gender = Column(SmallInteger, default=0, comment='会员性别; 0, 未知 1, 男性 2, 女性')
    country = Column(String(30), comment='会员所在国家')
    province = Column(String(30), comment='会员所在省')
    city = Column(String(30), comment='会员所在市')
    active = Column(SmallInteger, default=1,
                    comment='当前用户是否为激活状态，非激活状态默认失去用户权限 ; 1 -> 激活 | 0 -> 非激活')

    def _set_fields(self):
        self._fields = ['nickName', 'avatarUrl', 'gender', 'country', 'province', 'city']

    # @property
    # def gender_enum(self):
    #     try:
    #         status = GenderEnum(self._gender)
    #     except ValueError:
    #         raise GenderStatusException()
    #     return status

    def is_active(self):
        return self.active == MemberActive.ACTIVE.value

    @classmethod
    def get_paginate_models(cls, start, count, q=None, *, err_msg=None):
        """分页查询会员模型(支持搜索)"""
        statement = cls.query.filter_by(delete_time=None)
        if q:
            search_key = '%{}%'.format(q)
            statement = statement.filter(cls.nickName.ilike(search_key))
        total = statement.count()
        models = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not models:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }
