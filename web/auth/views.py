from base64 import b64decode
from base64 import urlsafe_b64encode
from json import loads
from secrets import token_urlsafe
from time import time
from urllib.parse import urlencode

from flask import abort
from flask import current_app
from flask import make_response
from flask import redirect
from flask import request
from flask import url_for
from requests import get
from requests import post

from web.auth.models import Session
from web.auth.decorators import authentication_prohibited
from web.auth.decorators import authentication_required


@authentication_prohibited
def authorize():
    state = token_urlsafe(64)
    data = {
        'response_type': 'code',
        'redirect_uri': current_app.config['AUTH_CALLBACK_URL'],
        'client_id': current_app.config['AUTH_CLIENT_ID'],
        'scope': current_app.config['AUTH_SCOPE'],
        'state': state
    }
    location = f'https://login.eveonline.com/v2/oauth/authorize/?{urlencode(data)}'
    response = make_response(redirect(location=location, code=302))
    response.set_cookie(current_app.config['AUTH_STATE_COOKIE_NAME'], state)
    return response


def callback():
    validate_request_state()
    jwt = request_jwt()

    response = make_response(redirect(url_for(current_app.config['AUTH_LOGIN_REDIRECT_URL'])))
    response.set_cookie(current_app.config['AUTH_STATE_COOKIE_NAME'], '', expires=0)
    session_id = create_session(jwt)
    response.set_cookie(current_app.config['AUTH_SESSION_COOKIE_NAME'], session_id)
    return response


def validate_request_state():
    returned_state = request.args.get('state')
    sent_state = request.cookies.get(current_app.config['AUTH_STATE_COOKIE_NAME'])
    if returned_state != sent_state:
        abort(400)


def request_jwt():
    code = request.args.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code
    }
    auth_string = f"{current_app.config['AUTH_CLIENT_ID']}:{current_app.config['AUTH_SECRET_KEY']}".encode('utf-8')
    encoded_auth_string = urlsafe_b64encode(auth_string).decode()
    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }
    sso_response = post(url='https://login.eveonline.com/v2/oauth/token', data=data, headers=headers)
    sso_response.raise_for_status()
    return sso_response.json()


def create_session(jwt):
    session_id = token_urlsafe(64)

    jwt_header, jwt_payload, jwt_signature = jwt['access_token'].split('.')

    # parse payload
    payload = b64decode(jwt_payload + '==')
    payload = loads(payload)
    character_name = payload['name']
    character_id = payload['sub'].split(':')[2]

    # get character
    esi_response = get(f'https://esi.evetech.net/latest/characters/{character_id}/?datasource=tranquility')
    esi_response.raise_for_status()
    character = esi_response.json()
    corporation_id = character['corporation_id']
    alliance_id = character['alliance_id']

    session = Session(
        session_id=session_id,
        access_token=jwt['access_token'],
        expires_at=jwt['expires_in'] + int(time()),
        refresh_token=jwt['refresh_token'],
        header=jwt_header,
        payload=jwt_payload,
        signature=jwt_signature,
        name=character_name,
        character_id=character_id,
        corporation_id=corporation_id,
        alliance_id=alliance_id
    )
    session.save()
    return session_id


@authentication_required
def logout():
    session_id = request.cookies.get(current_app.config['AUTH_SESSION_COOKIE_NAME'])
    if session_id:
        session = Session.query.filter_by(session_id=session_id).first()

        if session:
            session.delete()

    response = make_response(redirect(url_for(current_app.config['AUTH_LOGOUT_REDIRECT_URL'])))
    response.set_cookie(current_app.config['AUTH_STATE_COOKIE_NAME'], '', expires=0)
    response.set_cookie(current_app.config['AUTH_SESSION_COOKIE_NAME'], '', expires=0)
    return response
