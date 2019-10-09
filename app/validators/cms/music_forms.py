from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CreateOrUpdateMusicForm(Form):
    title = StringField(validators=[DataRequired(message='音乐标题不能为空')])
    summary = StringField(validators=[DataRequired(message='音乐简介不能为空')])
    imgId = IntegerField(validators=[DataRequired(message='音乐主图ID不能为空'),
                                     NumberRange(min=1, message='音乐主图ID必须是正整数')])
    urlId = IntegerField(validators=[DataRequired(message='音乐文件ID不能为空'),
                                     NumberRange(min=1, message='音乐文件ID必须是正整数')])


class MusicSearchForm(Form):
    q = StringField(validators=[DataRequired(message='必须传入搜索关键字')])  # 前端的请求参数中必须携带`q`
