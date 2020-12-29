from .common import db

def get_disabled(ans, useranswer):
    return 'disabled title=You_already_answered ' if ans == useranswer else ' title=Click_to_Answer '


def get_class(qtype='quest', answer=1, framework='Bulma'):
    # Function to return button classes - only supporting Bulma.css for now
    # is-success and is-danger for agree disagree on issues and approve disapprove on actions
    default = 'button is-small is-rounded '
    if qtype == 'quest':
        return default
    else:
        if answer == 1:
            return default + ' is-success'
        else:
            return default + ' is-danger'

def get_actions(qtype='action', status=None, x=0, y=10, event=None):
    query = make_query(qtype, status, event)
    # TODO will request specific fields at some point and probably pass through datatable options eg search and so on
    # forth
    sortby = ~db.question.id
    actions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                               orderby=[sortby], limitby=(x, y))
    return actions


def get_questions(qtype='quest', status=None, x=0, y=10, event=None):
    query = make_query(qtype, status, event)
    questions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                                 orderby=~db.question.id, limitby=(x, y))
    return questions


def get_issues(qtype='issue', status=None, x=0, y=10, event=None):
    query = make_query(qtype, status, event)
    issues = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                              orderby=~db.question.id, limitby=(x, y))
    return issues


def make_query(qtype='quest', status=None, event=None):
    if qtype == 'quest':
        query = (db.question.qtype == 'quest')
    elif qtype == 'action':
        query = (db.question.qtype == 'action') & (db.question.execstatus != 'Completed')
    else:
        query = (db.question.qtype == 'issue')
    if status:
        query &= (db.question.status == status)
    if event:
        query &= (db.question.eventid == event)
    return query
