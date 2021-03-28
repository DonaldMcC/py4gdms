from ..common import db, auth, session
from py4web import action, request
#  This will aim to use componennt loader to display the relevant comments (ideally with some pagination in due course
#  should be relatively doable ideally the request will ask for the table and the parent id for now and then
# at present we may return all comments or page them


@action('getcomments', method=['POST', 'GET'])
@action.uses(session, db, auth.user, "getcomments.load")
def getcomments():
    itemid = request.json['itemid']
    table = request.json['table']
    x = 0
    y = 50
    query = (db.comment.parent_table == table) & (db.comment.parent_id == itemid)
    sortby = db.comment.id
    comments = db(query).select(orderby=[sortby], limitby=(x, y))
    return dict(comments=comments)
