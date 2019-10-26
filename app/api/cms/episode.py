from flask import jsonify, request
from lin import login_required
from lin.exception import Success, NotFound
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.episode import Episode
from app.validators.cms.episode_forms import CreateOrUpdateEpisodeForm, EpisodeSearchForm

episode_api = Redprint('episode')


@episode_api.route('/<bid>', methods=['GET'])
@login_required
def get_episode(bid):
    episode = Episode.get_model_with_img(bid, err_msg='相关句子不存在')
    return jsonify(episode)


@episode_api.route('', methods=['GET'])
@login_required
def get_episodes():
    start, count = paginate()
    q = request.args.get('q', None)
    episodes = Episode.get_paginate_models_with_img(start, count, q, err_msg='相关句子不存在')
    return jsonify(episodes)


@episode_api.route('', methods=['POST'])
@login_required
def create_episode():
    form = CreateOrUpdateEpisodeForm().validate_for_api()
    Episode.new_model(form.data, err_msg='相关句子已存在')
    return Success(msg='新建句子成功')


@episode_api.route('/<bid>', methods=['PUT'])
@login_required
def update_episode(bid):
    form = CreateOrUpdateEpisodeForm().validate_for_api()
    Episode.edit_model(bid, form.data, err_msg='相关句子不存在')
    return Success(msg='更新句子成功')


@episode_api.route('/<bid>', methods=['DELETE'])
@login_required
def delete_episode(bid):
    Episode.remove_model(bid, err_msg='相关句子不存在')
    return Success(msg='删除句子成功')
