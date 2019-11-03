from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange, AnyOf, Length


class BookSummaryForm(Form):
    summary = StringField(validators=[AnyOf(['0', '1'], message='是否显示完整内容标示不正确, 只能是0或1')], default='0')


class NewBookShortComment(Form):
    book_id = IntegerField(validators=[DataRequired(message='必须传入书籍ID'),
                                       NumberRange(min=1, message='书籍ID必须为正整数')])
    content = StringField(validators=[DataRequired(message='必须传入短评内容'),
                                      Length(min=1, max=12, message='评论内容,我们可允许的评论内容范围为12字以内')])
