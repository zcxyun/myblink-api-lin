from functools import wraps

from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from lin.exception import AuthFailed, NotFound

from app.models.member import Member


def member_login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        _check_is_active(get_current_member())
        return fn(*args, **kwargs)

    return wrapper


def get_current_member():
    identity = get_jwt_claims()
    if identity['scope'] != 'lin':
        raise AuthFailed()
    if 'remote_addr' in identity.keys() and identity['remote_addr'] != request.remote_addr:
        raise AuthFailed()
    # token is granted , user must be exit
    # 如果token已经被颁发，则该用户一定存在
    member = Member.get(id=identity['uid'], one=True)
    if member is None:
        raise NotFound(msg='会员不存在')
    return member


def _check_is_active(current_member):
    if not current_member.is_active:
        raise AuthFailed(msg='您目前处于未激活状态，请联系超级管理员')
