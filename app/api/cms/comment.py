from flask import request, jsonify
from lin.exception import ParameterException
from lin.redprint import Redprint
from app.libs.enum import ClassicType

from app.libs.utils import paginate
from app.models.comment import Comment

comment_api = Redprint('comment')


@comment_api.route('', methods=['GET'])
def get_comments():
    start, count = paginate()
    q = request.args.get('q', None)
    classic_type = int(request.args.get('type', None))
    if classic_type:
        validate_classic_type(classic_type)
    comments = Comment.get_paginate_models(start, count, classic_type, q, err_msg='相关评论不存在')
    return jsonify(comments)


def validate_classic_type(classic_type):
    """校验期刊类型"""
    try:
        _ = ClassicType(int(classic_type))
    except ValueError:
        raise ParameterException(msg='期刊类型不正确')
