# - Coding UTF8 -
#
# Networked Decision Making
# A framework for groups to make decisions asynchronously as asynchronous communication has proved highly
# successful and popular yet meetings persist for group decision making
#
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.py4web.com
# or Groups: http://groups.google.com/group/py4web
# For details on the web framework used for this development
#
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be

# This controller retrieves comments for any table

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
