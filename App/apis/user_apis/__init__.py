from flask_restful import Api

from App.apis.user_apis.user_api import MovieUsersResource,MovieUserResource
from App.apis.user_apis.user_order import MovieUserOrderResource

user_api = Api(prefix='/user')
user_api.add_resource(MovieUsersResource,'/users/')
user_api.add_resource(MovieUserResource,"/user/<int:id>")

user_api.add_resource(MovieUserOrderResource,'/order/')
