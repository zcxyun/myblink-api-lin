from flask import jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import api_login_required, current_user
from app.validators.api_forms import MemberInfoForm

member_api = Redprint('member')


@member_api.route('/get', methods=['GET'])
@api_login_required
def get():
    member = current_user()
    return jsonify(member)


@member_api.route('/update', methods=['POST'])
@api_login_required
def update():
    form = MemberInfoForm().validate_for_api()
    member = current_user()
    member.update(
        nickName=form.nickName.data,
        avatarUrl=form.avatarUrl.data,
        _gender=form.gender.data,
        country=form.country.data,
        province=form.province.data,
        city=form.city.data,
        commit=True
    )
    return Success(msg='微信用户信息已更改')


