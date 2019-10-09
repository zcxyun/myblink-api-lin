"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    from .book import book_api
    from .token import token_api
    from .member import member_api
    book_api.register(bp_v1)
    token_api.register(bp_v1)
    member_api.register(bp_v1)
    return bp_v1
