# - Coding UTF8 -
#
# Networked Decision Making
# A framework for groups to make decisions asynchronously as asynchronous communication has proved highly
# successful and popular yet meetings persist for group decision making
#
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.py4web.com
# or Groups: http://groups.google.com/group/py4web
# For details on the web framework used for this development
#
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be

# This controller provides functions for new location and location grid

from py4web import action, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBootstrap4
from ..bs4inline import FormStyleBootstrap4inline
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyleBootstrap5

flash = Flash()


@action("new_location", method=["GET", "POST"])
@action("new_location/<lid>", method=['GET', 'POST'])
@action.uses('new_location.html', session, db, flash, auth.user)
def new_location(lid=None):
    lid = int(lid) if lid and lid.isnumeric() else None
    if lid:
        islocked = db(db.locn.id == lid).select('locked').first()
        if islocked.locked:
            flash.set("Locked records cannot be edited")
            redirect(URL('locationgrid'))
    form = Form(db.locn, lid, formstyle=FormStyleBootstrap4inline)
    if form.accepted:
        redirect(URL('locationgrid'))
    return dict(form=form)


@action('locationgrid', method=['POST', 'GET'])
@action('locationgrid/<path:path>', method=['POST', 'GET'])
@action.uses('locationgrid.html', session, db, flash, auth.user)
def locationgrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4inline,
                         grid_class_style=GridClassStyleBootstrap5)

    fields = [db.locn.location_name, db.locn.address1, db.locn.address2,
              db.locn.addrcode, db.locn.addrurl, db.locn.country, db.locn.description]

    orderby = [db.locn.location_name]
    search_queries = [['Search by Name', lambda value: db.locn.location_name == value]]
    # search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.locn,
                fields=fields,
                headings=['Name', 'Address1', 'Address2', 'Addrcode', 'Addrurl',
                          'Country', 'Description'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_location/'),
                details=True,
                editable=URL('new_location/'),
                deletable=URL('new_project/delete/'),
                **GRID_DEFAULTS)
    return dict(grid=grid)
