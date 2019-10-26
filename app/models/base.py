import os
import re

from flask import current_app
from lin import db
from lin.core import File
from lin.exception import ParameterException, NotFound
from lin.interface import InfoCrud

from app.libs.enum import IsClassic


class Base(InfoCrud):
    __abstract__ = True

    @property
    def is_classic(self):
        try:
            res = IsClassic(self._is_classic)
        except ValueError:
            return None
        return res

    @is_classic.setter
    def is_classic(self, data):
        if type(data) != IsClassic:
            raise ParameterException(msg='是否已加入期刊的类型不正确')
        self._is_classic = data.value

    @classmethod
    def get_model(cls, id, *, err_msg=None):
        model = cls.query.filter_by(id=id, delete_time=None).first()
        if not model:
            if err_msg is None:
                return None
            else:
                raise NotFound(msg=err_msg)
        return model

    @classmethod
    def get_paginate_models(cls, start, count, q=None, *, err_msg=None):
        statement = cls.query.filter_by(delete_time=None)
        if q:
            search_key = '%{}%'.format(q)
            statement = statement.filter(cls.title.ilike(search_key))
        total = statement.count()
        models = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not models:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_models_by_ids(cls, ids, *, err_msg=None):
        models = cls.query.filter(cls.id.in_(ids), cls.delete_time == None).all()
        if not models:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        return models

    @classmethod
    def get_model_with_img(cls, id, *, err_msg=None):
        model, img_relative_url, img_id = db.session.query(cls, File.path, File.id).filter(
            cls.img_id == File.id,
            cls.id == id,
            cls.delete_time == None
        ).first()
        if not model:
            if err_msg is None:
                return None
            else:
                raise NotFound(msg=err_msg)
        model.img_url = cls._get_file_url(img_relative_url)
        model.img_id = img_id
        model._fields.extend(['img_url', 'img_id'])
        return model

    @classmethod
    def get_paginate_models_with_img(cls, start, count, q=None, *, err_msg=None):
        statement = db.session.query(cls, File.path, File.id).filter(
            cls.img_id == File.id,
            cls.delete_time == None
        )
        if q:
            search_key = '%{}%'.format(q)
            statement = statement.filter(cls.title.ilike(search_key))
        total = statement.count()
        res = statement.order_by(cls.id.desc()).offset(start).limit(count).all()
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._add_img_to_models(res)
        return {
            'start': start,
            'count': count,
            'total': total,
            'models': models
        }

    @classmethod
    def get_models_by_ids_with_img(cls, ids, *, err_msg=None):
        res = db.session.query(cls, File.path, File.id).filter(
            cls.img_id == File.id,
            cls.id.in_(ids),
            cls.delete_time == None
        )
        if not res:
            if err_msg is None:
                return []
            else:
                raise NotFound(msg=err_msg)
        models = cls._add_img_to_models(res)
        return models

    @classmethod
    def _get_file_url(cls, file_relative_path):
        site_main = current_app.config.get('SITE_DOMAIN', 'http://127.0.0.1:5000')
        file_url = site_main + os.path.join(current_app.static_url_path, file_relative_path)
        return file_url

    @classmethod
    def _add_img_to_models(cls, data):
        res = []
        for model, img_relative_url, img_id in data:
            model.img_url = cls._get_file_url(img_relative_url)
            model.img_id = img_id
            model._fields.extend(['img_url', 'img_id'])
            res.append(model)
        return res

    @classmethod
    def new_model(cls, data, *, err_msg=None):
        if not data.get('title'):
            return False
        model = cls.query.filter_by(title=data.get('title'), delete_time=None).first()
        if model is not None:
            if err_msg is None:
                return False
            else:
                raise ParameterException(msg=err_msg)
        cls.create(**data, commit=True)
        return True

    @classmethod
    def edit_model(cls, id, data, *, err_msg=None):
        model = cls.query.filter_by(id=id, delete_time=None).first()
        if model is None:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        model.update(**data, commit=True)
        return True

    @classmethod
    def remove_model(cls, id, *, err_msg=None):
        model = cls.query.filter_by(id=id, delete_time=None).first()
        if model is None:
            if err_msg is None:
                return False
            else:
                raise NotFound(msg=err_msg)
        model.delete(commit=True)   # 软删除
        return True

    @classmethod
    def _get_total(cls, q=None):
        statement = cls.query.filter()
        if q:
            statement = cls.query.filter(cls.title.ilike('%' + q + '%'))
        total = statement.count()
        return total

    @classmethod
    def _handle_new_line(cls, text):
        return re.sub(r'\\n', '\\n       ', text) if type(text) == str else ''
