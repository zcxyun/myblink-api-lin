from sqlalchemy import Column, Integer, String, Boolean

from .base import Base


class Episode(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(30), nullable=False, unique=True, comment='句子标题')
    summary = Column(String(50), nullable=False, comment='句子摘要')
    img_id = Column(Integer, comment='句子图片id 文件表外键')
    is_classic = Column(Boolean, default=False, comment='是否已加入期刊')

    def _set_fields(self):
        self._fields = ['id', 'title', 'summary', 'is_classic']

    # @property
    # def is_classic_enum(self):
    #     """获得判断当前资源是否在期刊中的属性"""
    #     try:
    #         res = IsClassic(self._is_classic)
    #     except ValueError:
    #         return None
    #     return res
    #
    # @is_classic_enum.setter
    # def is_classic_enum(self, data):
    #     """设置判断当前资源是否在期刊中的属性"""
    #     if type(data) != IsClassic:
    #         raise ParameterException(msg='是否已加入期刊的类型不正确')
    #     self._is_classic = data.value
