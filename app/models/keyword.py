from sqlalchemy import Column, Integer, String

from .base import Base


class Keyword(Base):
    id = Column(Integer, primary_key=True)
    key = Column(String(50), nullable=False, unique=True, comment='搜索关键字')
    count = Column(Integer, default=1, comment='搜索关键字次数')

    def _set_fields(self):
        pass

    @classmethod
    def get_hots(cls, amount=8):
        hots = cls.query.filter_by(delete_time=None).order_by(cls.count.desc()).limit(amount).all()
        return [hot.key for hot in hots]

    @classmethod
    def add(cls, q):
        model = cls.query.filter_by(key=q, delete_time=None).first()
        if not model:
            cls.create(key=q, commit=True)
            return True
        count = model.count + 1     # 搜索次数加1
        model.update(count=count, commit=True)
        return True
