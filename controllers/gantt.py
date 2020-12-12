# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#   http://netdecisionmaking.com/gdmsdemo/
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.web2py.com
# or Groups: http://groups.google.com/group/web2py
# For details on the web framework used for this development
#
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be

"""
    exposes:
    http://..../[app]/gantt/index.html

    """
from builtins import range
from ..ndsfunctions import getlinks, get_gantt_data
from ..common import db, unauthenticated, authenticated, auth, session
from py4web import action, request, Flash
from yatl.helpers import XML

@action("gantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def gantt():
    # So issue now is sorting these with actions being demoted they should be sorted by parent and then
    # demoted items in order of parent start date so thinking we will sort by event level and just filter
    # the lower level later in the process

    strquery = (db.question.qtype == 'action') & (db.question.status == 'Resolved')
    orderstr = db.question.startdate
    quests = db(strquery).select(orderby=orderstr)

    questlist = [x.id for x in quests]
    dependlist = [[] for x in range(len(questlist))]
    intlinks = getlinks(questlist)
    for x in intlinks:
        dependlist[questlist.index(x.targetid)].append(x.sourceid)

    if quests:
        projxml = get_gantt_data(quests)
    else:
        projxml = "<project></project>"

    return dict(project=XML(projxml), quests=quests)
