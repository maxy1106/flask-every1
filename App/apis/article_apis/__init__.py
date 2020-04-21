from flask_restful import Api

from App.apis.article_apis.article_api import ArticleResource, ArticlesResource

article_api = Api(prefix='/articles')

article_api.add_resource(ArticleResource,'/article/')
article_api.add_resource(ArticlesResource,'/articles/')