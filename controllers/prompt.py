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

# This controller provides functions to created and edit prompts for AI LLMs - focus on OpenAI models for now

import datetime
from py4web import action, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBootstrap4
from ..bs4inline import FormStyleBootstrap4inline
from ..common import db, session,  auth
from py4web.utils.grid import Grid, GridClassStyleBootstrap5
from ..ndsqueries import get_class, get_disabled, get_items
from ..ndsfunctions import myconverter, get_gantt_data
from .answer import like
from yatl.helpers import XML
from markmin import markmin2html
from pydal.tools.tags import Tags
groups = Tags(db.auth_user, tag_table=db.auth_user_tag_groups)
flash = Flash()


@action("new_prompt/<pid>", method=['GET', 'POST'])
@action("new_prompt", method=['GET', 'POST'])
@action.uses('new_prompt.html', session, db, flash, auth.user, )
def new_prompt(pid=None):
    if not 'manager' in groups.get(auth.get_user()['id']):
        redirect(URL('not_authorized'))
    # default for this in models doesn't seem to work
    pid = int(pid) if pid and pid.isnumeric() else None
    form = Form(db.prompt, record=pid, formstyle=FormStyleBootstrap4inline)
    if form.accepted:
        redirect(URL('promptgrid'))
    return dict(form=form)


@action('promptgrid', method=['POST', 'GET'])
@action('promptgrid/<path:path>', method=['POST', 'GET'])
@action.uses('promptgrid.html', session, db, flash, auth.user)
def promptgrid(path=None):
    if not 'manager' in groups.get(auth.get_user()['id']):
        redirect(URL('not_authorized'))
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4inline,
                         grid_class_style=GridClassStyleBootstrap5)

    fields = [db.prompt.chosenai, db.prompt.scenario, db.prompt.setup, db.prompt.prompttype,
              db.prompt.sequence, db.prompt.status, db.prompt.prompt_text]
    orderby = [db.prompt.prompttype, db.prompt.sequence]
    search_queries = [['Search by Name', lambda value: db.prompt.name == value]]

    grid = Grid(path,
                db.prompt,
                fields=fields,
                headings=['Chosen AI', 'Scenario', 'Setup', 'Prompt Type', 'Seq', 'Status', 'Text'],
                orderby=orderby,
                search_queries=search_queries,
                create=URL('new_prompt/'),
                details=True,
                editable=URL('new_prompt/'),
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)
