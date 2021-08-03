# https://groups.google.com/g/py4web/c/3kGHOJp6DUo/m/fWc1PKmqAwAJ

from py4web import action, request, abort, redirect, URL, HTTP
from py4web.core import Fixture
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
from pydal.restapi import RestAPI, Policy
from pydal.validators import CRYPT
import jwt
from datetime import datetime, timedelta
import json

#TODO try implementing above to authenticate for API in some manner
policy = Policy()
policy.set('*', 'GET', authorize=True, allowed_patterns=['*'])
policy.set('*', 'PUT', authorize=False)
policy.set('*', 'POST', authorize=False)
policy.set('*', 'DELETE', authorize=False)


class AuthorizationError(Exception):
    """ A base class for exceptions used by bottle. """
    pass


def jwt_token_from_header():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthorizationError(
            {'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthorizationError(
            {'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
        raise AuthorizationError(
            {'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})

    return parts[1]


@action("authenticate", method=['POST'])
def authenticate():
    username, password = request.json.get("email"), request.json.get("password")
    print(username)
    print(password)

    try:
        # authenticate against auth_user table
        query = db.auth_user.email == username
        user = db(query).select().first()
        if CRYPT()(password)[0] != user.password:
            return (json.dumps({'error': 403, 'message': 'Authentication failed for: %s' % (username)}))
    except:
        return (json.dumps({'error': 403, 'message': 'Authentication failed for %s: ' % (username)}))

    data = {}
    data['username'] = username
    data['email'] = user.email
    data['first_name'] = user.first_name
    data['last_name'] = user.last_name
    data['exp'] = datetime.utcnow() + timedelta(seconds=1200)
    token = jwt.encode(data, 'secret', algorithm='HS256')

    print (token)
    return (json.dumps({'token': token}))


@action('apisec/<tablename>/')
@action('apisec/<tablename>/<rec_id>')
def apisec(tablename, rec_id=None):
    token = jwt_token_from_header()
    if token:
        try:
            jwt.decode(token, 'secret', algorithms=['HS256'])
            return RestAPI(db, policy)(request.method,
                                       tablename,
                                       rec_id,
                                       request.GET,
                                       request.POST
                                       )
        except jwt.ExpiredSignatureError:
            return (json.dumps({'error': 403, 'message': 'Token Expired'}))
        except jwt.InvalidSignatureError:
            return (json.dumps({'error': 403, 'message': 'JWT Signature failed!'}))
        except:
            return (json.dumps({'error': 403, 'message': 'User not found'}))
    else:
        return (json.dumps({'error': 403, 'message': 'Token required!'}))


class JwtLogin(Fixture):
    def __init__(self):
        self.token = None

    def on_request(self):
        self.token = jwt_token_from_header()
        if self.token:
            try:
                jwt.decode(self.token, 'secret', algorithms=['HS256'])
                pass
            except jwt.ExpiredSignatureError:
                raise HTTP(426)
            except jwt.InvalidSignatureError:
                raise HTTP(401)
            except:
                raise HTTP(401)
        else:
            raise HTTP(511)


@action('api/<tablename>/', method=['GET', 'POST'])
@action('api/<tablename>/<rec_id>', method=['GET', 'PUT', 'DELETE'])
@action.uses(db, session, auth.user)
def api(tablename, rec_id=None):
    return RestAPI(db, policy)(request.method, tablename, rec_id, request.GET, request.POST)


@action('apisecjwt/<tablename>/')
@action('apisecjwt/<tablename>/<rec_id>')
@action.uses(JwtLogin())
def apisejwtc(tablename, rec_id=None):
    return RestAPI(db, policy)(request.method,
                                   tablename,
                                   rec_id,
                                   request.GET,
                                   request.POST
                                   )
