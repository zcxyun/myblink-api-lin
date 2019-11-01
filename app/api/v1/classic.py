from flask import jsonify
from lin.redprint import Redprint

from app.libs.enum import ClassicType
from app.libs.jwt_api import member_login_required, get_current_member
from app.models.classic import Classic
from app.models.like import Like

classic_api = Redprint('classic')


@classic_api.route('/latest', methods=['GET'])
@member_login_required
def get_latest():
    classic = Classic.get_latest()
    classic_with_like_status(classic)
    return jsonify(classic)


@classic_api.route('/<int:index>/next', methods=['GET'])
@member_login_required
def get_next(index):
    classic = Classic.get_next(index)
    classic_with_like_status(classic)
    return jsonify(classic)


@classic_api.route('/<int:index>/previous', methods=['GET'])
@member_login_required
def get_previous(index):
    classic = Classic.get_previous(index)
    classic_with_like_status(classic)
    return jsonify(classic)


def classic_with_like_status(classic):
    classic_type = ClassicType(classic.type)
    like_status = Like.get_like_status_for_member(get_current_member().id, classic_type, classic.id)
    classic.like_status = like_status
    classic._fields.append('like_status')
