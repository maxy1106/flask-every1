from App.apis.goods_apis import goods_api
from App.apis.user_apis import user_api


def init_api(app):
    goods_api.init_app(app)
    user_api.init_app(app)




