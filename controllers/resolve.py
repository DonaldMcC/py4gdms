from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBootstrap4
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
from py4web.utils.grid import Grid, GridClassStyle


#@authenticated
@action("new_resolve", method=['GET', 'POST'])
@action.uses('new_resolve.html', session, db)
def new_resolve():
    form = Form(db.resolve)
    return dict(form=form)


@action('resolvegrid', method=['POST', 'GET'])
@action('resolvegrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'resolvegrid.html')
def resolvegrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4,
                         grid_class_style=GridClassStyle)

    fields = [db.resolve.resolve_name, db.resolve.responses, db.resolve.consensus, db.resolve.adminresolve]

    orderby = [db.resolve.resolve_name]

    queries = [(db.resolve.id > 0)]

    search_queries = [['Search by Name', lambda value: db.resolve.resolve_name == value]]

    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.resolve,
                fields=fields,
                headings=['Name', 'Responses', 'Consensus', 'Adminresolve'],
                orderby=orderby,
                search_queries=search_queries,
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)