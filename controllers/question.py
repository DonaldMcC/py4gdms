# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#

import json
from functools import reduce

from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form, FormStyleBulma, FormStyleDefault, FormStyleBootstrap4
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..libs.datatables import DataTablesField, DataTablesRequest, DataTablesResponse
from ..libs.utils import GridSearch
from pydal.validators import *


@action("new_question/<qid>", method=['GET', 'POST'])
@action("new_question", method=['GET', 'POST'])
@action.uses('new_question.html', session, db)
def new_question(qid='0'):
    db.question.id.readable = False
    db.question.id.writable = False
    db.question.status.requires = IS_IN_SET(['Draft', 'In Progress'])
    # TODO find out how request.args works with bottle prob different
    # questid = request.url_args(0, cast=int, default=0)

    # form = Form([db.question.questiontext, db.question.factopinion, db.question.answertext,
    #             db.question.answer1, db.question.answer2],
    #            formstyle=FormStyleGrid)
    # Note fieldlist creates error if you specify a record - so l
    form = Form(db.question,
                record=qid,
                formstyle=FormStyleGrid)
    if form.accepted:
        redirect(URL('datatables'))
    return dict(form=form)


@action('questiongrid', method=['POST', 'GET'])
@action('questiongrid/<path:path>', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'questiongrid.html')
def questiongrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBulma,
                         grid_class_style=GridClassStyleBulma)

    fields = [db.question.qtype, db.question.status, db.question.questiontext, db.question.factopinion,
              db.question.answer1, db.question.answer2, db.question.answertext, db.question.resolvemethod,
              db.evt.evt_name, db.project.proj_name]

    orderby = [db.question.qtype, db.question.status, db.question.questiontext]

    queries = [(db.question.eventid == db.evt.id)]


    eventlist = IS_NULL_OR(IS_IN_SET([x.evt_name for x in db(db.evt.id > 0).select(db.evt.evt_name,
                                                                                              orderby=db.evt.evt_name,
                                                                                              distinct=True)]))

    search_queries = [['Search by Event', lambda val: db.evt.evt_name == val,eventlist],
                      ['Search by Name', lambda val: db.question.questiontext.contains(val)]]

    search = GridSearch(search_queries, queries)

    # TODO move to entirely inner join and add project search query
    # TODO Get existing new_question form rather than default and we are then progressing a bit

    grid = Grid(path,
                search.query,
                fields=fields,
                left=[db.project.on(db.evt.projid == db.project.id)],
                headings=['Type', 'Status', 'Text', 'Fact_Opinion', 'Answer1', 'Answer2', 'Answertext',
                          'Resolvemethod', 'Event', 'Project'],
                orderby=orderby,
                search_form=search.search_form,
                #search_queries=search_queries,
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)


@unauthenticated
@action('datatables', method=['GET', 'POST'])
@action.uses(session, db, auth, 'datatables.html')
def datatables():
    """
    display a page with a datatables.net grid on it
    :return:
    """
    dt = DataTablesResponse(fields=[DataTablesField(name='DT_RowId', visible=False),
                                    DataTablesField(name='qtype'),
                                    DataTablesField(name='status'),
                                    DataTablesField(name='questiontext'),
                                    DataTablesField(name='factopinion'),
                                    DataTablesField(name='answer1')],
                            data_url=URL('datatables_data'),
                            create_url=URL('new_question/0'),
                            edit_url=URL('new_question/record_id'),
                            delete_url=URL('new_question/delete/record_id'),
                            sort_sequence=[[1, 'asc']])
    dt.script()
    return dict(dt=dt)


@unauthenticated
@action('datatables_data', method=['GET', 'POST'])
@action.uses(session, db, auth)
def datatables_data():
    """
    datatables.net makes an ajax call to this method to get the data
    :return:
    """
    dtr = DataTablesRequest(dict(request.query.decode()))
    dtr.order(db, 'question')

    queries = [(db.question.id > 0)]
    if dtr.search_value and dtr.search_value != '':
        queries.append((db.question.question_text.contains(dtr.search_value)) |
                       (db.question.responsible.contains(dtr.search_value)))

    query = reduce(lambda a, b: (a & b), queries)
    record_count = db(db.question.id > 0).count()
    filtered_count = db(query).count()

    dt = DataTablesResponse(fields=[DataTablesField(name='DT_RowId', visible=False),
                                    DataTablesField(name='qtype'),
                                    DataTablesField(name='Status'),
                                    DataTablesField(name='questiontext'),
                                    DataTablesField(name='factopinion'),
                                    DataTablesField(name='answer1')],
                            data_url=URL('datatables_data'),
                            create_url=URL('question/0'),
                            edit_url=URL('question/record_id'),
                            delete_url=URL('question/delete/record_id'),
                            sort_sequence=[[1, 'asc']])

    data = [dict(DT_RowId=z.id,
                 qtype=z.qtype,
                 status=z.status,
                 questiontext=z.questiontext,
                 factopinion=z.factopinion,
                 answer1=z.answer1) for z in db(query).select(orderby=dtr.dal_orderby,
                                                              limitby=[dtr.start, dtr.start + dtr.length])]
    return json.dumps(dict(data=data, recordsTotal=record_count, recordsFiltered=filtered_count))


@action('new_question/delete/<questid>', method=['GET', 'POST'])
@action.uses(session, db, auth, 'grid.html')
def new_question_delete(questid):
    result = db(db.question.id == questid).delete()
    redirect(URL('datatables'))


def FormStyleGrid(table, vars, errors, readonly, deletable):
    classes = {
        "outer": "field",
        "inner": "control",
        "label": "label is-uppercase",
        "info": "help",
        "error": "help is-danger py4web-validation-error",
        "submit": "button is-success",
        "input": "input",
        "input[type=text]": "input",
        "input[type=date]": "input",
        "input[type=time]": "input",
        "input[type=datetime-local]": "input",
        "input[type=radio]": "radio",
        "input[type=checkbox]": "checkbox",
        "input[type=submit]": "button",
        "input[type=password]": "password",
        "input[type=file]": "file",
        "select": "control select",
        "textarea": "textarea",
    }
    return FormStyleDefault(table, vars, errors, readonly, deletable, classes)
