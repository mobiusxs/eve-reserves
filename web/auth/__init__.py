from flask import Blueprint

from . import views

routes = Blueprint('auth', __name__, url_prefix='/auth')

routes.add_url_rule('/authorize', endpoint='authorize', view_func=views.authorize, methods=['GET'])
routes.add_url_rule('/callback', endpoint='callback', view_func=views.callback, methods=['GET'])
routes.add_url_rule('/logout', endpoint='logout', view_func=views.logout, methods=['GET'])
