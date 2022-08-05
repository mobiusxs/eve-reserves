ENV = 'testing'
TESTING = True
SECRET_KEY = 'test'
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SQLALCHEMY_TRACK_MODIFICATIONS = False

AUTH_LOGIN_REDIRECT_URL = 'dashboard.index'
AUTH_LOGOUT_REDIRECT_URL = 'public.index'
AUTH_SESSION_COOKIE_NAME = 'auth_session'
AUTH_STATE_COOKIE_NAME = 'auth_state'
AUTH_CLIENT_ID = '1234'
AUTH_SECRET_KEY = '1234'
AUTH_SCOPE = 'esi-calendar.respond_calendar_events.v1'
AUTH_CALLBACK_URL = 'http://localhost/auth/callback'
