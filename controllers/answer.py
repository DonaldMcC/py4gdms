import datetime
from ..common import db, authenticated, auth, session
from py4web import action, request, Flash
from ..ndsfunctions import score_question
from ..ndsqueries import get_class, get_disabled, get_items
flash = Flash()


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
    if uq:
        return 'You already answered this one'
    db.userquestion.insert(questionid=questid, auth_userid=auth.user_id, answer=answer)
    messagetxt = 'Answer recorded for item:' + str(questid) + ' '
    status = score_question(questid, answer)
    messagetxt += status
    return messagetxt


@action('perccomplete', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def perccomplete():
    """
    This updates resolved actions only for responsible person, due date and % complete
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
@action.uses(flash)
def like(itemid, table='question'):
    # TODO disable button or change to unlike on initial like via js and get the flash working via
    alreadyliked = db((db.itemlike.parentid == itemid) & (db.itemlike.parenttable == table) &
                      (db.itemlike.createdby == auth.user_id)).select()
    if alreadyliked:
        flash.set("You Already liked this one", sanitize=True)
    else:
        db.itemlike.insert(parentid=itemid, parenttable=table, createdby=auth.user_id)
        if table == 'question':
            liked_item = db(db.question.id == itemid).select().first()
            likecount = liked_item.numlike + 1
            liked_item.update_record(numlike=likecount)
            db.commit()
        flash.set("Like Recorded", sanitize=True)
    return dict()


@action('index', method=['POST', 'GET'])
@action('index/<qtype>', method=['POST', 'GET'])
@action('index/<qtype>/<qid>', method=['POST', 'GET'])
@action.uses(session, db, auth, 'index.html')
def index(qtype=None, qid=None):
    qid = int(qid) if qid and qid.isnumeric() else None

    actions = get_items(qtype='action', status='In Progress') if (qtype == 'actions' or qtype == None) else None
    questions = get_items(qtype='quest', status='In Progress') if (qtype == 'questions' or qtype == None) else None
    issues = get_items(qtype='issue', status='In Progress') if (qtype == 'issues' or qtype == None) else None
    res_actions = get_items(status='Resolved') if (qtype == 'resactions' or qtype == None) else None

    return dict(actions=actions, questions=questions, issues=issues, res_actions=res_actions,
                get_class=get_class, get_disabled=get_disabled, auth=auth, like=like)
