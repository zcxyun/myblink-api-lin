from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CreateOrUpdateBookForm(Form):
    title = StringField(validators=[DataRequired(message='必须传入书名')])
    subtitle = StringField(validators=[DataRequired(message='必须传入书名子标题')])
    author = FieldList(StringField(validators=[DataRequired(message='必须传入作者')]))
    summary = StringField(validators=[DataRequired(message='必须传入书籍摘要')])
    category = StringField(validators=[DataRequired(message='必须传入书籍种类')])
    binding = StringField(validators=[DataRequired(message='必须传入书籍装帧风格')])
    publisher = StringField(validators=[DataRequired(message='必须传入书籍出版社')])
    price = StringField(validators=[DataRequired(message='必须传入书籍价格')])
    pages = StringField(validators=[DataRequired(message='必须传入书籍页数')])
    pubdate = StringField(validators=[DataRequired(message='必须传入书籍出版时间')])
    isbn = StringField(validators=[DataRequired(message='必须传入书籍ISBN')])
    translator = FieldList(StringField(validators=[]), default='')
    img_id = IntegerField(validators=[DataRequired(message='必须传入书籍封面图片ID'),
                                      NumberRange(min=1, message='书籍封面图片ID必须为正整数')])
