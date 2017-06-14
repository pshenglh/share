from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import Users, AnonymousUser
from .errors import forbidden, unauthorized
from . import api

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email, password):
    if email == '':
        g.current_user = AnonymousUser
        return True
    user = Users.objects(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.route('/token')
def git_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')