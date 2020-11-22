# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#


from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
from py4web.utils.grid import Grid, GridClassStyleBulma

@authenticated
def new_location():
    form = Form(db.locn)
    return dict(form=form)


@action('locationgrid', method=['POST', 'GET'])
@action('locationgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'locationgrid.html')
def locationgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.locn.location_name, db.locn.address1, db.locn.address2, db.locn.address3,
              db.locn.address4, db.locn.addrcode, db.locn.addrurl, db.locn.country, db.locn.description,
              db.locn.locn_shared]

    orderby = [db.locn.location_name]

    queries = [(db.locn.id > 0)]

    search_queries = [['Search by Name', lambda value: db.locn.location_name == value]]

    #search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.locn,
                fields=fields,
                headings=['Name', 'Address1', 'Address2', 'Address3', 'Address4', 'Addrcode', 'Addrurl',
                          'Country', 'Description'],
                orderby=orderby,
                search_queries=search_queries,
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)