from flask import jsonify
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.music import Music
from app.validators.cms.music_forms import MusicSearchForm, CreateOrUpdateMusicForm

music_api = Redprint('music')


@music_api.route('/<int:id>', methods=['GET'])
@login_required
def get_music(id):
    music = Music.get_detail(id)
    return jsonify(music)


@music_api.route('/', methods=['GET'])
@login_required
def get_musics():
    musics = Music.get_all()
    return jsonify(musics)


@music_api.route('/search', methods=['GET'])
@login_required
def search():
    form = MusicSearchForm().validate_for_api()
    musics = Music.search(form.q.data)
    return jsonify(musics)


@music_api.route('/', methods=['POST'])
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
