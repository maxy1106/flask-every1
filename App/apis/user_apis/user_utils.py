from flask_restful import abort

from App.ext import cache
from App.modeles.user import User


import hashlib
import time
import requests

def get_user(user_ident):
    """
    通过输入信息，获取user信息
    :param user_ident:
    :return:
    """

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
    user = User.query.filter(User.userName.__eq__(user_ident)).first()
    if user:
        return user

    #查不到
    return None



def send_code(phone):
    url = "https://api.netease.im/sms/sendcode.action"
    postdata = {
       "mobile":phone
    }

    nonce = hashlib.sha3_512(str(time.time()).encode("utf-8")).hexdigest()
    curtime = str(int(time.time()))
    secret = "518d9b487221"
    sha1 = hashlib.sha1()
    sha1.update((secret + nonce + curtime).encode("utf-8"))
    checkSum = sha1.hexdigest()
    header = {
        "AppKey":"aa0d4b4ecc2e576bbdea7a943746db04",
        "Nonce":nonce,
        "CurTime":curtime,
        "CheckSum":checkSum
    }
    resp = requests.post(url,postdata,headers=header)
    return resp

def check_token(token):
    if not token:
        abort(404,msg = "请输入正确许可后进行操作")
    user_id = cache.get(token)
    user = get_user(user_id)
    if not user:
        abort(404,msg = "用户未登录，请进行登录")

    return user