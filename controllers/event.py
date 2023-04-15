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

# This controller provides eventgrid, new event and other functions for creating recurring events

import datetime
from py4web import action, redirect, request, URL, Flash
from py4web.utils.form import Form, FormStyleBootstrap4
from ..bs4inline import FormStyleBootstrap4inline
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyleBootstrap5
from ..ndsqueries import get_class, get_disabled, get_items
from ..d3js2py import getd3graph
from .answer import like
from ..ndsfunctions import myconverter
from pydal.validators import *

flash = Flash()

@action("new_event/<eid>", method=['GET', 'POST'])
@action("new_event", method=['GET', 'POST'])
@action.uses('new_event.html', session, db, flash, auth.user)
def new_event(eid=None):
    db.event.startdatetime.default = (datetime.datetime.utcnow()
                                      + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:00")
    db.event.enddatetime.default = (datetime.datetime.utcnow()
                                    + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:00")
    db.event.projid.requires = IS_IN_DB(db((db.project.proj_shared == True) | (db.project.proj_owner == auth.user_id)),
                                        'project.id', '%(proj_name)s')
    try:
        db.event.projid.default = session.get('projid',
                                              db(db.project.name == 'Unspecified').select(db.project.id).first().id)
    except AttributeError:
        pass

    eid = int(eid) if eid and eid.isnumeric() else None
    if eid:
        islocked = db(db.event.id == eid).select('locked', 'prev_event').first()
        if islocked.locked:
            flash.set("Locked Event cannot be edited", sanitize=True)
            redirect(URL('eventgrid'))
    else:
        islocked = None
    form = Form(db.event, record=eid, formstyle=FormStyleBootstrap4inline)
    db.event.prev_event.requires = IS_EMPTY_OR(IS_IN_DB(db, 'event.id', '%(event_name)s'))

    if eid:
        proj = db(db.project.id == form.vars['projid']).select().first()
        if (not proj.proj_shared) and proj.proj_owner != auth.user_id:
            flash.set("Not Editable by You", sanitize=True)
            form.deletable = False
            form.readonly = True

    if form.vars.get('event_name', '') == 'Unspecified':
        form.deletable = False

    if form.accepted:
        session['eventid'] = form.vars['id']
        # Now want to establish if prev_event has been set and if it has we need to select it and link it's next
        # event to this one in order for archiving to work
        # so either eid and changed prev_event or created new record with an event id then we need the prev_event
        # and created event and update accordingly
        # TODO decide if need to remove if we blank - probably less urgent but should be done
        if not eid and form.vars['prev_event'] or (eid and form.vars['prev_event'] != islocked['prev_event']):
            orig_rec = db(db.event.id == form.vars['prev_event']).select().first()
            orig_rec.update_record(next_event=form.vars['id'])
            db.commit()
        redirect(URL('eventgrid'))
    return dict(form=form)


@action('create_next_event', method=['POST', 'GET'])
@action.uses(session, db, flash, auth.user)
def create_next_event():
    # so expectation is that this is only called when event has no next event ie next_event field is zero
    # for now anyone can create the next event for a project - might restrict to project owner at some point
    # unless shared project

    eid = int(request.json['eid'])
    orig_rec = db(db.event.id == eid).select().first()
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
    orig_event['event_name'] = 'Next ' + orig_event['event_name']
    orig_event['prev_event'] = eid
    orig_event['status'] = 'Open'
    orig_event['id'] = None
    new_evt = db.event.insert(**dict(orig_event))
    orig_rec.update_record(next_event=new_evt)
    db.commit()
    messagetxt = 'Next Event Created'
    flash.set("Next Event Created", sanitize=True)
    return messagetxt


@action("view_event/<eid>", method=['GET', 'POST'])
@action("view_event", method=['GET', 'POST'])
@action.uses('view_event.html', session, db, flash, auth.user)
def view_event(eid='0'):
    eventrow = db(db.event.id == eid).select().first()
    next_event_name = ''
    next_event_id = None
    if eventrow:
        session['eventid'] = eid
        session['projid'] = eventrow.projid
        if eventrow.next_event:
            next_eventrow = db(db.event.id == eventrow.next_event).select().first()
            next_event_name = next_eventrow.event_name if next_eventrow else ''
            next_event_id = next_eventrow.id if next_eventrow else 0
    else:
        redirect(URL('eventgrid'))

    actions = get_items(qtype='action', status='In Progress', event=eid, eventstatus=eventrow.status)
    questions = get_items(qtype='quest', status='In Progress', event=eid, eventstatus=eventrow.status)
    issues = get_items(qtype='issue', event=eid, eventstatus=eventrow.status)
    res_questions = get_items(qtype='quest', status='Resolved', event=eid, eventstatus=eventrow.status)
    res_actions = get_items(qtype='action', status='Resolved', event=eid, eventstatus=eventrow.status,
                            execstatus='Incomplete')
    comp_actions = get_items(qtype='action', status='Resolved', event=eid, eventstatus=eventrow.status,
                             execstatus='Completed')

    eventlevel = 0
    parentquest = 0
    quests, nodes, links, resultstring = getd3graph('event', eid, eventrow.status, 1, eventlevel, parentquest)
    projrow = db(db.project.id == eventrow.projid).select().first()
    editable = 'true' if projrow.proj_shared or projrow.proj_owner == auth.user else 'false'

    db.comment.auth_userid.default = auth.user_id
    db.comment.parenttable.default = 'event'
    db.comment.parentid.default = eid
    commentform = Form(db.comment, formstyle=FormStyleBootstrap4inline)

    return dict(eventrow=eventrow, eventid=eid, qactions=actions, questions=questions,
                issues=issues, res_actions=res_actions, res_questions=res_questions,
                comp_actions=comp_actions, get_class=get_class, get_disabled=get_disabled, quests=quests, nodes=nodes,
                links=links, resultstring=resultstring, redraw='false', eventowner=editable, projid=eventrow.projid,
                myconverter=myconverter, auth=auth, like=like, commentform=commentform,
                next_event_name=next_event_name, next_event_id=next_event_id)


@action('event_redirect/<status>', method=['POST', 'GET'])
@action.uses(session)
def event_redirect(status=None):
    session['event_status'] = status
    redirect(URL('eventgrid'))


@action('eventgrid', method=['POST', 'GET'])
@action('eventgrid/<path:path>', method=['POST', 'GET'])
@action.uses('eventgrid.html', session, db, flash, auth.user)
def eventgrid(path=None):
    # TODO need to look at passing a variable into the grid seems like path is only argument now
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4inline,
                         grid_class_style=GridClassStyleBootstrap5)

    fields = [db.event.event_name, db.locn.location_name, db.project.proj_name, db.event.status, db.event.startdatetime,
              db.event.enddatetime, db.event.description]

    orderby = [db.event.startdatetime]
    search_queries = [['Search by Name', lambda value: db.event.event_name == value]]

    status = session.get('event_status', 'Open')
    # search = GridSearch(search_queries, queries)
    if status != 'All':
        query = db.event.status == status
    else:
        query = db.event.id > 0

    grid = Grid(path,
                query,
                fields=fields,
                left=[db.locn.on(db.event.locationid == db.locn.id), db.project.on(db.event.projid == db.project.id)],
                headings=['Name', 'Location', 'Project', 'Status', 'Starttime', 'EndTime', 'Description'],
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

    eventid = int(request.json['eventid'])
    event = db(db.event.id == eventid).select().first()
    if not event:
        return 'No matching event found'
    nexteventid = event.next_event
    if event.status == 'Open':
        status = 'Archived'
        responsetext = 'Event moved to archived status'
        if not nexteventid:
            responsetext += ' WARNING: No follow-on event has been setup yet'
    else:
        return 'Only open events can be archived'

    event.update_record(status=status)
    query = db.question.eventid == eventid
    quests = db(query).select()

    unspecevent = db(db.event.event_name == 'Unspecified').select(db.event.id).first()
    unspecid = unspecevent['id']

    for row in quests:
        db.eventmap.update_or_insert((db.eventmap.eventid == eventid) & (db.eventmap.questid == row.id),
                                         eventid=eventid, questid=row.id,
                                         status=row.status,
                                         xpos=row.xpos,
                                         ypos=row.ypos,
                                         questiontext=row.questiontext,
                                         answer1=row.answer1,
                                         answer2=row.answer2,
                                         qtype=row.qtype,
                                         urgency=row.urgency,
                                         startdate=row.startdate,
                                         enddate=row.enddate,
                                         factopnion=row.factopinion,
                                         perccomplete=row.perccomplete,
                                         execstatus=row.execstatus,
                                         importance=row.importance,
                                         chosenai=row.chosenai,
                                         responsible=row.responsible,
                                         correctans=row.correctans,
                                         queststatus=row.status,
                                         aianswer=row.aianswer,
                                         notes=row.notes)

        if nexteventid != 0 and (row.status == 'In Progress' or (row.qtype == 'issue' and row.status == 'Agreed') or
                                     (row.qtype == 'action' and row.status == 'Agreed'
                                      and row.execstatus != 'Completed')):
            row.update_record(eventid=nexteventid)
        else:
            row.update_record(eventid=unspecid)
        db.commit()

    return responsetext
