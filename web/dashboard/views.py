from flask import render_template

from web.auth.decorators import authentication_required
from web.auth.decorators import role_required
from web.auth.models import Session


@authentication_required
def index():
    user = Session().get_current_user()
    return render_template('dashboard/index.html', user=user)


@authentication_required
@role_required('user')
def market():
    user = Session().get_current_user()
    return render_template('dashboard/market.html', user=user)
