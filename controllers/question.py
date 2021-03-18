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

from py4web import action, request, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBulma
from ..common import db, session, auth, authenticated
from py4web.utils.grid import Grid, GridClassStyleBulma
from ..libs.datatables import DataTablesField, DataTablesRequest, DataTablesResponse
from ..libs.utils import GridSearch
from pydal.validators import *
flash = Flash()

wolfram = True
try:
    import wolframalpha
    from ..settings_private import WA_ID
except ImportError as error:
    wolfram = False
import wikipedia


# make a "like" button factory
@authenticated.callback()
def like(qid):
    db.item_like.insert(item_id=qid)


@action("new_question/<qid>", method=['GET', 'POST'])
@action("new_question/<qid>/<qtype>", method=['GET', 'POST'])
@action("new_question/<qid>/<eid>/<xpos>/<ypos>/<sourceurl>", method=['GET', 'POST'])
@action("new_question", method=['GET', 'POST'])
@action.uses(session, db, auth.user, flash, 'new_question.html')
def new_question(qid='0', eid='0', xpos='0', ypos='0', sourceurl='questiongrid', qtype='quest'):
    db.question.id.readable = False
    db.question.id.writable = False
    db.question.status.requires = IS_IN_SET(['Draft', 'In Progress', 'Resolved'])
    db.question.xpos.default = int(xpos) if xpos.isnumeric() else 0
    db.question.ypos.default = int(ypos) if ypos.isnumeric() else 0
    db.question.qtype.default = qtype
    db.question.eventid.requires = IS_IN_DB(db((db.evt.status == 'Open') & (db.evt.projid == db.project.id) &
                                               ((db.project.proj_owner == auth.user_id) |
                                                (db.project.proj_shared == True))), 'evt.id', '%(evt_name)s')
    qid = int(qid)

    try:
        db.question.resolvemethod.default = session.get('resolvemethod',
                                            db(db.resolve.Defaultresolve == True).select(db.resolve.id).first().id)
    except AttributeError:
        pass

    try:
        db.question.eventid.default = int(eid) if eid.isnumeric() and int(eid) > 0 else session.get('eventid',
                                      db(db.evt.evt_name == 'Unspecified').select(db.evt.id).first().id)
    except AttributeError:
        pass

    # default for this in models doesn't seem to work
    db.question.auth_userid.default=auth.user_id
    # Note fieldlist creates error if you specify a record - so gone with javascript to customise form
    # TODO think want validation function so fact questions must be resolved and opinion questions cannot be - but draft
    # questions I think are always OK but should not show except for user - maybe just chew on this for a night before
    # I setup
    form = Form(db.question,
                record=qid,
                formstyle=FormStyleBulma)



    if qid:
        questrec = db((db.question.id == qid) & (db.question.eventid == db.evt.id) &
                     (db.evt.projid == db.project.id)).select().first()
        # You can edit quests on shared projects, your projects and always your questions
        if ((not questrec.project.proj_shared) and questrec.project.proj_owner != auth.user_id and
                questrec.question.auth_userid != auth.user_id):
            flash.set("Not Editable by You", sanitize=True)
            form.deletable = False
            form.readonly = True

    if form.accepted:
        session['eventid'] = form.vars['eventid']
        session['resolvemethod'] = form.vars['resolvemethod']
        sourceurl = sourceurl + '/' + eid if sourceurl == 'view_event' else sourceurl
        redirect(URL(sourceurl, vars=dict(qtype=qtype)))
    return dict(form=form)


