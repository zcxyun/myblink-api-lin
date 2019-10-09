"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class BookNotFound(APIException):
    code = 404  # http状态码
    msg = '没有找到相关图书'  # 异常信息
    error_code = 80010  # 约定的异常码


class GenderStatusException(APIException):
    code = 400
    msg = '会员性别状态错误'
    error_code = 20000


class WxCodeException(APIException):
    code = 400
    msg = '微信系统繁忙或code码无效'
    error_code = 90000


class EpisodeNotFound(APIException):
    code = 404
    msg = '没有找到相关句子'
    error_code = 30010


class ClassicNotFound(APIException):
    code = 404
    msg = '没有找到相关期刊'
    error_code = 40010


class MovieNotFound(APIException):
    code = 404
    msg = '没有找到相关电影'
    error_code = 50010


class MusicNotFound(APIException):
    code = 404
    msg = '没有找到相关音乐'
    error_code = 60010


class FileNotFound(APIException):
    code = 404
    msg = '没有找到相关文件'
    error_code = 70010
