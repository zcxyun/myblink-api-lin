"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

import time
import re
from flask import request, current_app

from lin.exception import ParameterException


def get_timestamp(fmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(fmt, time.localtime(time.time()))


def paginate():
    count = int(request.args.get('count', current_app.config.get('COUNT_DEFAULT', 1)))
    page = int(request.args.get('page', current_app.config.get('PAGE_DEFAULT', 1))) - 1
    count = 15 if count >= 15 else count
    start = page * count
    if start < 0 or count < 0:
        raise ParameterException()
    return start, count


def camel2line(camel: str):
    p = re.compile(r'([a-z]|\d)([A-Z])')
    line = re.sub(p, r'\1_\2', camel).lower()
    return line


def is_isbn_or_key(word):
    if len(word) == 13 and word.isdigit():
        return 'isbn'
    if '-' in word and len(word.replace('-', '')) == 10:
        # isbn10
        return 'isbn'
    return 'keyword'


def get_isbn(data_dict):
    isbn = data_dict.get('isbn')
    if not isbn:
        isbn = data_dict.get('isbn13')
        if not isbn:
            isbn = data_dict.get('isbn10')
    return isbn


