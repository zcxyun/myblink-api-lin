from flask import jsonify
from lin import login_required
from lin.exception import Success, NotFound
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.classic import Classic
from app.validators.cms.classic_forms import CreateOrUpdateClassicForm

classic_api = Redprint('classic')


# @classic_api.route('/<int:id>', methods=['GET'])
# @login_required
# def get_classic(id):
#     classic = Classic.get_model(id, err_msg='相关期刊不存在')
#     return jsonify(classic)


@classic_api.route('', methods=['GET'])
@login_required
def get_classics():
    start, count = paginate()
    classics = Classic.get_paginate_models(start, count)
    if not classics:
        raise NotFound(msg='相关期刊不存在')
    return jsonify(classics)


# @classic_api.route('', methods=['POST'])
# @login_required
# def create_classic():
#     form = CreateOrUpdateClassicForm().validate_for_api()
#     Classic.new_classic(form)
#     return Success('期刊创建成功')


@classic_api.route('', methods=['POST'])
@login_required
def update_classic():
    form = CreateOrUpdateClassicForm().validate_for_api()
    Classic.new_or_edit_classic(form.data)
    return Success(msg='已加入期刊')


@classic_api.route('/cancel', methods=['POST'])
@login_required
def delete_classic():
    form = CreateOrUpdateClassicForm().validate_for_api()
    Classic.remove_classic(form.data)
    return Success(msg='已删除期刊')
