from ..common import db, auth, session
from py4web import action
#  This will aim to use componennt loader to display the relevant comments (ideally with some pagination in due course
#  should be relatively doable ideally the request will ask for the table and the parent id for now and then
# at present we may return all comments or page them


@action('getcomments/<itemid>/<table>', method=['POST', 'GET'])
@action('getcomments/<itemid>', method=['POST', 'GET'])
@action('getcomments', method=['POST', 'GET'])
@action.uses(session, db, auth.user, "getcomments.load")
def getcomments(itemid=0, table='question'):
    x = 0
    y = 50
    query = (db.comment.parenttable == table) & (db.comment.parentid == itemid)
    comments = db(query).select(orderby=[db.comment.id], limitby=(x, y))
    return dict(comments=comments, auth=auth)
