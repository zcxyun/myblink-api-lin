from lin import db
from lin.exception import ParameterException
from sqlalchemy import Column, Integer, SmallInteger, String, func, text, desc

from app.libs.enum import ClassicType
from .base import Base


class Comment(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    content_id = Column(Integer, comment='类型id 外键')
    type = Column(SmallInteger, comment='类型分为: 100 电影 200 音乐 300 句子 400 书籍')
    short_comment = Column(String(12), nullable=False, comment='短评内容')

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
    def get_comments_for_type(cls, classic_type, content_id, start=0, count=8):
        """分页显示某一期刊的短评分组统计数量, 按统计数量倒序排序"""
        cls.validate_classic_type(classic_type)
        comments = db.session.query(
            cls.short_comment.label('content'),
            func.count(cls.short_comment).label('nums')
        ).filter(
            cls.delete_time == None,
            cls.type == classic_type,
            cls.content_id == content_id
        ).group_by(
            cls.short_comment
        ).order_by(
            desc('nums')
        ).offset(start).limit(count).all()
        comments = [{'content': content, 'nums': nums} for content, nums in comments]
        return comments

    @classmethod
    def new_model(cls, data, *, err_msg=None):
        """添加短评"""
        model = cls.query.filter_by(**data, delete_time=None).first()
        if model is not None:
            if err_msg is None:
                return False
            else:
                raise ParameterException(msg=err_msg)
        cls.create(**data, commit=True)
        return True
