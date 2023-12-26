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

# This controller provides functions to create and edit questions, actions and issues


import json
import wikipedia
from functools import reduce

from py4web import action, request, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBootstrap4
from ..bs4inline import FormStyleBootstrap4inline
from ..common import db, session, auth
from py4web.utils.grid import Grid, GridClassStyleBootstrap5, GridClassStyle
from ..libs.datatables import DataTablesField, DataTablesRequest, DataTablesResponse
# from ..libs.utils import GridSearch
from pydal.validators import *
from ..twitter_client import publish
from ..ndsfunctions import score_question
from ..ndsqueries import get_messages
from .network import request_link

flash = auth.flash

try:
    import wolframalpha
    from ..settings_private import WA_ID

    wolfram = True
except ImportError as error:
    wolfram = False

try:
    from openai import OpenAI
    from ..settings_private import OPENAI_API_KEY

    oai = True
except ImportError as error:
    oai = False

try:
    from bardapi import Bard
    from ..settings_private import BARD_API_KEY

    _BARD_API_KEY = BARD_API_KEY
    bardai = True
except ImportError as error:
    bardai = False
    print('failed to import bard')


def check_status(form):
    if form.vars['status'] == 'In Progress' and form.vars['factopinion'] == 'Fact':
        form.errors['status'] = 'Fact questions must have status Resolved or Draft'
    if form.vars['status'] == 'Resolved' and form.vars['factopinion'] == 'Opinion':
        form.errors['status'] = 'Questions of opinion cannot be submitted as resolved'
    return


