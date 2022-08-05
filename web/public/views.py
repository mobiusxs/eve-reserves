from flask import render_template

from web.auth.decorators import authentication_prohibited


@authentication_prohibited
def index():
    return render_template('public/index.html')
