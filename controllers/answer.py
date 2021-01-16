import datetime
from ..common import db, unauthenticated, authenticated, auth, session
from py4web import action, request, Flash
from ..ndsfunctions import score_question
from ..ndsqueries import get_questions, get_issues, get_actions, get_class, get_disabled


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
    uq = db((db.userquestion.questionid == questid) & (db.userquestion.auth_userid == auth.user_id)).select()

    if not uq:
        uqid = db.userquestion.insert(questionid=questid, auth_userid=auth.user_id, answer=answer)
        messagetxt = 'Answer recorded for item:' + str(questid)
        status = score_question(questid, answer)
        messagetxt+=status
    elif uq:
        messagetxt = 'You already answered this one'
    else:
        messagetxt = 'Answer not recorded'

    return messagetxt


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
    return()


# make a "like" button factory
@authenticated.callback()
def agree(qid):
    print(str(qid) + 'was called')
    # db.item_like.insert(item_id=id)


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
