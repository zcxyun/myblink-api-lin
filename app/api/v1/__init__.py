"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1.book import book_api
from app.api.v1.token import token_api
from app.api.v1.member import member_api


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    book_api.register(bp_v1)
    token_api.register(bp_v1)
    member_api.register(bp_v1)
    return bp_v1
