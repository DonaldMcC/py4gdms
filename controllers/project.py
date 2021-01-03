
from py4web import action, redirect, URL
from ..common import db, session, auth
#from .libs.utils import GridSearch
from py4web.utils.grid import Grid, GridClassStyleBulma
from py4web.utils.form import Form, FormStyleBootstrap4


# @authenticated
@action("new_project/<pid>", method=['GET', 'POST'])
@action("new_project", method=['GET', 'POST'])
@action.uses('new_project.html', session, db, auth.user)
def new_project(pid=0):
    form = Form(db.project,
                record=pid,
                formstyle=FormStyleBootstrap4)
    if form.accepted:
        session.projid = form.vars.id
        print(form.vars)
        print('projid', session.projid)
        redirect(URL('projectgrid'))

    return dict(form=form)


@action('projectgrid', method=['POST', 'GET'])
@action('projectgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'projectgrid.html')
def projectgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4,
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
                details=True,
                editable=URL('new_project/'),
                deletable=URL('new_project/delete/'),
                **GRID_DEFAULTS)

    return dict(grid=grid)