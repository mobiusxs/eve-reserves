from flask import Blueprint

from . import views

routes = Blueprint('dashboard', __name__, url_prefix='/dashboard')

routes.add_url_rule('/', endpoint='index', view_func=views.index, methods=['GET'])
routes.add_url_rule('/market', endpoint='market', view_func=views.market, methods=['GET'])
