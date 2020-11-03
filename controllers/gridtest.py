from py4web import action
from py4web.utils.form import FormStyleBulma
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..common import db, session, auth

@action('grid/test', method=['POST', 'GET'])
@action('grid/test/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'grid.html')
def regions(path=None):
    
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.evt.evt_name, db.evt.locationid, db.evt.projid, db.evt.status, db.evt.startdatetime,
              db.evt.enddatetime, db.evt.description, db.evt.evt_shared]

    orderby = [db.evt.evt_name]

    search_queries = [['Search by Number', lambda value: db.region.region_number == value]]

    grid = Grid(path,
                db.evt,
                fields=fields,
                headings=['Name', 'Location', 'Project', 'Status','Starttime', 'EndTime', 'Description', 'Shared'],
                orderby=orderby,
                search_queries=search_queries,
                **GRID_DEFAULTS)

    return dict(grid=grid)