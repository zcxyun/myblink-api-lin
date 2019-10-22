from flask import current_app
from lin.interface import InfoCrud
import os, re


class Base(InfoCrud):
    __abstract__ = True

    @classmethod
    def _get_file_url(cls, file_relative_path):
        site_main = current_app.config.get('SITE_DOMAIN', 'http://127.0.0.1:5000')
        file_url = site_main + os.path.join(current_app.static_url_path, file_relative_path)
        return file_url

    @classmethod
    def _get_models_with_img(cls, data):
        res = []
        for model, img_relative_url, img_id in data:
            model.img_url = cls._get_file_url(img_relative_url)
            model.img_id = img_id
            model._fields.extend(['img_url', 'img_id'])
            res.append(model)
        return res

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
