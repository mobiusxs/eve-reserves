from flask import Blueprint

from . import views

routes = Blueprint('doctrine', __name__, url_prefix='/doctrine')

routes.add_url_rule('/create', endpoint='create', view_func=views.create, methods=['GET'])
