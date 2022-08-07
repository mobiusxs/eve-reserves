from flask import render_template

from web.auth.decorators import authentication_required
from web.auth.decorators import role_required
from web.auth.models import Session

session = Session()


@authentication_required
@role_required('staff')
def create():
    user = session.get_current_user()
    return render_template('doctrine/create.html', user=user)
