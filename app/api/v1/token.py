from flask import jsonify
from flask_jwt_extended import verify_jwt_refresh_token_in_request, get_jwt_identity, create_access_token, \
    create_refresh_token
from lin.exception import RefreshException, NotFound
from lin.redprint import Redprint

from app.libs.error_code import WxCodeException
from lin.jwt import get_tokens
from app.libs.wxhelper import WxHelper
from app.models.member import Member
from app.validators.api_forms import MemberLoginForm

token_api = Redprint('token')


@token_api.route('/refresh', methods=['GET'])
def refresh():
    try:
        verify_jwt_refresh_token_in_request()
    except Exception:
        return RefreshException()

    identity = get_jwt_identity()
    if identity:
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    return NotFound(msg='refresh_token未被识别')


@token_api.route('/get', methods=['POST'])
def get():
    form = MemberLoginForm().validate_for_api()
    openid = WxHelper.get_openid(form.code.data)
    if openid:
        member = Member.get(one=True, openid=openid)
        if not member:
            member = Member.create(
                openid=openid,
                nickName=form.nickName.data,
                avatarUrl=form.avatarUrl.data,
                _gender=form.gender.data,
                country=form.country.data,
                province=form.province.data,
                city=form.city.data,
                commit=True
            )
        access_token, refresh_token = get_tokens(member)
    else:
        raise WxCodeException()

    return jsonify({
        'accessToken': access_token,
        'refreshToken': refresh_token
    })
