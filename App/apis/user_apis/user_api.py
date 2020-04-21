import random
import uuid

from flask import jsonify
from flask_restful import Resource, fields, abort, reqparse, marshal

from App.apis.api_constant import *
from App.ext import cache
from App.modeles.user import User
from App.apis.user_apis.user_utils import get_user, send_code

userFields = {
    "id":fields.Integer,
    "userName":fields.String,
    "addressCode":fields.String,
    "addressDefaultName":fields.String,
    "userPhoto":fields.String,
    "userIntroduction":fields.String,
    "phone":fields.String
}

singleUserFields = {
    "msg":fields.String,
    "status":fields.Integer,
    "data":fields.Nested(userFields),
    "token":fields.String
}



parseBase = reqparse.RequestParser()
parseBase.add_argument("phone", type=str, required=True, help="请输入手机号")
parseBase.add_argument("action", type=str, required=True, help="请确认请求参数")
parseBase.add_argument("ver_code", type=str, help="请输入验证码")
parseBase.add_argument("password", type=str, required=True, help="请输入密码")


parse_register = parseBase.copy()

parse_login = parseBase.copy()
parse_login.add_argument("username", type=str, help="请输入username")
parse_register.add_argument("phone", type=str, help="请输入手机号")


class UsersResource(Resource):

    def get(self):
        return {"msg":"ok"}

    def post(self):
        args = parseBase.parse_args()

        phone = args.get("phone")
        action = args.get("action").lower()
        ver_code = args.get("ver_code")

        if action == USER_ACTION_REGISTER:

            user = get_user(phone)
            if user:
                data={
                   "msg":"already phone register",
                   "status":USER_EXIST,
                   "data":user
                }
                return marshal(data,singleUserFields)

            if ver_code == cache.get(phone):
                password = args.get("password")
                user = User()
                user.userName = phone + str(random.randint(1,1000))
                user.phone = phone
                print(password)
                user.userpassword = password
                user.save()
                token = uuid.uuid4().hex
                cache.set(token,user.id,60*60*24*100)
                data = {
                    "msg":"user reginster success",
                    "status":REQUEST_OK,
                    "data":user,
                    "token":token
                }
                return marshal(data,singleUserFields)

        elif action == USER_ACTION_YZM:
            sendcode_resp = send_code(phone)
            result = sendcode_resp.json()
            if result.get("code") == SEND_CODE_OK:
                obj = result.get("obj")
                cache.set(phone,obj,60*60*24*100)
                data = {
                    "msg": "code send success",
                    "status": SEND_CODE_OK
                }
                return jsonify(data)
            data={
                "msg": "code send error",
                "status": SEND_CODE_ERROR
            }
            return jsonify(data)
        elif action == USER_ACTION_LOGIN:
            user = get_user(phone)
            if not user:
                data={
                   "msg":"user not exist",
                   "status":USER_NOT_EXIST,
                   "data":user
                }
                return marshal(data,singleUserFields)
            print(user,type(user))
            password = args.get("password")
            print(password)
            print(user.check_passwprd(password))
            if not user.check_passwprd(password):

                data = {
                    "msg": "password filed",
                    "status": REQUEST_NO,
                }
                return marshal(data, singleUserFields)
            token = uuid.uuid4().hex
            cache.set(token,user.id,60*60*24*100)
            data = {
                "msg":"user login success",
                "status":REQUEST_OK,
                "data":user,
                "token":token
            }
            return marshal(data,singleUserFields) 