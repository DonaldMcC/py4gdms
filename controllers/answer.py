import datetime
from ..common import db, authenticated, auth, session
from py4web import action, request
from ..ndsfunctions import score_question
from ..ndsqueries import get_class, get_disabled, get_items


@action('quickanswer', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
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
        messagetxt += status
    elif uq:
        messagetxt = 'You already answered this one'
    else:
        messagetxt = 'Answer not recorded'

    return messagetxt


@action('perccomplete', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def perccomplete():
    """
    This updates percent complete on resolved actions
    """
    questid = request.json['questid']
    percentcomplete = int(request.json['perccomplete'])
    resp = request.json['responsible']
    duestr = request.json['duedate']
    quest = db(db.question.id == questid).select().first()

    try:
        duedate = datetime.datetime.strptime(duestr, "%Y-%m-%d")
        quest.enddate = duedate
    except ValueError:
        pass

    quest.perccomplete = percentcomplete
    quest.responsible = resp

    if perccomplete == 100:
        quest.execstatus = 'Completed'
    quest.update_record()
    db.commit()
    return 'Action updated to ' + str(percentcomplete)


# make a "like" button factory
@authenticated.callback()
def agree(qid):
    print(str(qid) + 'was called')
    # db.item_like.insert(item_id=id)


@action('index', method=['POST', 'GET'])
@action('index/<qtype>', method=['POST', 'GET'])
@action.uses(session, db, auth, 'index.html')
def index(qtype=None):
    actions = get_items(qtype='action', status='In Progress') if (qtype == 'actions' or qtype == None) else None
    questions = get_items(qtype='quest', status='In Progress') if (qtype == 'questions' or qtype == None) else None
    issues = get_items(qtype='issue', status='In Progress') if (qtype == 'issues' or qtype == None) else None
    res_actions = get_items(status='Resolved') if (qtype == 'resactions' or qtype == None) else None
    return dict(actions=actions, questions=questions, issues=issues, agree=agree, res_actions=res_actions,
                get_class=get_class, get_disabled=get_disabled, auth=auth)
