"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class GenderStatusException(APIException):
    code = 400
    msg = '会员性别状态错误'
    error_code = 20000


class WxCodeException(APIException):
    code = 400
    msg = '微信系统繁忙或code码无效'
    error_code = 90000
