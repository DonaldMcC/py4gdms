
from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
#from .libs.utils import GridSearch
from py4web.utils.grid import Grid, GridClassStyleBulma

#@authenticated
@action("new_project", method=['GET', 'POST'])
@action.uses('new_project.html', session, db)
def new_project():
    form = Form(db.project)
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
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)