from flask import jsonify, request
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import paginate
from app.models.movie import Movie
from app.validators.cms.movie_forms import CreateOrUpdateMovieForm

movie_api = Redprint('movie')


@movie_api.route('/<int:id>', methods=['GET'])
@login_required
def get_movie(id):
    movie = Movie.get_movie(id)
    return jsonify(movie)


@movie_api.route('', methods=['GET'])
@login_required
def get_movies():
    start, count = paginate()
    q = request.args.get('q', None)
    movies = Movie.get_movies(q, start, count)
    return jsonify(movies)


@movie_api.route('', methods=['POST'])
@login_required
def create_movie():
    form = CreateOrUpdateMovieForm().validate_for_api()
    Movie.new_movie(form)
    return Success('电影创建成功')


@movie_api.route('/<int:id>', methods=['PUT'])
@login_required
def update_movie(id):
    form = CreateOrUpdateMovieForm().validate_for_api()
    Movie.edit_movie(id, form)
    return Success(msg='电影更新成功')


@movie_api.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_movie(id):
    Movie.remove_movie(id)
    return Success(msg='电影删除成功')
