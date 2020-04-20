from flask_restful import abort

from App.ext import cache
from App.modeles.user import User


def get_user(user_ident):

    if not user_ident:
        return None
    #根据id查找
    user = User.query.get(user_ident)
    if user:
        return user

    #根据phone 找
    user = User.query.filter(User.phone.__eq__(user_ident)).first()
    if user:
        return user

    #根据username
    user = User.query.filter(User.username.__eq__(user_ident)).first()
    if user:
        return user

    #查不到
    return None

def check_token(token):
    print(token,type(token))
    user_id = cache.get(token)
    print(user_id)
    user = get_user(user_id)
    print(user)
    if not user:
        abort(404,msg = "请输入有限验证")

    return True