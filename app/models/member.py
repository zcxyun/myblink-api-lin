from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer, SmallInteger

from app.libs.enum import GenderEnum, MemberActive
from app.libs.error_code import GenderStatusException


class Member(Base):
    id = Column(Integer, primary_key=True, comment='会员id')
    openid = Column(String(100), comment='微信用户openid')
    nickName = Column(String(30), nullable=False, comment='会员名')
    avatarUrl = Column(String(500), comment='会员头像')
    _gender = Column('gender', SmallInteger, comment='会员性别; 0, 未知 1, 男性 2, 女性')
    country = Column(String(30), comment='会员所在国家')
    province = Column(String(30), comment='会员所在省')
    city = Column(String(30), comment='会员所在市')
    active = Column(SmallInteger, default=1,
                    comment='当前用户是否为激活状态，非激活状态默认失去用户权限 ; 1 -> 激活 | 0 -> 非激活')

    def _set_fields(self):
        self._fields = ['nickName', 'avatarUrl', '_gender', 'country', 'province', 'city']

    @property
    def gender(self):
        try:
            status = GenderEnum(self._gender)
        except ValueError:
            raise GenderStatusException()
        return status

    def is_active(self):
        return self.active == MemberActive.ACTIVE.value
