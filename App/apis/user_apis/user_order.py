from flask_restful import Resource, reqparse

from App.ext import cache
from App.apis.user_apis.user_utils import get_user, check_token

parse =reqparse.RequestParser()
parse.add_argument("token",required=True,help="请输入有效验证")

class MovieUserOrderResource(Resource):

    def post(self):

        args = parse.parse_args()
        token = args.get("token")
        print(token)
        token_result = check_token(token)
        print(token_result)
        if token_result:
            return {"msg":"ok"}
        else:
            return {"msg":"no"}