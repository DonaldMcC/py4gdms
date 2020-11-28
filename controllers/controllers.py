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

"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from ..common import db, T,  auth, unauthenticated, authenticated

# make a "like" button factory
@authenticated.callback()
def agree(id):
    print(str(id)+'was called')
    #db.item_like.insert(item_id=id)


@authenticated()
def index():
    #user = auth.get_user()
    #message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = get_actions()
    questions = get_questions()
    issues = get_issues()
    return dict(actions=actions, questions=questions, issues=issues, agree=agree)


def get_actions(qtype='action', x=0, y=10):
    query=make_query(qtype)
    # TODO will request specific fields at some point and probably pass through datatable options eg search and so
    # forth
    sortby = ~db.question.id
    actions = db(query).select(orderby=[sortby], limitby=(x, y))
    return actions


def get_questions(x=0, y=10):
    query=make_query()
    questions = db(query).select(orderby=~db.question.id, limitby=(x, y))
    return questions


def get_issues(qtype='issue', x=0, y=10):
    query=make_query(qtype)
    issues = db(query).select(orderby=~db.question.id, limitby=(x, y))
    return issues


def make_query(qtype='quest'):
    if qtype=='quest':
        query = db.question.qtype=='quest'
    elif qtype == 'action':
        query = db.question.qtype=='action'
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




