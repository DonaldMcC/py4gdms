# - Coding UTF8 -
#
# Networked Decision Making
# A framework for groups to make decisions asynchronously as asynchronous communication has proved highly
# successful and popular yet meetings persist for group decision making
#
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://www.netdecisionmaking.com/
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

# This controller provides gantt chart items

from ..ndsfunctions import get_gantt_data
from ..common import db, auth, session
from py4web import action
from yatl.helpers import XML
from ..ndsqueries import get_items


@action("allgantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def allgantt():
    eventrow = None
    eid = None
    res_actions = get_items(event=eid, status='Resolved', execstatus='Incomplete')
    projxml = get_gantt_data(res_actions) if res_actions else "<project></project>"
    return dict(project=XML(projxml), quests=res_actions, eventrow=eventrow)


@action("gantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def gantt():
    eid = session.get('eventid', None)
    eventrow = None
    if eid:
        eventrow = db(db.event.id == eid).select().first()
        res_actions = get_items(event=eid, status='Resolved')
    else:  # only incomplete actions as too many otherwise
        res_actions = get_items(event=eid, status='Resolved', execstatus='Incomplete')
    projxml = get_gantt_data(res_actions) if res_actions else "<project></project>"
    return dict(project=XML(projxml), quests=res_actions, eventrow=eventrow)
