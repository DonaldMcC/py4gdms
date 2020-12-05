# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#   http://netdecisionmaking.com/gdmsdemo/
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


# This controller provides details about network decision making
# and access to the FAQ

"""
    exposes:
    http://..../[app]/about/index
    http://..../[app]/about/privacy
    http://..../[app]/about/faq
    http://..../[app]/about/present
    http://..../[app]/about/enhance
    http://..../[app]/about/stdmsg
    http://..../[app]/about/download
    http://..../[app]/about/getfile

    """

from ..common import db, unauthenticated, authenticated, auth, session
from py4web import action, request, Flash
from ..ndsfunctions import score_question


@action("quickanswer", method=['POST'])
@action.uses(session, db, auth, Flash)
def quickanswer():
    """
    This willl provide a quick method of approving an action or issue by means of approve disapprove buttons
    basically needs to create a userquestion record and remove the buttons from the relevant row which
    may be more challenging - it will never apply to questions and there is a question about how scope changes and
    geography changes should be handled - but for now we are going to implicitly answer that these stay where they are
    and retrieve them from the question
    """
    print('qickans called')
    questid = request.json['questid']
    answer = request.json['answer']
    print(questid + 'was called with answer ' + answer)
    uq = db((db.userquestion.questionid == questid) & (db.userquestion.auth_userid == auth.user_id)).select()

    if not uq:
        uqid = db.userquestion.insert(questionid=questid, auth_userid=auth.user_id, answer=answer)
        messagetxt = 'Answer recorded for item:' + str(questid)
        status = score_question(questid, answer)
    elif uq:
        messagetxt = 'You have already answered this item'
    else:
        messagetxt = 'Answer not recorded'

    # TODO - will probalby look to return a flashbar of some srot in a bit - but std flash looks like wont
    # work without eval or similar
    return messagetxt


# make a "like" button factory
@authenticated.callback()
def agree(id):
    print(str(id)+'was called')
    # db.item_like.insert(item_id=id)


@authenticated()
def index():
    # user = auth.get_user()
    # message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = get_actions()
    questions = get_questions()
    issues = get_issues()
    return dict(actions=actions, questions=questions, issues=issues, agree=agree)


def get_actions(qtype='action', x=0, y=10):
    query=make_query(qtype)
    # TODO will request specific fields at some point and probably pass through datatable options eg search and so
    # forth
    sortby = ~db.question.id
    actions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                                orderby=[sortby], limitby=(x, y))
    return actions


def get_questions(x=0, y=10):
    query=make_query()
    questions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                orderby=~db.question.id, limitby=(x, y))
    return questions


def get_issues(qtype='issue', x=0, y=10):
    query=make_query(qtype)
    issues = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                               orderby=~db.question.id, limitby=(x, y))
    return issues


def make_query(qtype='quest'):
    if qtype == 'quest':
        query = db.question.qtype == 'quest'
    elif qtype == 'action':
        query = db.question.qtype == 'action'
    else:
        query = db.question.qtype == 'issue'
    return query


@unauthenticated()
def about():
    return dict(message="all done in the view")


@unauthenticated()
def privacy():
    return dict(message="all done in the view")


@unauthenticated()
def faq():
    return dict(message="all done in the view")


@unauthenticated()
def present():
    return dict(message="all done in the view")


@unauthenticated()
def enhance():
    return dict(message="all done in the view")


@unauthenticated()
def download():
    downloads = db().select(db.download.ALL, orderby=db.download.title)
    return dict(downloads=downloads)
