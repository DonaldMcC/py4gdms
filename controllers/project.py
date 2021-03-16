
import datetime
from py4web import action, redirect, URL, request
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session,  auth
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_questions, get_issues, get_actions, get_class, get_disabled
from ..ndsfunctions import myconverter, get_gantt_data
from yatl.helpers import XML


@action("view_project/<pid>", method=['GET', 'POST'])
@action("view_project", method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'view_project.html')
def view_project(pid='0'):
    projectrow = db(db.project.id == pid).select().first()
    session['projid'] = pid if projectrow else 0
    events = db(db.evt.projid == pid).select(orderby=~db.evt.startdatetime)
    actions = get_actions(status='In Progress', project=pid)
    questions = get_questions(status='In Progress', project=pid)
    issues = get_issues(project=pid)
    res_actions = get_actions(status='Resolved', project=pid, execstatus='Incomplete')
    comp_actions = get_actions(status='Resolved', project=pid, execstatus='Completed')
    res_questions = get_questions(status='Resolved', project=pid)

    if res_actions:
        projxml = get_gantt_data(res_actions)
    else:
        projxml = "<project></project>"

    return dict(projectid=pid, projectrow=projectrow, actions=actions, questions=questions, issues=issues,
                res_actions=res_actions, res_questions=res_questions, comp_actions=comp_actions, events=events,
                get_class=get_class, get_disabled=get_disabled, myconverter=myconverter, project=XML(projxml),
                auth=auth)


@action("new_project/<pid>", method=['GET', 'POST'])
@action("new_project", method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'new_project.html')
def new_project(pid=0):
    db.project.startdate.default = (datetime.datetime.utcnow()).strftime("%Y-%m-%d")

    # default for this in models doesn't seem to work
    db.project.proj_owner.default=auth.user_id
    form = Form(db.project,
                record=pid,
                formstyle=FormStyleBulma)

    if form.accepted:
        session['projid'] = form.vars.id
        redirect(URL('projectgrid'))
    return dict(form=form)


@action('projectgrid', method=['POST', 'GET'])
@action('projectgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'projectgrid.html')
def projectgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.project.proj_name, db.project.proj_status, db.project.startdate, db.project.enddate,
              db.project.proj_owner]

    orderby = [db.project.proj_name]
    queries = [(db.project.id > 0)]
    search_queries = [['Search by Name', lambda value: db.project.name == value]]
    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.project,
                fields=fields,
                headings=['Name', 'Location', 'Project', 'Status', 'Starttime', 'EndTime', 'Description', 'Shared'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_project/0'),
                details=URL('view_project/'),
                editable=URL('new_project/'),
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)
