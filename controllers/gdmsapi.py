from py4web import action, request
from ..common import db
from pydal.restapi import RestAPI, Policy

policy = Policy()
policy.set('*', 'GET', authorize=True, allowed_patterns=['*'])
policy.set('*', 'PUT', authorize=False)
policy.set('*', 'POST', authorize=False)
policy.set('*', 'DELETE', authorize=False)


@action('api/<tablename>/', method=['GET', 'POST'])
@action('api/<tablename>/<rec_id>', method=['GET', 'PUT', 'DELETE'])
@action.uses(db)
def api(tablename, rec_id=None):
    return RestAPI(db, policy)(request.method, tablename, rec_id, request.GET, request.POST)
