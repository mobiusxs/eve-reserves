from flask import Blueprint

from . import views

routes = Blueprint('index', __name__, template_folder='templates', static_folder='static', static_url_path='/index/static')

routes.add_url_rule('/', endpoint='index', view_func=views.index, methods=['GET', 'POST'])
