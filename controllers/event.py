# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
import datetime
from py4web import action, redirect, request, URL, Flash
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_class, get_disabled, get_items
from ..d3js2py import getd3graph
from ..ndsfunctions import myconverter
from pydal.validators import *
flash = Flash()


@action("new_event/<eid>", method=['GET', 'POST'])
@action("new_event", method=['GET', 'POST'])
@action.uses(session, db, auth.user, flash, 'new_event.html')
def new_event(eid='0'):
    db.event.startdatetime.default = (datetime.datetime.utcnow()
                                    + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    db.event.enddatetime.default = (datetime.datetime.utcnow()
                                  + datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")
    try:
        db.event.projid.default = session.get('projid',
                                            db(db.project.name == 'Unspecified').select(db.project.id).first().id)
    except AttributeError:
        pass

    eid = int(eid)
    form = Form(db.event, record=eid, formstyle=FormStyleBulma)
    db.event.projid.requires = IS_IN_DB(db((db.project.proj_shared == True) | (db.project.proj_owner == auth.user_id)),
                                      'project.id', '%(proj_name)s')

    if eid:
        proj = db(db.project.id == form.vars['projid']).select().first()
        print(proj.proj_shared)
        if (not proj.proj_shared) and proj.proj_owner != auth.user_id:
            flash.set("Not Editable by You", sanitize=True)
            form.deletable = False
            form.readonly = True

    if form.vars.get('event_name', '') == 'Unspecified':
        form.deletable = False

    if form.accepted:
        session['eventid'] = form.vars.id
        redirect(URL('eventgrid'))
    return dict(form=form)


@action('create_next_event', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
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
    orig_event['id'] = None
    new_event = db.event.insert(**dict(orig_event))
    orig_rec.update_record(next_event=new_event)
    db.commit()
    messagetxt = 'Next Event Created'
    return messagetxt


@action("view_event/<eid>", method=['GET', 'POST'])
@action("view_event", method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'view_event.html')
def view_event(eid='0'):
    eventrow = db(db.event.id == eid).select().first()
    if eventrow:
        session['eventid'] = eid
        session['projid'] = eventrow.projid

    actions = get_items(qtype='action', status='In Progress', event=eid, eventstatus=eventrow.status)
    questions = get_items(qtype='quest', status='In Progress', event=eid, eventstatus=eventrow.status)
    issues = get_items(qtype='issue', event=eid, eventstatus=eventrow.status)
    res_questions = get_items(qtype='quest',status='Resolved', event=eid, eventstatus=eventrow.status)
    res_actions = get_items(qtype='action', status='Resolved', event=eid, execstatus='Incomplete')
    comp_actions = get_items(qtype='action', status='Resolved', event=eid, execstatus='Completed')

    eventlevel = 0
    parentquest = 0
    quests, nodes, links, resultstring = getd3graph('event', eid, eventrow.status, 1, eventlevel, parentquest)
    projrow = db(db.project.id == eventrow.projid).select().first()
    editable = 'true' if projrow.proj_shared or projrow.proj_owner == auth.user else 'false'

    return dict(eventrow=eventrow, eventid=eid, actions=actions, questions=questions,
                issues=issues, res_actions=res_actions, res_questions=res_questions,
                comp_actions=comp_actions, get_class=get_class, get_disabled=get_disabled, quests=quests, nodes=nodes,
                links=links, resultstring=resultstring, redraw='false', eventowner=editable, projid=eventrow.projid,
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

    fields = [db.event.event_name, db.locn.location_name, db.project.proj_name, db.event.status, db.event.startdatetime,
              db.event.enddatetime, db.event.description]

    orderby = [db.event.projid, db.event.event_name, db.event.startdatetime]
    search_queries = [['Search by Name', lambda value: db.event.event_name == value]]

    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.event,
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
                                                 status=row.status,
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

        unspecevent = db(db.event.event_name == 'Unspecified').select(db.event.id).first()
        unspecid = unspecevent.id
        for x in quests:
            if nexteventid != 0 and (x.status == 'In Progress' or (x.qtype == 'issue' and x.status == 'Agreed') or
                                     (x.qtype == 'action' and x.status == 'Agreed' and x.execstatus != 'Completed')):
                x.update_record(eventid=nexteventid)
            else:
                x.update_record(eventid=unspecid)
        db.commit()

    return responsetext
