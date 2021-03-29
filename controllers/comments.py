from ..common import db, auth, session
from py4web import action, request
#  This will aim to use componennt loader to display the relevant comments (ideally with some pagination in due course
#  should be relatively doable ideally the request will ask for the table and the parent id for now and then
# at present we may return all comments or page them


# TODO - will need some sort of class based on users comments vs others comments
# this can be done all in template I think
@action('getcomments/<itemid>/<table>', method=['POST', 'GET'])
@action('getcomments/<itemid>', method=['POST', 'GET'])
@action('getcomments', method=['POST', 'GET'])
@action.uses(session, db, auth.user, "getcomments.load")
def getcomments(itemid=1, table='question'):
    x = 0
    y = 50
    query = (db.comment.parenttable == table) & (db.comment.parentid == itemid)
    sortby = db.comment.id
    comments = db(query).select(orderby=[sortby], limitby=(x, y))
    return dict(comments=comments)
