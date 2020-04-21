from App.apis.article_apis import article_api
from App.apis.user_apis import user_api




def init_api(app):
    user_api.init_app(app)
    article_api.init_app(app)




