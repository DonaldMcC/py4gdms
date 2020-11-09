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

@action("new_question/<questid>", method=['GET', 'POST'])
@action("new_question", method=['GET', 'POST'])
@action.uses('new_question.html', session, db)
def new_question(questid='0'):
    # TODO find out how request.args works with bottle prob different
    # qtype = request.args(0, default='quest')
    #questid = request.url_args(0, cast=int, default=0)
    print('arg'+str(questid))
    form = Form([db.question.questiontext,
                 db.question.factopinion,
                 db.question.answertext,
                 db.question.answer1,
                 db.question.answer2])

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

    queries = [(db.question.id > 0)]

    search_queries = [['Search by Name', lambda value: db.question.questiontext == value]]

    #search = GridSearch(search_queries, queries)

    grid = Grid(path,
                db.question,
                fields=fields,
                left=[db.evt.on(db.question.eventid == db.evt.id),
                      db.project.on(db.question.projid == db.project.id)],
                headings=['Type', 'Status', 'Text', 'Fact_Opinion', 'Answer1', 'Answer2', 'Answertext',
                          'Resolvemethod', 'Event', 'Project'],
                orderby=orderby,
                search_queries=search_queries,
                create=True,
                details=True,
                editable=True,
                deletable=True,
                **GRID_DEFAULTS)

    return dict(grid=grid)



@action("new_action", method=['GET', 'POST'])
@action.uses('new_question.html', session, db)
def new_action():
    #form.vars.answers = ['Approve', 'Disapprove']

    # TODO need to make label dynamic
    form = Form([db.question.questiontext,
                 db.question.responsible,
                 db.question.startdate,
                 db.question.enddate])

    return dict(form=form)


@action("new_issue", method=['GET', 'POST'])
@action.uses('new_question.html', session, db)
def new_issue():
    #form.vars.answers = ['Agree', 'Disagree']
    # TODO need to make label dynamic
    # Sticking with approach that you don't get to grade your own issues for urgency and importance at creation
    form = Form([db.question.questiontext])

    return dict(form=form)
