"""
    register api to admin blueprint
    ~~~~~~~~~
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint


def create_cms():
    cms = Blueprint('cms', __name__)
    from .admin import admin_api
    from .user import user_api
    from .log import log_api
    from .file import file_api
    from .test import test_api
    from .book import book_api
    from .movie import movie_api
    from .episode import episode_api
    from .music import music_api
    from .classic import classic_api
    admin_api.register(cms)
    user_api.register(cms)
    log_api.register(cms)
    file_api.register(cms)
    test_api.register(cms)
    book_api.register(cms)
    episode_api.register(cms)
    movie_api.register(cms)
    music_api.register(cms)
    classic_api.register(cms)
    return cms
