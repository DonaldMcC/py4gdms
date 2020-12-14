# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
from py4web import action, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session,  auth
from py4web.utils.grid import Grid, GridClassStyleBulma


@action("new_event/<eid>", method=['GET', 'POST'])
@action("new_event", method=['GET', 'POST'])
@action.uses('new_event.html', session, db, auth.user)
def new_event(eid=0):
    form = Form(db.evt,
                record=eid,
                formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('eventgrid'))
    return dict(form=form)


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
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)
