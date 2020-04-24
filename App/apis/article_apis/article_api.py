from datetime import datetime
from copy import copy
from flask_restful import Resource, fields, reqparse, marshal

from App.apis.api_constant import *
from App.apis.article_apis.article_utils import get_article
from App.apis.user_apis.user_utils import check_token
from App.modeles.article_models import Article
from App.modeles.article_models.article_model import Category

articleFields = {
    "id":fields.Integer,
    "title":fields.String,
    "context":fields.String,
    "cateId":fields.String,
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


categoryFields = {
    "id":fields.Integer,
    "name":fields.String,
    "desc":fields.String,
    "category_type":fields.String,
    "partent_cateory":fields.String,
    "is_tab":fields.Boolean,
    "add_time":fields.DateTime,
    "models":fields.List(fields.Nested(1))
}

multiCategoryFields = {
    "models":fields.List(fields.Nested(categoryFields))
}

multisCategoryFields = {
    "msg":fields.String,
    "status":fields.String,
    "categorys":fields.List(fields.Nested(categoryFields))
}



parseBase = reqparse.RequestParser()
parseBase.add_argument("action",required=True,help="请输入正确请求")

parseCreate = parseBase.copy()
parseCreate.add_argument("token",help="请输入有效验证")
parseCreate.add_argument("title",required=True,help="请输入标题")
parseCreate.add_argument("context",required=True,help="请输入文章内容")
parseCreate.add_argument("cateId",required=True,help="请输入正确类型")
parseCreate.add_argument("titlePic",help="请输入正确类型")


parseModify = parseBase.copy()
parseBase.add_argument("token",help="请输入有效验证")
parseModify.add_argument("id",required=True,help="请选择正确id")

parseSearchOne = parseBase.copy()
parseSearchOne.add_argument("id",required=True,help="请选择正确id")

class ArticleResource(Resource):
    def post(self):
        args_base = parseBase.parse_args()
        action = args_base.get("action").lower()

        if action != ARTICLE_ACTION_SEARCH_ONE:
            args_create = parseCreate.parse_args()
            token = args_create.get("token")
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
                cateId = args_create.get("cateId")
                article = Article()
                article.title = title
                article.context = context
                article.cateId = cateId
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
                cateId = args_create.get("nickname")

                article.title = title
                article.context = context
                article.cateId = cateId
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
            article.fontReadNo = article.fontReadNo + 1
            if article.save():
                data = {
                    "msg": "查询文章成功",
                    "status": REQUEST_OK,
                    "data": article
                }
                return marshal(data, singleArticleFields)
            else:
                data = {
                    "msg": "该文章不存在",
                    "stauts": ARTICLE_NOT_EXIST
                }
                return data

class ArticlesResource(Resource):
    def post(self):
        pass
    
class CategoryResource(Resource):
    def post(self):
        args = parseBase.parse_args()
        action = args.get("action")
        if action == CATEGORY_SEARCH:
            category = Category.query.filter(Category.category_type.__eq__("1")).all()
            category_list = copy(category)
            for i in category:
                category_sub = Category.query.filter(Category.category_type.__eq__("2"),Category.parent_cateory.__eq__(i.id)).all()
                category_list[i.id-1].models = list(category_sub)
                # category_list[i.id-1].models = []
                # category_list[i.id-1].models.append(category_sub)
                print(category_sub)
                category_list.append(category_sub)
            print(category_list)

            data1 = {
                "models":category_list
            }
            print(marshal(data1, multiCategoryFields))
            return marshal(data1, multiCategoryFields)
            # data = {
            #     "status":200,
            #     "msg":"success",
            #     "categorys":marshal(data1, multiCategoryFields)
            # }
            # print(marshal(data1, multiCategoryFields))
            # return marshal(data,multisCategoryFields)
