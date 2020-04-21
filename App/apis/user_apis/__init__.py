from flask_restful import Api

from App.apis.user_apis.user_api import UsersResource
from App.apis.user_apis.user_order import MovieUserOrderResource

user_api = Api(prefix='/users')
user_api.add_resource(UsersResource,'/user/')

user_api.add_resource(MovieUserOrderResource,'/order/')
