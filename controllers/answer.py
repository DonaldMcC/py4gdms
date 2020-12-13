import datetime
from ..common import db, unauthenticated, authenticated, auth, session
from py4web import action, request, Flash
from ..ndsfunctions import score_question

# @action.uses(Template('index.html', delimiters='[[ ]]'))


@authenticated()
def quickanswer():
    """
    This willl provide a quick method of approving an action or issue by means of approve disapprove buttons
    basically needs to create a userquestion record and remove the buttons from the relevant row which
    may be more challenging - it will never apply to questions and there is a question about how scope changes and
    geography changes should be handled - but for now we are going to implicitly answer that these stay where they are
    and retrieve them from the question
    """

    questid = request.json['questid']
    answer = request.json['answer']
    print(questid + 'was called with answer ' + answer)
    uq = db((db.userquestion.questionid == questid) & (db.userquestion.auth_userid == auth.user_id)).select()
    status = 'In Progress'

    if not uq:
        uqid = db.userquestion.insert(questionid=questid, auth_userid=auth.user_id, answer=answer)
        messagetxt = 'Answer recorded for item:' + str(questid)
        status = score_question(questid, answer)
    elif uq:
        messagetxt = 'You have already answered this item'
    else:
        messagetxt = 'Answer not recorded'

    # TODO - will probably look to return a flashbar of some sort in a bit - but std flash looks like wont
    # work without eval or similar
    return messagetxt, status

@authenticated()
def perccomplete():
    """
    This updates percent complete on resolved actions
    """
    questid = request.json['questid']
    perccomplete = int(request.json['perccomplete'])
    resp = request.json['responsible']
    duestr = request.json['duedate']
    quest = db(db.question.id == questid).select().first()
    try:
        duedate = datetime.datetime.strptime(duestr, "%Y-%m-%d")
        quest.enddate = duedate
    except ValueError:
        pass

    quest.perccomplete = perccomplete
    quest.responsible = resp

    if perccomplete == 100:
        quest.execstatus = 'Completed'
    quest.update_record()
    db.commit()

    # TODO - will probably look to return a flashbar of some sort in a bit - but std flash looks like wont
    # work without eval or similar
    return


# make a "like" button factory
@authenticated.callback()
def agree(qid):
    print(str(qid) + 'was called')
    # db.item_like.insert(item_id=id)


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
#    title = 'Click to Answer'
#    title='Change Answer'


@authenticated()
def index():
    # user = auth.get_user()
    # message = T("Hello {first_name}".format(**user) if user else "Hello")
    actions = get_actions(status='In Progress')
    questions = get_questions(status='In Progress')
    issues = get_issues(status='In Progress')
    res_actions = get_actions(status='Resolved')
    return dict(actions=actions, questions=questions, issues=issues, agree=agree, res_actions=res_actions,
                get_class=get_class, get_disabled=get_disabled)


def get_actions(qtype='action', status='', x=0, y=10):
    query = make_query(qtype, status)
    # TODO will request specific fields at some point and probably pass through datatable options eg search and so on
    # forth
    sortby = ~db.question.id
    actions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                               orderby=[sortby], limitby=(x, y))
    return actions


def get_questions(qtype='quest', status='', x=0, y=10):
    query = make_query(qtype, status)
    questions = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                                 orderby=~db.question.id, limitby=(x, y))
    return questions


def get_issues(qtype='issue', status='', x=0, y=10):
    query = make_query(qtype, status)
    issues = db(query).select(left=db.userquestion.on(db.question.id == db.userquestion.questionid),
                              orderby=~db.question.id, limitby=(x, y))
    return issues


def make_query(qtype='quest', status=''):
    if qtype == 'quest':
        query = (db.question.qtype == 'quest')
    elif qtype == 'action':
        query = (db.question.qtype == 'action') & (db.question.execstatus != 'Completed')
    else:
        query = (db.question.qtype == 'issue')
    if status:
        query &= (db.question.status == status)
    return query
