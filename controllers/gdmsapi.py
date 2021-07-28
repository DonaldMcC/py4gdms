from py4web import action, request
from ..common import db, auth, session
from pydal.restapi import RestAPI, Policy
# https://groups.google.com/g/py4web/c/3kGHOJp6DUo/m/fWc1PKmqAwAJ

#TODO try implementing above to authenticate for API in some manner
policy = Policy()
policy.set('*', 'GET', authorize=True, allowed_patterns=['*'])
policy.set('*', 'PUT', authorize=False)
policy.set('*', 'POST', authorize=False)
policy.set('*', 'DELETE', authorize=False)


@action('api/<tablename>/', method=['GET', 'POST'])
@action('api/<tablename>/<rec_id>', method=['GET', 'PUT', 'DELETE'])
@action.uses(db, session, auth.user)
def api(tablename, rec_id=None):
    return RestAPI(db, policy)(request.method, tablename, rec_id, request.GET, request.POST)
