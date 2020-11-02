# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#


from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated


from py4web.utils.grid import Grid, GridClassStyle
from py4web.utils.param import Param


@action('eventgrid', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'grid.html')
def eventgrid(**kwargs):

    queries = [(db.evt.id > 0)]
    orderby = [db.evt.id]

    grid = Grid(query=queries,
                orderby=orderby)
    return dict(grid=grid)


@action("new_event", method=['GET', 'POST'])
@action.uses('new_event.html', session, db)
def new_event():
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
    form = Form(db.evt)

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