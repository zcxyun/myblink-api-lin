from lin.exception import Success
from lin.redprint import Redprint

from app.libs.jwt_api import get_current_member, member_login_required
from app.models.like import Like
from app.validators.v1.like_forms import LikeForm

like_api = Redprint('like')


@like_api.route('', methods=['POST'])
@member_login_required
def like():
    form = LikeForm().validate_for_api()
    member_id = get_current_member().id
    Like.like(form.type.data, form.art_id.data, member_id)
    return Success(msg='点赞成功')


@like_api.route('/cancel', methods=['POST'])
@member_login_required
def unlike():
    form = LikeForm().validate_for_api()
    member_id = get_current_member().id
    Like.unlike(form.type.data, form.art_id.data, member_id)
    return Success(msg='取消点赞成功')
