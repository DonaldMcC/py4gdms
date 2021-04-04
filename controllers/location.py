# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#

from py4web import action, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyle
flash = Flash()

@action("new_location/<lid>", method=['GET', 'POST'])
@action("new_location", method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'new_location.html')
def new_location(lid='0'):
    lid=int(lid)
    if lid:
        #TODO - get flash working with redirect - seems it should but doesn't
        islocked = db(db.locn.id == lid).select('locked').first()
        if islocked.locked:
            flash.set("Locked records cannot be edited", sanitize=True)
            print('got locked location')
            redirect(URL('locationgrid'))
    form = Form(db.locn,
                record=lid,
                formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('locationgrid'))
    return dict(form=form)


@action('locationgrid', method=['POST', 'GET'])
@action('locationgrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'locationgrid.html')
def locationgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyle)

    fields = [db.locn.location_name, db.locn.address1, db.locn.address2, db.locn.address3,
              db.locn.address4, db.locn.addrcode, db.locn.addrurl, db.locn.country, db.locn.description]

    orderby = [db.locn.location_name]
    search_queries = [['Search by Name', lambda value: db.locn.location_name == value]]
    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.locn,
                fields=fields,
                headings=['Name', 'Address1', 'Address2', 'Address3', 'Address4', 'Addrcode', 'Addrurl',
                          'Country', 'Description'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_location/0'),
                details=True,
                editable=URL('new_location/'),
                deletable=URL('new_project/delete/'),
                **GRID_DEFAULTS)
    return dict(grid=grid)
