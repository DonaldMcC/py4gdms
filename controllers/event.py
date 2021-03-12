# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
import datetime
from py4web import action, redirect, request, URL
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_questions, get_issues, get_actions, get_class, get_disabled
from ..d3js2py import getd3graph
from ..ndsfunctions import myconverter


# from pydal.validators import *


@action("new_event/<eid>", method=['GET', 'POST'])
@action("new_event", method=['GET', 'POST'])
@action.uses('new_event.html', session, db, auth.user)
def new_event(eid=0):
    db.evt.startdatetime.default = (datetime.datetime.utcnow()
                                    + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    db.evt.enddatetime.default = (datetime.datetime.utcnow()
                                  + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        db.evt.projid.default = session.get('projid',
                                            db(db.project.name == 'Unspecified').select(db.project.id).first().id)
    except AttributeError:
        pass
    form = Form(db.evt,
                record=eid,
                formstyle=FormStyleBulma)

    if form.accepted:
        session['eventid'] = form.vars.id
        redirect(URL('eventgrid'))
    return dict(form=form)


@action('create_next_event', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def create_next_event():
    # TODO think there is a prev_event to action
    # so expectation is that this is only called when event has no next event ie next_evt field is zero
    # for now anyone can create the next event for a project - might restrict to project owner at some point
    # unless shared project

    eid = request.json['eid']
    orig_rec = db(db.evt.id == eid).select().first()
    orig_event = orig_rec.as_dict()

    proj = db(db.project.id == orig_event['projid']).select().first()
    if not (proj.proj_shared or proj.proj_owner == auth.user_id):
        return 'You are not project owner and project not shared so not allowed to create events'

    recurrence = orig_event['recurrence']
    if recurrence == 'Weekly':
        recurdays = 7
    elif recurrence == 'Bi-weekly':
        recurdays = 14
    elif recurrence == 'Monthly':
        recurdays = 28
    elif recurrence == 'Quarterly':
        recurdays = 90
    else:
        recurdays = 1

    orig_event['startdatetime'] = orig_event['startdatetime'] + datetime.timedelta(days=recurdays)
    orig_event['enddatetime'] = orig_event['enddatetime'] + datetime.timedelta(days=recurdays)
    orig_event['evt_name'] = 'Next ' + orig_event['evt_name']
    orig_event['id'] = None
    new_evt = db.evt.insert(**dict(orig_event))
    orig_rec.update_record(next_evt=new_evt)
    db.commit()
    messagetxt = 'Next Event Created'
    return messagetxt


@action("view_event/<eid>", method=['GET', 'POST'])
@action("view_event", method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'view_event.html')
def view_event(eid='0'):
    eventrow = db(db.evt.id == eid).select().first()
    if eventrow:
        session['eventid'] = eid
        session['projid'] = eventrow.projid

    actions = get_actions(status='In Progress', event=eid, eventstatus=eventrow.status)
    questions = get_questions(status='In Progress', event=eid, eventstatus=eventrow.status)
    issues = get_issues(event=eid, eventstatus=eventrow.status)
    res_questions = get_questions(status='Resolved', event=eid, eventstatus=eventrow.status)
    res_actions = get_actions(status='Resolved', event=eid, execstatus='Incomplete')
    comp_actions = get_actions(status='Resolved', event=eid, execstatus='Completed')

    eventlevel = 0
    parentquest = 0
    redraw = 'false'

    quests, nodes, links, resultstring = getd3graph('event', eid, eventrow.status, 1, eventlevel, parentquest)

    # TODO finalise if events have owners or security
    # if auth.user and eventrow.evt_owner == auth.user.id:

    if auth.user:
        editable = 'true'
    else:
        editable = 'false'

    return dict(eventrow=eventrow, eventid=eid, actions=actions, questions=questions,
                issues=issues, res_actions=res_actions, res_questions=res_questions,
                comp_actions=comp_actions, get_class=get_class, get_disabled=get_disabled, quests=quests, nodes=nodes,
                links=links, resultstring=resultstring, redraw=redraw, eventowner=editable, projid=eventrow.projid,
                myconverter=myconverter, auth=auth)


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


@action('archive', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def archive():
    # This callable via a button from view_event
    # with all records in it and it will probably be restricted to project owner in due course-
    # May Need a fairly lengthy explanation
    # of what archiving is and current status shows in the event details then probably sort of OK
    # Lets attempt to do this via ajax and come back with a message that explains what archiving is - may well want a
    # pop up on this before submission
    # poss move to :eval on this for response.flash as done on quickanswer now

    eventid = int(request.json['eventid'])
    event = db(db.evt.id == eventid).select().first()
    if not event:
        return 'No matching event found'
    nexteventid = event.next_evt
    status = event.status
    responsetext = ''
    if event.status == 'Open':
        status = 'Archiving'
        responsetext = 'Event moved to archiving'
    elif event.status == 'Archiving':
        status = 'Archived'
        responsetext = 'Event moved to archived status'
        if not nexteventid:
            responsetext += ' WARNING: No follow-on event has been setup yet'
    else:
        return 'Only open events can be archived'

    event.update_record(status=status)
    query = db.question.eventid == eventid
    quests = db(query).select()

    # so below runs through if archiving lets leave as is albeit expectation is this function
    # is only called once so would always be doing inserts - maybe rearchive is possible though
    # so fine for now

    if status == 'Archiving':
        for row in quests:
            recid = db.eventmap.update_or_insert((db.eventmap.eventid == eventid) & (db.eventmap.questid == row.id),
                                                 eventid=eventid, questid=row.id,
                                                 status='Archiving',
                                                 xpos=row.xpos,
                                                 ypos=row.ypos,
                                                 questiontext=row.questiontext, answer1=row.answer1,
                                                 answer2=row.answer2,
                                                 qtype=row.qtype, urgency=row.urgency, importance=row.importance,
                                                 responsible=row.responsible,
                                                 correctans=row.correctans, queststatus=row.status,
                                                 notes=row.notes)

    if status == 'Archived':
        # So I think there will be a warning as a popup if no next event - if there is a next event
        # then approach will be to roll all open issues and open questions and any actions which are not
        # down as completed - completed actions and disagreed issues will still go to unspecified event
        # the following event will now need to be sent to this

        unspecevent = db(db.evt.evt_name == 'Unspecified').select(db.evt.id).first()
        unspecid = unspecevent.id
        for x in quests:
            if nexteventid != 0 and (x.status == 'In Progress' or (x.qtype == 'issue' and x.status == 'Agreed') or
                                     (x.qtype == 'action' and x.status == 'Agreed' and x.execstatus != 'Completed')):
                x.update_record(eventid=nexteventid)
            else:
                x.update_record(eventid=unspecid)

        query = db.eventmap.eventid == eventid
        eventquests = db(query).select()
        for row in eventquests:
            row.update_record(status='Archived')
        db.commit()

    return responsetext
