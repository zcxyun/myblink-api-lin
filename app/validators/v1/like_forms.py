from lin.forms import Form
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange, AnyOf


class LikeForm(Form):
    art_id = IntegerField(validators=[DataRequired(message='点赞对象的ID不能为空'),
                                      NumberRange(min=1, message='点赞对象的ID必须为正整数')])
    type = IntegerField(validators=[DataRequired(message='点赞对象的类型不能为空'),
                                    AnyOf([100, 200, 300, 400], message='点赞类型不正确')])
