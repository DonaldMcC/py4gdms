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
    http://..../[app]/gantt.html

    """
from ..ndsfunctions import get_gantt_data
from ..common import db, auth, session
from py4web import action
from yatl.helpers import XML
from ..ndsqueries import get_actions


@action("gantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def gantt():
    res_actions = get_actions(status='Resolved')
    if res_actions:
        projxml = get_gantt_data(res_actions)
    else:
        projxml = "<project></project>"
    return dict(project=XML(projxml), quests=res_actions)
