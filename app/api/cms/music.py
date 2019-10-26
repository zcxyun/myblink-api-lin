from flask import jsonify, request
from lin import login_required
from lin.exception import Success, NotFound
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.music import Music
from app.validators.cms.music_forms import CreateOrUpdateMusicForm

music_api = Redprint('music')


@music_api.route('/<int:id>', methods=['GET'])
@login_required
def get_music(id):
    music = Music.get_model_with_img_voice(id, err_msg='相关音乐不存在')
    return jsonify(music)


@music_api.route('', methods=['GET'])
@login_required
def get_musics():
    start, count = paginate()
    q = request.args.get('q', None)
    musics = Music.get_paginate_models_with_img_voice(start, count, q, err_msg='相关音乐不存在')
    return jsonify(musics)


@music_api.route('', methods=['POST'])
@login_required
def create_music():
    form = CreateOrUpdateMusicForm().validate_for_api()
    Music.new_model(form.data, err_msg='相关音乐已存在')
    return Success('音乐创建成功')


@music_api.route('/<int:id>', methods=['PUT'])
@login_required
def update_music(id):
    form = CreateOrUpdateMusicForm().validate_for_api()
    Music.edit_model(id, form.data, err_msg='相关音乐不存在')
    return Success(msg='音乐更新成功')


@music_api.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_music(id):
    Music.remove_model(id, err_msg='相关音乐不存在')
    return Success(msg='音乐删除成功')
