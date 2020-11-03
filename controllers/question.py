# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#


from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated


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
