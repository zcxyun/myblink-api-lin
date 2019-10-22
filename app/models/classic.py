from lin.exception import ParameterException
from sqlalchemy import Column, Integer, SmallInteger
from .base import Base

from app.libs.error_code import ClassicNotFound


class Classic(Base):
    index = Column(Integer, primary_key=True, comment='期号, 主键')
    classic_id = Column(Integer, comment='期刊在数据中序号，供点赞使用, 电影,音乐,句子的id 外键')
    type = Column(SmallInteger, comment='期刊类型,这里的类型分为: 100 电影 200 音乐 300 句子')

    def _set_fields(self):
        self._fields = ['index', 'type']

    # @classmethod
    # def get_classic(cls, index):
    #     classic = cls.query.filter_by(index=index, delete_time=None).first()
    #     if not classic:
    #         raise ClassicNotFound()
    #     return classic

    @classmethod
    def get_classics(cls, start=0, count=15):
        classics = cls.query.filter_by(delete_time=None).offset(start).limit(count).all()
        if not classics:
            raise ClassicNotFound()
        return classics

    @classmethod
    def new_classic(cls, form):
        classic = cls.query.filter_by(
            classic_id=form.classicId.data,
            type=form.type.data,
            delete_time=None
        ).first()
        if classic:
            raise ParameterException(msg='期刊已存在')
        cls.create(
            classic_id=form.classicId.data,
            type=form.type.data,
            commit=True
        )
        return True

    # @classmethod
    # def edit_classic(cls, index, form):
    #     classic = cls.query.filter_by(index=index, delete_time=None).first()
    #     if not classic:
    #         raise ClassicNotFound()
    #     classic.update(
    #         classic_id=form.classicId.data,
    #         type=form.type.data,
    #         commit=True
    #     )
    #     return True

    @classmethod
    def remove_classic(cls, index):
        classic = cls.query.filter_by(index=index, delete_time=None).first()
        if not classic:
            raise ClassicNotFound()
        classic.delete(commit=True)
        return True
