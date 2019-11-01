from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, Boolean, SmallInteger, func

from app.libs.enum import ClassicType
from .base import Base


class Like(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    content_id = Column(Integer, comment='点赞类型表id 外键')
    type = Column(SmallInteger, comment='点赞类型,这里的类型分为: 100 电影 200 音乐 300 句子')
    like_status = Column(Boolean, default=False, comment='是否点赞')

    @classmethod
    def like(cls, classic_type, content_id, member_id):
        """点赞"""
        cls._validate_classic_type(classic_type)
        data = {
            'type': classic_type.value,
            'content_id': content_id,
            'member_id': member_id
        }
        model = cls.query.filter_by(**data).first()
        if model:
            if model.delete_time is None:
                if model.like_status is True:
                    raise ParameterException(msg='对不起, 已经点过赞了, 不能再点了')
                else:
                    model.update(like_status=True, commit=True)
            else:
                model.update(delete_time=None, like_status=True, commit=True)
        else:
            cls.create(**data, like_status=True, commit=True)
        return True

    @classmethod
    def unlike(cls, classic_type, content_id, member_id):
        """取消点赞"""
        cls._validate_classic_type(classic_type)
        data = {
            'type': classic_type.value,
            'content_id': content_id,
            'member_id': member_id
        }
        model = cls.query.filter_by(**data).first()
        if model:
            if model.delete_time is None:
                if model.like_status is False:
                    raise ParameterException(msg='对不起, 已经取消过点赞了, 不能再取消了')
                else:
                    model.update(like_status=False, commit=True)
            else:
                model.update(delete_time=None, like_status=False, commit=True)
        else:
            cls.create(**data, like_status=False, commit=True)
        return True

    @classmethod
    def get_like_counts_for_types(cls, classic_type, content_ids):
        """获取某一期刊类型点赞的总数量"""
        cls._validate_classic_type(classic_type)
        res = db.session.query(cls.content_id, func.count(cls.content_id).label('like_count')).filter_by(
            delete_time=None,
            type=classic_type.value,
            like_status=True
        ).filter(cls.content_id.in_(content_ids)).group_by(cls.content_id).all()
        if not res:
            return [(content_id, 0) for content_id in content_ids]
        return res

    @classmethod
    def get_like_count_for_type(cls, classic_type, content_id):
        """获取某一期刊点赞的总数量"""
        cls._validate_classic_type(classic_type)
        total = cls.query.filter_by(
            delete_time=None,
            type=classic_type.value,
            like_status=True,
            content_id=content_id
        ).count()
        return total

    @classmethod
    def get_like_status_for_member(cls, member_id, classic_type, content_id):
        """获取某一会员点赞状态"""
        cls._validate_classic_type(classic_type)
        model = cls.query.filter_by(
            delete_time=None,
            type=classic_type.value,
            content_id=content_id,
            member_id=member_id
        ).first()
        return model.like_status if model else False

    @classmethod
    def _validate_classic_type(cls, classic_type):
        """校验期刊类型"""
        if type(classic_type) != ClassicType:
            raise ParameterException(msg='要点赞的表类型不正确')
