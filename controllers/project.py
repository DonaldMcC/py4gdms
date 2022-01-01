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

# This controller provides functions to created and edit projects

import datetime
from py4web import action, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session,  auth
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_class, get_disabled, get_items
from ..ndsfunctions import myconverter, get_gantt_data
from .answer import like
from yatl.helpers import XML
flash = Flash()


@action("view_project/<pid>", method=['GET', 'POST'])
@action("view_project", method=['GET', 'POST'])
@action.uses(session, db, flash, auth.user, 'view_project.html')
def view_project(pid='0'):
    projectrow = db(db.project.id == pid).select().first()
    session['projid'] = pid if projectrow else 0
    events = db(db.event.projid == pid).select(orderby=~db.event.startdatetime)
    actions = get_items(qtype='action', status='In Progress', project=pid)
    questions = get_items(qtype='question', status='In Progress', project=pid)
    issues = get_items(qtype='issue', project=pid)
    res_actions = get_items(qtype='action', status='Resolved', project=pid, execstatus='Incomplete')
    comp_actions = get_items(qtype='action', status='Resolved', project=pid, execstatus='Completed')
    res_questions = get_items(qtype='question', status='Resolved', project=pid)

    if res_actions:
        projxml = get_gantt_data(res_actions)
    else:
        projxml = "<project></project>"

    db.comment.auth_userid.default = auth.user_id
    db.comment.parenttable.default = 'project'
    db.comment.parentid.default = pid
    commentform = Form(db.comment,  formstyle=FormStyleBulma)
    return dict(projectid=pid, projectrow=projectrow, qactions=actions, questions=questions, issues=issues,
                res_actions=res_actions, res_questions=res_questions, comp_actions=comp_actions, events=events,
                get_class=get_class, get_disabled=get_disabled, myconverter=myconverter, project=XML(projxml),
                auth=auth, like=like, commentform=commentform)


@action("new_project/<pid>", method=['GET', 'POST'])
@action("new_project", method=['GET', 'POST'])
@action.uses(session, db, flash, auth.user,  'new_project.html')
def new_project(pid=None):
    # default for this in models doesn't seem to work
    db.project.startdate.default = (datetime.datetime.utcnow()).strftime("%Y-%m-%d")
    pid = int(pid) if pid and pid.isnumeric() else None
    if pid:
        # locked is mainly to protect the unspecified project from changes
        islocked = db(db.project.id == pid).select().first()
        if islocked.locked or (islocked.proj_owner != auth.user_id and not islocked.proj_shared):
            flash.set("You can't edit this record", sanitize=True)
            redirect(URL('projectgrid'))
    db.project.proj_owner.default = auth.user_id
    form = Form(db.project, record=pid, formstyle=FormStyleBulma)

    if pid:
        proj = db(db.project.id == pid).select().first()
        if (not proj.proj_shared) and proj.proj_owner != auth.user_id:
            flash.set("Not Editable by You", sanitize=True)
            form.deletable = False
            form.readonly = True

    if form.accepted:
        session['projid'] = form.vars['id']
        redirect(URL('projectgrid'))
    return dict(form=form)


@action('projectgrid', method=['POST', 'GET'])
@action('projectgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, flash, auth.user,  'projectgrid.html')
def projectgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.project.proj_name, db.project.proj_status, db.project.description,  db.project.proj_shared]
    orderby = [~db.project.priority]
    search_queries = [['Search by Name', lambda value: db.project.name == value]]
    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.project,
                fields=fields,
                headings=['Name', 'Status', 'Description', 'Shared'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_project/0'),
                details=URL('view_project/'),
                editable=URL('new_project/'),
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)