@action("new_question/<qid>", method=['GET', 'POST'])
@action("new_question/<qid>/<qtype>", method=['GET', 'POST'])
@action("new_question/<qid>/<qtype>/<eid>", method=['GET', 'POST'])
@action("new_question/<qid>/<qtype>/<eid>/<xpos>/<ypos>/<sourceurl>", method=['GET', 'POST'])
@action("new_question/<qid>/<qtype>/<eid>/<xpos>/<ypos>/<sourceurl>/<sourceq>", method=['GET', 'POST'])
@action("new_question", method=['GET', 'POST'])
@action.uses('new_question.html', session, db, flash, auth.user)
def new_question(qid=None, qtype='quest', eid='0', xpos='0', ypos='0', sourceurl='questiongrid/select', sourceq=0):
    db.question.id.readable = False
    db.question.id.writable = False
    db.question.status.requires = IS_IN_SET(['Draft', 'In Progress', 'Resolved'])
    db.question.xpos.default = int(xpos) if xpos.isnumeric() else 0
    db.question.ypos.default = int(ypos) if ypos.isnumeric() else 0
    db.question.qtype.default = qtype
    db.question.eventid.requires = IS_IN_DB(db((db.event.status == 'Open') & (db.event.projid == db.project.id) &
                                               ((db.project.proj_owner == auth.user_id) |
                                                (db.project.proj_shared == True))), 'event.id', '%(event_name)s')
    qid = int(qid) if qid and qid.isnumeric() else None
    questrec = None
    # print(auth.user_id)

    userdefresolve = db(db.auth_user.id == auth.user_id).select(db.auth_user.default_resolve).first()['default_resolve']
    try:
        defaultresolve = db(db.resolve.resolve_name == userdefresolve).select(db.resolve.id).first()['id']
    except (AttributeError, TypeError):
        try:
            defaultresolve = db(db.resolve.Defaultresolve == True).select(db.resolve.id).first()['id']
        except (AttributError, TypeError):
            defaultresolve = 1

    try:
        db.question.resolvemethod.default = session.get('resolvemethod', defaultresolve)
    except AttributeError:
        pass
    except TypeError:
        pass

    try:
        db.question.eventid.default = int(eid) if eid.isnumeric() and int(eid) > 0 \
            else session.get('eventid', db(db.event.event_name == 'Unspecified').select(db.event.id).first()['id'])
    except AttributeError:
        pass
    except TypeError:
        pass

    try:
        db.question.chosenai.default = session.get('chosenai', db(db.knowledge.defaultknowledge == True).select(
            db.knowledge.id).first()['id'])
    except AttributeError:
        pass
    except TypeError:
        pass

    # default for this in models doesn't seem to work
    db.question.auth_userid.default = auth.user_id
    # Note fieldlist creates error if you specify a record - so gone with javascript to customise form
    # form = Form(db.question, record=qid, validation=check_status, formstyle=FormStyleBulma)
    # temporarily removing validation as that seems to mean submit button won't work on IOS
    if qid:
        questrec = db((db.question.id == qid) & (db.question.eventid == db.event.id) &
                      (db.event.projid == db.project.id)).select().first()
        answers = db(db.userquestion.questionid == qid).select()
        if answers:
            db.question.questiontext.writable = False
            db.question.qtype.writable = False
            db.question.status.writable = False
            db.question.factopinion.writable = False
            db.question.answer1.writable = False
            db.question.answer2.writable = False

    db.question.correctanstext.readable = False
    db.question.priority.writable = False
    if qid:
        form = Form(db.question, record=qid, formstyle=FormStyleBootstrap4inline)
    else:
        form = Form(db.question, formstyle=FormStyleBootstrap4inline)

    if qid and questrec:
        # You can edit quests on shared projects, your projects and always your questions
        if ((not questrec.project.proj_shared) and questrec.project.proj_owner != auth.user_id and
                questrec.question.auth_userid != auth.user_id):
            flash.set("Not Editable by You", sanitize=True)
            form.deletable = False
            form.readonly = True

    if form.accepted:
        session['eventid'] = form.vars['eventid']
        session['resolvemethod'] = form.vars['resolvemethod']
        session['chosenai'] = form.vars['chosenai']
        # sourceurl = sourceurl + '/' + eid if sourceurl == 'view_event' else sourceurl
        # sourceurl = sourceurl + '/' + eid if int(eid) else sourceurl
        flash.set("Item Created RecordID:" + str(form.vars['id']), sanitize=True)
        if qid:
            score_question(qid)  # Added to rescore question principally to allow changing to single resolution later
        if form.vars['social_media'] and not qid:  # only want to publish new questions not edits
            # now just insert a record into
            db.tweets.insert(parentid=qid, tweet_text=form.vars['questiontext'])

        if sourceq:
            request_link(sourceq, form.vars['id'], 'create')
        if eid:
            sourceurl += r'/' + str(eid)
        redirect(URL(sourceurl, vars=dict(qtype=qtype)))
    return dict(form=form)


