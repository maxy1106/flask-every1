from datetime import datetime

from flask_restful import Resource, fields, reqparse, marshal

from App.apis.api_constant import *
from App.apis.article_apis.article_utils import get_article
from App.apis.user_apis.user_utils import check_token
from App.modeles.article_models import Article

articleFields = {
    "id":fields.Integer,
    "title":fields.String,
    "context":fields.String,
    "nickname":fields.String,
    "publishTime":fields.DateTime,
    "lastModifyTime":fields.DateTime,
    "isDelete":fields.Boolean,
    "authorId":fields.Integer
}

singleArticleFields = {
    "msg":fields.String,
    "status":fields.Integer,
    "data":fields.Nested(articleFields)
}

multiArticleFields = {
    "msg":fields.String,
    "status":fields.Integer,
    "data":fields.List(fields.Nested(articleFields))
}

parseBase = reqparse.RequestParser()
parseBase.add_argument("action",required=True,help="请输入正确请求")
parseBase.add_argument("token",help="请输入有效验证")

parseCreate = parseBase.copy()
parseCreate.add_argument("title",required=True,help="请输入标题")
parseCreate.add_argument("context",required=True,help="请输入文章内容")
parseCreate.add_argument("nickname",required=True,help="请输入正确类型")

parseModify = parseBase.copy()
parseModify.add_argument("id",required=True,help="请选择正确id")

parseSearchOne = reqparse.RequestParser()
parseSearchOne.add_argument("id",required=True,help="请选择正确id")

class ArticleResource(Resource):
    def post(self):
        args_base = parseBase.parse_args()
        action = args_base.get("action").lower()

        if action != ARTICLE_ACTION_SEARCH_ONE:
            token = args_base.get("token")
            user = check_token(token)
            print(user.id)
            if not user:

                data = {
                    "msg":"用户未登录，请登录",
                    "status":USER_NOT_LOGIN,
                    "data":user
                }
                return marshal(data,singleArticleFields)
            if action == ARTICLE_ACTION_CREATE:
                args_create = parseCreate.parse_args()
                title = args_create.get("title")
                context = args_create.get("context")
                nickname = args_create.get("nickname")
                article = Article()
                article.title = title
                article.context = context
                article.nickname = nickname
                article.publishTime = datetime.now()
                article.lastModifyTime = datetime.now()
                article.authorId = user.id
                article.save()
                data={
                    "msg":"新建文章成功",
                    "status":REQUEST_OK,
                    "data":article
                }
                return marshal(data,singleArticleFields)

            elif action == ARTICLE_ACTION_MODIFY:
                args_modify = parseModify.parse_args()
                articleId = args_modify.get("id")
                article = get_article(articleId)
                if not article:
                    data = {
                        "msg":"该文章不存在",
                        "stauts":ARTICLE_NOT_EXIST
                    }
                    return data
                args_create = parseCreate.parse_args()
                title = args_create.get("title")
                context = args_create.get("context")
                nickname = args_create.get("nickname")

                article.title = title
                article.context = context
                article.nickname = nickname
                article.authorId = user.id
                article.lastModifyTime = datetime.now()
                article.save()
                data={
                    "msg":"修改文章成功",
                    "status":REQUEST_OK,
                    "data":article
                }
                return marshal(data,singleArticleFields)


            elif action == ARTICLE_ACTION_DELETE:
                args_modify = parseModify.parse_args()
                articleId = args_modify.get("id")
                article = get_article(articleId)
                if not article:
                    data = {
                        "msg":"该文章不存在",
                        "stauts":ARTICLE_NOT_EXIST
                    }
                    return data
                article.isDelete = True
                article.save()
                data={
                    "msg":"删除文章成功",
                    "status":REQUEST_OK,
                }
                return data
        elif action == ARTICLE_ACTION_SEARCH_ONE:
            args_search_one = parseSearchOne.parse_args()
            articleId = args_search_one.get("id")
            article = get_article(articleId)
            if not article:
                data = {
                    "msg": "该文章不存在",
                    "stauts": ARTICLE_NOT_EXIST
                }
                return data
            data = {
                "msg": "查询文章成功",
                "status": REQUEST_OK,
                "data": article
            }
            return marshal(data, singleArticleFields)


class ArticlesResource(Resource):
    def post(self):
        pass
