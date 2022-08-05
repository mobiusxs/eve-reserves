from functools import wraps

from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import url_for

from web.auth.models import Session
from web.settings import AUTH_LOGIN_REDIRECT_URL

session = Session()


def authentication_required(f):
    """Require users to be authenticated in order to access a view.
    Redirect to authorization view if not authenticated.

    Usage:
        @authentication_required
        def some_view():
            return render_template('some_view.html')
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get_current_user()
        if not user or not user.is_authenticated():
            return redirect(url_for('auth.authorize'))
        return f(*args, **kwargs)
    return decorated_function


def authentication_prohibited(f):
    """Prevent authenticated users from accessing a view.
    Redirect to AUTH_LOGIN_REDIRECT_URL if authenticated.

    Usage:
        @authentication_prohibited
        def some_view():
            return render_template('some_view.html')
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get_current_user()
        if user and user.is_authenticated():
            return redirect(url_for(AUTH_LOGIN_REDIRECT_URL))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """Require some role to access a view.
    Redirect to AUTH_LOGIN_REDIRECT_URL and flash a message if user lacks role.

    Usage:
        @role_required('some_role')
        def some_view():
            return render_template('some_view.html')
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get_current_user()
            if user.has_role(role):
                return f(*args, **kwargs)
            else:
                current_app.logger.error(f'{user.name}:{user.character_id} attempted to access {request.full_path} without {role} role')
                flash('You do not have permission to access that page.')
                return redirect(url_for(AUTH_LOGIN_REDIRECT_URL))
        return decorated_function
    return decorator
