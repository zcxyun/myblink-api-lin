from lin.forms import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange, AnyOf


class CreateOrUpdateClassicForm(Form):
    classic_id = IntegerField(validators=[DataRequired(message='电影,音乐,句子的ID号不能为空'),
                                         NumberRange(min=1, message='ID必须为正整数')])
    type = IntegerField(validators=[DataRequired(message='期刊类型不能为空'),
                                  AnyOf([100, 200, 300], message='期刊类型只能是100, 200, 300')])

