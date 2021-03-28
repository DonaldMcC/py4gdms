import datetime
from ..common import db, authenticated, auth, session
from py4web import action, request
from ..ndsfunctions import score_question
from ..ndsqueries import get_class, get_disabled, get_items, check_liked

#  This will aim to use componennt loader to display the relevant comments (ideally with some pagination in due course
#  should be relatively doable ideally the request will ask for the table and the parent id for now and then
# at present we may return all comments or page them
