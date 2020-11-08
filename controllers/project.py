
from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
#from .libs.utils import GridSearch
from py4web.utils.grid import Grid, GridClassStyleBulma


@action("new_project", method=['GET', 'POST'])
@action.uses('new_project.html', session, db)
def new_project():
    # This allows creation and editing of projects by their owner
    # 'answer_group' removed as no other security functions for projects and events yet - not currently needed
    #fields = ['proj_name', 'description', 'proj_url', 'startdate', 'enddate', 'proj_shared']
    #projid = request.args(0, default=None)
    #if projid is not None:
    #    record = db.project(projid)
    #    if record.proj_owner != auth.user_id:
    #        session.flash = 'Not Authorised - projects can only be edited by their owners'
    #        redirect(URL('new_project'))
    #    form = SQLFORM(db.project, record, fields=fields)
    #else:
    form = Form(db.project)

    #if form.validate():
    #    if projid is not None:
    #        if form.deleted:
    #            db(db.project.id == projid).delete()
    #            response.flash = 'Project deleted'
    #            redirect(URL('default', 'index'))
    #        else:
    #            record.update_record(**dict(form.vars))
    #            response.flash = 'Project updated'
    #            redirect(URL('default', 'index'))
    #    else:
    #        form.vars.id = db.project.insert(**dict(form.vars))
    #        session.flash = 'Project Created'
    #        redirect(URL('accept_project', args=[form.vars.id, auth.user_id]))
    #elif form.errors:
    #    response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill out the form'

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

    #search = GridSearch(search_queries, queries)

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