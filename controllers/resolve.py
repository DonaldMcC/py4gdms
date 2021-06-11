from py4web import action, URL, Flash
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyle
flash = Flash()

@action("new_resolve/<res_id>", method=['GET', 'POST'])
@action("new_resolve", method=['GET', 'POST'])
@action.uses(session, db, auth.user, flash, 'new_resolve.html')
def new_resolve(res_id=None):
    res_id = int(res_id) if res_id and res_id.isnumeric() else None

    form = Form(db.resolve, record=res_id, formstyle=FormStyleBulma)
    if res_id:
        res_rec = db(db.resolve.id == res_id).select().first()
        if res_rec.owner != auth.user_id:
            form.readonly = True
            form.deletable = False
            flash.set("Only owner can edit resolve methods")
    return dict(form=form)


@action('resolvegrid', method=['POST', 'GET'])
@action('resolvegrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'resolvegrid.html')
def resolvegrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyle)

    fields = [db.resolve.resolve_name, db.resolve.responses, db.resolve.consensus, db.resolve.adminresolve]
    orderby = [db.resolve.resolve_name]
    # queries = [(db.resolve.id > 0)]
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
                editable=URL('new_resolve/'),
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)
