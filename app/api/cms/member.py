from flask import request, jsonify
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.member import Member

member_api = Redprint('member')


@member_api.route('', methods=['GET'])
def get_members():
    start, count = paginate()
    q = request.args.get('q', None)
    members = Member.get_paginate_models(start, count, q, err_msg='相关会员不存在')
    return jsonify(members)
