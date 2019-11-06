from lin import db
from lin.exception import ParameterException, NotFound
from sqlalchemy import Column, Integer, Boolean, SmallInteger, func

from app.libs.enum import ClassicType
from .base import Base


class Like(Base):
    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, comment='会员id 外键')
    content_id = Column(Integer, comment='类型id 外键')
    type = Column(SmallInteger, comment='类型分为: 100 电影 200 音乐 300 句子 400 书籍')
    like_status = Column(Boolean, default=False, comment='是否点赞')

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
    def like(cls, classic_type, content_id, member_id):
        """点赞"""
        cls.validate_classic_type(classic_type)
        data = {
            'type': classic_type,
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
        cls.validate_classic_type(classic_type)
        data = {
            'type': classic_type,
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
    def get_like_counts_by_type(cls, classic_type, content_ids):
        """获取某一期刊类型以id为分组的点赞总数量"""
        cls.validate_classic_type(classic_type)
        res = db.session.query(cls.content_id, func.count(cls.content_id).label('like_count')).filter_by(
            delete_time=None,
            type=classic_type,
            like_status=True
        ).filter(cls.content_id.in_(content_ids)).group_by(cls.content_id).all()
        if not res:
            return [(content_id, 0) for content_id in content_ids]
        return res

    @classmethod
    def get_like_count_by_type(cls, classic_type, content_id):
        """获取某一期刊点赞的总数量"""
        cls.validate_classic_type(classic_type)
        total = cls.query.filter_by(
            delete_time=None,
            type=classic_type,
            like_status=True,
            content_id=content_id
        ).count()
        return total

    @classmethod
    def get_like_status_by_member(cls, member_id, classic_type, content_id):
        """获取某一会员某一期刊的点赞状态"""
        cls.validate_classic_type(classic_type)
        model = cls.query.filter_by(
            delete_time=None,
            type=classic_type,
            content_id=content_id,
            member_id=member_id
        ).first()
        return model.like_status if model else False

    @classmethod
    def get_likes_by_member(cls, member_id):
        """获取某一会员的所有点赞模型"""
        models = cls.query.filter_by(
            delete_time=None,
            member_id=member_id,
            like_status=True
        ).all()
        return models if models else []

    @classmethod
    def get_like_count_by_member_type(cls, member_id, classic_type):
        """获取某一会员某一期刊类型的点赞总数量"""
        cls.validate_classic_type(classic_type)
        like_count = cls.query.filter_by(
            delete_time=None,
            member_id=member_id,
            like_status=True,
            type=classic_type
        ).count()
        return like_count

    @classmethod
    def get_like(cls, classic_type, content_id, member_id):
        """获取某一会员某一期刊的点赞信息"""
        fav_nums = cls.get_like_count_by_type(classic_type, content_id)
        like_status = cls.get_like_status_by_member(member_id, classic_type, content_id)
        return {
            'fav_nums': fav_nums,
            'like_status': like_status,
            'id': content_id
        }
