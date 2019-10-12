from flask import jsonify, request
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.music import Music
from app.validators.cms.music_forms import CreateOrUpdateMusicForm

music_api = Redprint('music')


@music_api.route('/<int:id>', methods=['GET'])
@login_required
def get_music(id):
    music = Music.get_music(id)
    return jsonify(music)


@music_api.route('', methods=['GET'])
@login_required
def get_musics():
    start, count = paginate()
    q = request.args.get('q', None)
    musics = Music.get_musics(q, start, count)
    return jsonify(musics)


@music_api.route('', methods=['POST'])
@login_required
def create_music():
    form = CreateOrUpdateMusicForm().validate_for_api()
    Music.new_music(form)
    return Success('音乐创建成功')


@music_api.route('/<int:id>', methods=['PUT'])
@login_required
def update_music(id):
    form = CreateOrUpdateMusicForm().validate_for_api()
    Music.edit_music(id, form)
    return Success(msg='音乐更新成功')


@music_api.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_music(id):
    Music.remove_music(id)
    return Success(msg='音乐删除成功')
