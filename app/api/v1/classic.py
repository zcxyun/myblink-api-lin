from flask import jsonify
from lin.redprint import Redprint

from app.libs.jwt_api import member_login_required, get_current_member
from app.libs.utils import offset_limit
from app.models.classic import Classic
from app.models.like import Like

classic_api = Redprint('classic')


@classic_api.route('/latest', methods=['GET'])
# # @member_login_required
def get_latest():
    classic = Classic.get_latest()
    # classic_with_like_status(classic)
    return jsonify(classic)


@classic_api.route('/<int:index>/next', methods=['GET'])
# @member_login_required
def get_next(index):
    classic = Classic.get_next(index)
    # classic_with_like_status(classic)
    return jsonify(classic)


@classic_api.route('/<int:index>/previous', methods=['GET'])
# @member_login_required
def get_previous(index):
    classic = Classic.get_previous(index)
    # classic_with_like_status(classic)
    return jsonify(classic)


@classic_api.route('/<int:type>/<int:id>')
# @member_login_required
def get_detail(type, id):
    classic = Classic.get_detail(type, id)
    return jsonify(classic)


@classic_api.route('/<int:type>/<int:id>/favor')
@member_login_required
def get_like(type, id):
    member_id = get_current_member().id
    like = Like.get_like(type, id, member_id)
    return jsonify(like)


@classic_api.route('/favor')
@member_login_required
def get_favor():
    start, count = offset_limit()
    member_id = get_current_member().id
    classic = Classic.get_favor(member_id, start, count)
    for model in classic['models']:
        model.like_status = True
        model._fields = ['id', 'type', 'summary', 'image', 'fav_nums', 'like_status']
    return jsonify(classic)


def classic_with_like_status(classic):
    like_status = Like.get_like_status_by_member(get_current_member().id, classic.type, classic.id)
    classic.like_status = like_status
    classic._fields.append('like_status')