#Below generally superceded by viewquest.py
@action("view_question/<qid>", method=['GET', 'POST'])
@action("view_question", method=['GET', 'POST'])
@action.uses(session, db, auth.user,'new_question.html')
def view_question(qid='0'):
    db.question.id.readable = False
    db.question.id.writable = False
    db.question.status.requires = IS_IN_SET(['Draft', 'In Progress'])

    # Note fieldlist creates error if you specify a record - so gone with javascript to customise form
    form = Form(db.question,
                readonly=True,
                record=qid,
                formstyle=FormStyleBulma)
    if form.accepted:
        redirect(URL('questiongrid'))
    print(auth.user_id)
    print(globals().get('user'))
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

    # queries = [(db.evt.id == db.question.eventid) & (db.evt.projid == db.project.id)]
    if 'qtype' in request.query:
        qtype = request.query.get('qtype')
    else:
        qtype = 'quest'

    if qtype:
        queries = [db.question.qtype == qtype]
    else:
        queries = [db.question.id > 0]

    eventlist = IS_NULL_OR(IS_IN_SET([x.evt_name for x in db(db.evt.id > 0).select(db.evt.evt_name,
                                                                                   orderby=db.evt.evt_name,
                                                                                   distinct=True)]))

    projlist = IS_NULL_OR(IS_IN_SET([x.proj_name for x in db(db.project.id > 0).select(db.project.proj_name,
                                                                                       orderby=db.project.proj_name,
                                                                                       distinct=True)]))

    search_queries = [['Search by Project', lambda val: db.project.proj_name == val, projlist],
                      ['Search by Event', lambda val: db.evt.evt_name == val, eventlist],
                      ['Search by Name', lambda val: db.question.questiontext.contains(val)]]
    search = GridSearch(search_queries, queries)

    if qtype == 'action':
        headings = ['Text', 'Status', 'Execstatus', 'Event', 'Project']
        fields = [db.question.questiontext, db.question.status, db.question.execstatus,
                  db.evt.evt_name, db.project.proj_name]
        orderby = [db.question.status, db.question.execstatus, db.question.questiontext]
    else:
        headings = ['Text', 'Answertext', 'Event', 'Project']
        fields = [db.question.questiontext, db.question.answertext, db.question.status,
                  db.evt.evt_name, db.project.proj_name]
        orderby = [db.question.status, db.question.questiontext]

    grid = Grid(path,
                search.query,
                fields=fields,
                headings=headings,
                left=[db.evt.on(db.question.eventid == db.evt.id),
                      db.project.on(db.evt.projid == db.project.id)],
                orderby=orderby,
                search_form=search.search_form,
                create=URL('new_question/0/'+qtype),
                details=URL('viewquest/'),
                editable=URL('new_question/'),
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)


@action('datatables', method=['GET', 'POST'])
@action.uses(session, db, auth.user, 'datatables.html')
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


# TODO probably need to confirm final fields in datatable and grid and seem to lack a display_url
@action('datatables_data', method=['GET', 'POST'])
@action.uses(session, db, auth.user)
def datatables_data():
    """
    datatables.net makes an ajax call to this method to get the data
    :return:
    """
    dtr = DataTablesRequest(dict(request.query.decode()))
    dtr.order(db, 'question')

    queries = [(db.question.id > 0)]
    # queries = [(db.question.eventid == db.evt.id) & (db.evt.projid == db.project.id)]
    # if dtr.search_value and dtr.search_value != '':
    #    queries.append((db.question.questiontext.contains(dtr.search_value)) |
    #                  (db.question.responsible.contains(dtr.search_value)))

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
@action.uses(session, db, auth.user, 'grid.html')
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
    return FormStyleBulma(table, vars, errors, readonly, deletable)


@action('wolfram_alpha_lookup', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def wolfram_alpha_lookup():
    # This should be a straightforward function called via Ajzx to lookup the answer to a question on wolfram alpha
    # and then feed the answer back into the Notes section of the question being created - it is anticipated that in
    # general this will only be used for self answered questions - however it might be called for other things in due
    # course and we may amend to support different knowledge engines later as well
    if not wolfram:
        return 'Wolfram Alpha Client not installed'
    client = wolframalpha.Client(WA_ID)

    qtext = request.json['questiontext']
    res = client.query(qtext)
    try:
        answer = ''
        for pod in res.pods:
            # print '{p.title}: {p.text}'.format(p=pod)
            if pod.title == 'Result':
                for sub in pod.subpods:
                    if sub.plaintext:
                        answer += sub.plaintext
                        answer += '\r'
            else:
                'No result found for this question'

    except AttributeError:
        answer = "No answer received"
    return answer



@action('wikipedia_lookup', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def wikipedia_lookup():
    # This should be a straightforward function called via Ajzx to lookup the answer to a question on wolfram alpha
    # and then feed the answer back into the Notes section of the question being created - it is anticipated that in
    # general this will only be used for self answered questions - however it might be called for other things in due
    # course and we may amend to support different knowledge engines later as well
    qtext = request.json['questiontext']
    print(qtext)
    pages = wikipedia.search(qtext, results=3)
    resultpage = wikipedia.summary(pages[0])
    # print(resultpage)

    if resultpage:
        res = resultpage
    else:
        res = 'No result found for this topic'
    return res
