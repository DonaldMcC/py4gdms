# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
import datetime
from py4web import action, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session,  auth
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_questions, get_issues, get_actions, get_class, get_disabled
from ..d3js2py import getlinks, getd3graph

@action("new_event/<eid>", method=['GET', 'POST'])
@action("new_event", method=['GET', 'POST'])
@action.uses('new_event.html', session, db, auth.user)
def new_event(eid=0):
    db.evt.startdatetime.default = (datetime.datetime.utcnow()
                                    + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        db.evt.projid.default = session.projid
    except AttributeError:
        pass
    form = Form(db.evt,
                record=eid,
                formstyle=FormStyleBulma)

    if form.accepted:
        session.eventid = form.vars.id
        redirect(URL('eventgrid'))
    return dict(form=form)


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


@action("view_event/<eid>", method=['GET', 'POST'])
@action("view_event", method=['GET', 'POST'])
@action.uses('view_event.html', session, db, auth.user)
def view_event(eid='0'):
    eventrow = db(db.evt.id == eid).select().first()
    if eventrow:
        session.eventid = eid
        session.projid = eventrow.projid
        if eventrow.status == 'Archived':
            redirect(URL('event', 'eventreview', args=eid))

    actions = get_actions(status='In Progress', event=eid)
    questions = get_questions(status='In Progress', event=eid)
    issues = get_issues(event=eid)
    res_actions = get_actions(status='Resolved', event=eid)
    res_questions = get_questions(status='Resolved', event=eid)

    eventlevel = 0 #  so think we report <= to this
    parentquest = 0
    redraw = 'true'

    quests, nodes, links, resultstring = getd3graph('event', eid, eventrow.status, 1, eventlevel, parentquest)

    #print(nodes)
    #TODO finalise if events have owners or security
    # if auth.user and eventrow.evt_owner == auth.user.id:

    if auth.user:
        editable = 'true'
    else:
        editable = 'false'


    return dict(eventrow=eventrow, eventid=eid, actions=actions, questions=questions,
                issues=issues, res_actions=res_actions, res_questions=res_questions,
                get_class=get_class, get_disabled=get_disabled, quests=quests, nodes=nodes, links=links,
                resultstring=resultstring, redraw=redraw, eventowner=editable, projid=eventrow.projid,
                myconverter=myconverter)




@action('eventgrid', method=['POST', 'GET'])
@action('eventgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'eventgrid.html')
def eventgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.evt.evt_name, db.locn.location_name, db.project.proj_name, db.evt.status, db.evt.startdatetime,
              db.evt.enddatetime, db.evt.description, db.evt.evt_shared]

    orderby = [db.evt.projid, db.evt.evt_name, db.evt.startdatetime]
    queries = [(db.evt.id > 0)]
    search_queries = [['Search by Name', lambda value: db.evt.evt_name == value]]

    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.evt,
                fields=fields,
                left=[db.locn.on(db.evt.locationid == db.locn.id),
                      db.project.on(db.evt.projid == db.project.id)],
                headings=['Name', 'Location', 'Project', 'Status', 'Starttime', 'EndTime', 'Description', 'Shared'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_event'),
                details=URL('view_event/'),
                editable=URL('new_event/'),
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)
