from flask import jsonify
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.classic import Classic
from app.validators.cms.classic_forms import CreateOrUpdateClassicForm

classic_api = Redprint('classic')


@classic_api.route('/<int:id>', methods=['GET'])
@login_required
def get_classic(id):
    classic = Classic.get_detail(id)
    return jsonify(classic)


@classic_api.route('/', methods=['GET'])
@login_required
def get_classics():
    classics = Classic.get_all()
    return jsonify(classics)


@classic_api.route('/', methods=['POST'])
@login_required
def create_classic():
    form = CreateOrUpdateClassicForm().validate_for_api()
    Classic.new_classic(form)
    return Success('期刊创建成功')


@classic_api.route('/<int:id>', methods=['PUT'])
@login_required
def update_classic(id):
    form = CreateOrUpdateClassicForm().validate_for_api()
    Classic.edit_classic(id, form)
    return Success(msg='期刊更新成功')


@classic_api.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_classic(id):
    Classic.remove_classic(id)
    return Success(msg='期刊删除成功')
