import uuid

from flask_restful import Resource, fields, abort, reqparse, marshal

from App.apis.api_constant import HTTP_CREATE_OK, USER_ACTION_REGISTER, USER_ACTION_LOGIN, HTTP_OK
from App.ext import cache
from App.modeles.user import User
from App.apis.user_apis.user_utils import get_user

user_fields = {
    "username": fields.String,
    "phone": fields.String
}

single_user_fields = {
    "status": fields.Integer,
    "msg": fields.String,
    "data": fields.Nested(user_fields)
}

parse_base = reqparse.RequestParser()
parse_base.add_argument("password", type=str, required=True, help="请输入密码")
parse_base.add_argument("action", type=str, required=True, help="请确认请求参数")

parse_register = parse_base.copy()
parse_register.add_argument("username", type=str, required=True, help="请输入username")
parse_register.add_argument("phone", type=str, required=True, help="请输入手机号")

parse_login = parse_base.copy()
parse_login.add_argument("username", type=str, help="请输入username")
parse_register.add_argument("phone", type=str, help="请输入手机号")


class MovieUsersResource(Resource):

    def post(self):
        args = parse_base.parse_args()
        password = args.get("password")
        action = args.get("action").lower()
        print("*************************************************************",action)

        if action == USER_ACTION_REGISTER:

            args_register = parse_register.parse_args()
            username = args_register.get("username")
            phone = args_register.get("phone")

            user_have = get_user(username) or get_user(phone)
            user = MovieUser()
            user.username = username
            user.password = password
            user.phone = phone

            if user_have:
                abort(400, msg="duplicate user")

            if not user.save():
                abort(400, msg="insert not success")

            data = {
                "status": HTTP_CREATE_OK,
                "msg": "insert success",
                "data": user
            }
            return marshal(data,single_user_fields)
        elif action == USER_ACTION_LOGIN:

            args_login = parse_login.parse_args()
            username = args_login.get("username")
            phone = args_login.get("phone")

            user = get_user(username) or get_user(phone)
            print(user)

            if not user:
                abort(400, msg="该用户不存在")

            if not user.check_password(password):
                abort(401, msg="用户名或密码错误，请重新输入")

            if user.is_delete:
                abort(401, msg="用户不存在")

            token = uuid.uuid4().hex
            print("************************** token", token,type(token))
            print("******************* user.id",user.id)
            cache.set(token, user.id, 60 * 60 * 24 * 7)

            data = {
                "status": HTTP_OK,
                "msg": "login success%s" %username,
                "token": token
            }
            return data
        else:
            abort(400, msg="请提供正确参数")


class MovieUserResource(Resource):
    def get(self, id):
        return {"msg": "user%d list" % id}
