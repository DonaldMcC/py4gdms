
import datetime
from py4web import action, redirect, request, URL
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session,  auth, authenticated
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..ndsqueries import get_questions, get_issues, get_actions, get_class, get_disabled
from ..d3js2py import getlinks, getd3graph
from ..ndsfunctions import myconverter


@action("view_project/<pid>", method=['GET', 'POST'])
@action("view_project", method=['GET', 'POST'])
@action.uses('view_project.html', session, db, auth.user)
def view_project(pid='0'):
    projectrow = db(db.evt.id == pid).select().first()
    session.projid = pid if projectrow else 0

    actions = get_actions(status='In Progress', project=pid)
    questions = get_questions(status='In Progress', project=pid)
    issues = get_issues(project=pid)
    res_actions = get_actions(status='Resolved', project=pid)
    res_questions = get_questions(status='Resolved', project=pid)

    return dict(projectid=pid, actions=actions, questions=questions,
                issues=issues, res_actions=res_actions, res_questions=res_questions,
                get_class=get_class, get_disabled=get_disabled,
                myconverter=myconverter)


# @authenticated
@action("new_project/<pid>", method=['GET', 'POST'])
@action("new_project", method=['GET', 'POST'])
@action.uses('new_project.html', session, db, auth.user)
def new_project(pid=0):
    form = Form(db.project,
                record=pid,
                formstyle=FormStyleBulma)
    if form.accepted:
        session.projid = form.vars.id
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