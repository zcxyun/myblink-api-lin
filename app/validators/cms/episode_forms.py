from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class CreateOrUpdateEpisodeForm(Form):
    title = StringField(validators=[DataRequired(message='句子标题不能为空')])
    summary = StringField(validators=[DataRequired(message='句子摘要不能为空')])
    img_id = IntegerField(validators=[DataRequired(message='句子主图ID不能为空'),
                                     NumberRange(min=1, message='句子主图ID必须是正整数')])


class EpisodeSearchForm(Form):
    q = StringField(validators=[DataRequired(message='必须传入搜索关键字')])  # 前端的请求参数中必须携带`q`


# class EpisodePaginateForm(Form):
#     start = IntegerField(validators=[DataRequired(message='分页查询需要起始数据'),
#                                      NumberRange(min=1, message='分页查询起始数据必须为正整数')])
#     count = IntegerField(validators=[DataRequired(message='分页查询需要具体数目'),
#                                      AnyOf([10, 20, 30, 40], message='分页查询具体数目必须为10, 20, 30, 40')])
