from flask import jsonify, request
from lin import login_required
from lin.exception import Success, NotFound
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.movie import Movie
from app.validators.cms.movie_forms import CreateOrUpdateMovieForm

movie_api = Redprint('movie')


@movie_api.route('/<int:id>', methods=['GET'])
@login_required
def get_movie(id):
    movie = Movie.get_model_with_img(id, err_msg='相关电影不存在')
    return jsonify(movie)


@movie_api.route('', methods=['GET'])
@login_required
def get_movies():
    start, count = paginate()
    q = request.args.get('q', None)
    movies = Movie.get_paginate_models_with_img(start, count, q, err_msg='相关电影不存在')
    return jsonify(movies)


@movie_api.route('', methods=['POST'])
@login_required
def create_movie():
    form = CreateOrUpdateMovieForm().validate_for_api()
    Movie.new_model(form.data, err_msg='相关电影已存在')
    return Success('电影创建成功')


@movie_api.route('/<int:id>', methods=['PUT'])
@login_required
def update_movie(id):
    form = CreateOrUpdateMovieForm().validate_for_api()
    Movie.edit_model(id, form.data, err_msg='相关电影不存在')
    return Success(msg='电影更新成功')


@movie_api.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_movie(id):
    Movie.remove_model(id, err_msg='相关电影不存在')
    return Success(msg='电影删除成功')