@action('questiongrid', method=['POST', 'GET'])
@action('questiongrid/<path:path>', method=['POST', 'GET'])
@action.uses('questiongrid.html', session, db, flash, auth.user)
def questiongrid(path=None):
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4inline,
                         grid_class_style=GridClassStyleBootstrap5)
    # queries = [(db.event.id == db.question.eventid) & (db.event.projid == db.project.id)]
    qtype = request.query.get('qtype') if 'qtype' in request.query else session.get('qtype', 'quest')
    session['qtype'] = qtype
    queries = db.question.qtype == qtype
    eventlist = IS_NULL_OR(IS_IN_SET([x.event_name for x in db(db.event.id > 0).select(db.event.event_name,
                                                                                       orderby=db.event.event_name,
                                                                                       distinct=True)]))
    projlist = IS_NULL_OR(IS_IN_SET([x.proj_name for x in db(db.project.id > 0).select(db.project.proj_name,
                                                                                       orderby=db.project.proj_name,
                                                                                       distinct=True)]))

    search_queries = [['Search by Project', lambda val: db.project.proj_name == val, projlist],
                      ['Search by Event', lambda val: db.event.event_name == val, eventlist],
                      ['Search by Name', lambda val: db.question.questiontext.contains(val)]]

    if qtype == 'action':
        headings = ['Action', 'Status', 'Execstatus', 'Event', 'Project']
        fields = [db.question.questiontext, db.question.status, db.question.execstatus, db.event.event_name,
                  db.project.proj_name]
        orderby = [db.question.status, db.question.execstatus, db.question.questiontext]
    elif qtype == 'issue':
        headings = ['Issue', 'Status', 'Event', 'Project']
        fields = [db.question.questiontext, db.question.status, db.event.event_name,
                  db.project.proj_name]
        orderby = [db.question.status, db.question.questiontext]
    else:
        headings = ['Question', 'Answer', 'Status', 'Event', 'Project']
        fields = [db.question.questiontext, db.question.correctanstext, db.question.status, db.event.event_name,
                  db.project.proj_name]
        orderby = [db.question.status, db.question.questiontext]

    grid = Grid(path,
                queries,
                fields=fields,
                headings=headings,
                left=[db.event.on(db.question.eventid == db.event.id), db.project.on(db.event.projid == db.project.id)],
                search_queries=search_queries,
                orderby=orderby,
                create=URL('new_question/None/' + qtype),
                details=URL('viewquest/'),
                editable=URL('new_question/'),
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)


@action('datatables', method=['GET', 'POST'])
@action.uses('datatables.html', session, db, auth.user)
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


# Need to confirm final fields in datatable and grid and seem to lack a display_url
# Have left this in but not generally part of current solution py4web grid easier
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
    # queries = [(db.question.eventid == db.event.id) & (db.event.projid == db.project.id)]
    # if dtr.search_value and dtr.search_value != '':
    #    queries.append((db.question.questiontext.contains(dtr.search_value)) |
    #                  (db.question.responsible.contains(dtr.search_value)))

    query = reduce(lambda a, b: (a & b), queries)
    record_count = db(db.question.id > 0).count()
    filtered_count = db(query).count()

    DataTablesResponse(fields=[DataTablesField(name='DT_RowId', visible=False),
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
@action.uses('grid.html', session, db, auth.user)
def new_question_delete(questid):
    db(db.question.id == questid).delete()
    redirect(URL('datatables'))


@action('wolfram_alpha_lookup', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def wolfram_alpha_lookup():
    # This should be a straightforward function called via Ajax to lookup the answer to a question on wolfram alpha
    # and then return the answer
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
    # This should be a straightforward function called via Ajax to lookup the answer to a question on wikipedia
    # and return the answer
    qtext = request.json['questiontext']
    pages = wikipedia.search(qtext, results=3)
    try:
        resultpage = wikipedia.summary(pages[0])
    except wikipedia.exceptions.PageError:
        resultpage = None
    # print(resultpage)
    res = resultpage if resultpage else 'No result found for this topic'
    return res


@action('openai_lookup', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def openai_lookup():
    # This is called via Ajax to lookup the answer to a question on openai and return answer
    qtext = request.json['questiontext']
    scenario = request.json['scenario']
    setup = 'A'
    client = OpenAI(api_key=OPENAI_API_KEY)

    # example_messages = [
    #    {"role": "system", "content": "You are providing advice to make the world better "},
    #    {"role": "user", "content": qtext}
    # ]

    chosenai = db(db.knowledge.title == 'OpenAI GPT-3').select().first()
    messages = get_messages(chosenai.id, scenario, setup, qtext)
    for item in messages:
        print(type(item), item)
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages, max_tokens=300, temperature=0.1)

    resulttext = completion.choices[0].message.content
    return resulttext


@action('bard_lookup', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def bard_lookup():
    # This should be a straightforward function called via Ajax to lookup the answer to a question on openai
    # and then return the answer
    bard = Bard(token=_BARD_API_KEY)
    qtext = request.json['questiontext']
    answer = bard.get_answer(qtext)
    return answer['content']
