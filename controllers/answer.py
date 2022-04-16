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

# This controller includes the default index function and other functions for answering questions
# and liking items

import datetime

from py4web import action, request, Flash
from ..common import db, auth, session
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

    if percentcomplete == 100:
        quest.execstatus = 'Completed'
    elif percentcomplete > 0:
        quest.execstatus = 'In Progress'
    else:
        quest.execstatus = 'Proposed'

    quest.update_record()
    db.commit()
    return 'Action updated to ' + str(percentcomplete)


@action('like/<itemid>', method=['POST', 'GET'])
@action.uses(session, db, auth)
def like(itemid, table='question'):
    alreadyliked = db((db.itemlike.parentid == itemid) & (db.itemlike.parenttable == table) &
                      (db.itemlike.createdby == auth.user_id)).select()
    numlikes = ''
    if alreadyliked:
        newbutton = 'Like'
        db((db.itemlike.parentid == itemid) & (db.itemlike.parenttable == table) &
           (db.itemlike.createdby == auth.user_id)).delete()
    else:
        db.itemlike.insert(parentid=itemid, parenttable=table, createdby=auth.user_id)
        newbutton = 'Unlike'
    if table == 'question':
        liked_item = db(db.question.id == itemid).select().first()
        likecount = liked_item.numlike - 1 if alreadyliked else liked_item.numlike + 1
        liked_item.update_record(numlike=likecount)
        numlikes = '<div id="btns{}" hx-swap-oob="true"> <sub>Likes:{}</sub></div>'.format(itemid, likecount)
    db.commit()
    return numlikes + newbutton


@action('index', method=['POST', 'GET'])
@action('index/<qtype>', method=['POST', 'GET'])
@action('index/<qtype>/<qid>', method=['POST', 'GET'])
@action.uses('index.html', flash, session, db, auth)
def index(qtype=None, qid=None):
    qid = int(qid) if qid and qid.isnumeric() else None
    qactions = get_items(qtype='action', status='In Progress', qid=qid) if (
            qtype == 'actions' or qtype == None) else None
    questions = get_items(qtype='quest', status='In Progress', qid=qid) if (
            qtype == 'questions' or qtype == None) else None
    issues = get_items(qtype='issue', status='In Progress', qid=qid) if (
            qtype == 'issues' or qtype == None) else None
    res_actions = get_items(status='Resolved', qid=qid, execstatus='Incomplete') if (
            qtype == 'resactions' or qtype == None) else None
    comp_actions = get_items(status='Resolved', qid=qid, execstatus='Completed') if (
            qtype == 'resactions' or qtype == None) else None
    actions = {"allowed_actions": auth.param.allowed_actions}
    return dict(actions=actions, qactions=qactions, questions=questions, issues=issues, res_actions=res_actions,
                comp_actions=comp_actions, get_class=get_class, get_disabled=get_disabled, auth=auth, like=like)
