# - Coding UTF8 -
#
# Networked Decision Making
# A framework for groups to make decisions asynchronously as asynchronous communication has proved highly
# successful and popular yet meetings persist for group decision making
#
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://www.netdecisionmaking.com/nds
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

"""
 This controller handles viewing the full details on questions if allowed
 and also displaying the reason you are not allowed to view the question
 the functionality to submit a challenge is also included in this controller
 and that is called via ajax from the view of the question detail
 The three functions are:
 index:  displays the question details
 comments: add comments - not yet implemented in py4web
 useranswers: shows detail of the useranswers - probably not going to be implemented as no reasons now included
 notshowing: explains why the question can't be displayed - actions should always be displayed
 challenge: allows submission of a challenge and return of whether this is allowed
 via ajax
 challenge - ajax submission to challenge
 urgency - ajax update urgency of item - this has moved to answer.py

 For actions not generally interested in user's views but would like these to be capable
 of prioritisation at any stage - need to see the date and will be some options to generate
 emails based on actions and also to challenge resolved actions to return them to proposed
 A separate comments function has now been created

    exposes:
    https://..../[app]/viewquest/index which has action, issue and question views
    https://..../[app]/viewquest/notshowing
    https://..../[app]/viewquest/comments
    https://..../[app]/viewquest/flagcomment  #  Ajax call
    https://..../[app]/viewquest/urgency  #  Ajax call
    https://..../[app]/viewquest/importance  #  Ajax call
    """

import os
from ..common import db, auth, session
from yatl.helpers import XML
from py4web import action, request, redirect, URL
from py4web.utils.form import Form, FormStyleBootstrap4
from ..ndsqueries import get_class, get_disabled
from ..ndsfunctions import get_filetype, qtypename, myconverter
from ..d3js2py import getd3graph
from py4web.utils.factories import Inject
from ..markmin.markmin2html import markmin2html


@action("viewquest/<qid>", method=['GET', 'POST'])
@action("viewquest/<qid>/<eid>", method=['GET', 'POST'])
@action('viewquest', method=['POST', 'GET'])
@action.uses('viewquest.html', session, db, auth.user, Inject(markmin2html=markmin2html))
def viewquest(qid=0, eid=0):
    # This will be a general view on question details and it will require the
    # question id as an argument Logic will be to only display the question if it
    # has been submitted, resolved or answered/passed by the user
    # This maintains the general privacy approach to questions that may be
    # subject to answer eventually if resolved then there will be a view option
    # However approach for actions is different - they can be viewed at any time
    # but the buttons at the bottom should be very similar

    uqrated = False
    filename = ''
    urlpath = ''
    filetype = None
    anstext = ''
    viewtext = ''
    uq = None
    ur = None
    uqanswered = False
    urgmessage = ''
    can_edit = False
    chosenai = ''

    quests = db(db.question.id == qid).select()
    quest = quests.first() if quests else redirect(URL('index'))
    if quest.question_media:
        (filename, fullname) = db.question.question_media.retrieve(quest.question_media, nameonly=True)
        urlpath = r'static/uploads/' + os.path.basename(fullname)
        filetype = get_filetype(filename)
    qname = qtypename(quest.qtype)

    if auth.user:
        uqs = db((db.userquestion.auth_userid == auth.user_id) & (db.userquestion.questionid == quest.id)).select()
        uq = uqs.first() if uqs else None
        uqanswered = True if uq else False
        uqrates = db((db.uqrating.auth_userid == auth.user_id) & (db.uqrating.questionid == quest.id)).select()
        ur = uqrates.first() if uqrates else None
        uqrated = True if ur else False
        if uqrated:
            urgmessage = "You and others people have rated urgency and importance below - you can update if required."
        else:
            urgmessage = "Other people have rated urgency and importance below - you have yet to do so."
        if auth.user_id == quest.auth_userid:  # owner can edit for now - may lock if answered
            can_edit = True

    # Now work out what we can say about this question
    # if resolved we can say if right or wrong and allow the question to be challenged
    if quest['status'] == 'Resolved':
        chosenai = quest.chosenai.title if quest.chosenai else 'Not Known'
        if quest['factopinion'] == 'Fact':
            anstext = f"Submitter or knowledge engines claim the answer is: {quest['answertext']}"
        else:
            correcttext = (quest['correctans'] == 1 and quest['answer1']) or (
                quest['correctans'] == 2 and quest['answer2']) or '?'
            anstext = f'Users have decided the correct answer is  {correcttext}'
            # Did the user answer the question
            if uqanswered:
                if quest['correctans'] == uq.answer:
                    viewtext = f'Well done - you helped with this {qname}'
                else:
                    viewtext = f'Your answer to this {qname} disagrees with the consensus.'
            else:
                viewtext = f"You haven't answered this {qname} yet."
    elif quest['status'] == 'Rejected':
        viewtext = f"This {qname} has been rejected."
    else:
        viewtext = f'This {qname} is in progress.'
        # That will do for now - display of challenges and probably numanswers remaining and level can be added later

    # need to get priorquests and subsquests as lists which may be empty for each quest now
    priorquestrows = db(db.questlink.targetid == quest.id).select(db.questlink.sourceid)
    subsquestrows = db(db.questlink.sourceid == quest.id).select(db.questlink.targetid)
    priorquests = [row.sourceid for row in priorquestrows]
    subsquests = [row.targetid for row in subsquestrows]
    eid = quest['eventid']
    editable = 'false'  # don't think we can use this on items as could be cross project or event
    quests, nodes, links, resultstring = getd3graph('quest', quest.id, 'Open', 1, 1, 0)

    # new section to cover ai_review of item - thinking now is that all items will be subject to AI review - however
    # may need a setting to turn this off for testing as could slow down and a bit pointless
    # so actions would be to find the latest AI_Review - for now there may only be 1 but
    # there may well be triggers to resubmit in due course so we will get the latest one by date for now
    # I think if there isn't one then we will generate via async function after displaying the question
    # so probably return AI_lookup type value for this if not found and setting not to not lookup

    query = ((db.ai_review.parentid == quest.id) & (db.ai_review.status == 'Active') &
             (db.ai_review.parenttable == 'question'))
    sortby = ~db.ai_review.reviewdate
    ai_comment = db(query).select(orderby=[sortby]).first()

    got_ai = "Yes" if ai_comment else "No"

    db.comment.auth_userid.default = auth.user_id
    db.comment.parentid.default = quest['id']
    commentform = Form(db.comment, formstyle=FormStyleBootstrap4)

    return dict(quest=quest, viewtext=viewtext, uqanswered=uqanswered, uq=uq, urgmessage=urgmessage,
                priorquests=priorquests, subsquests=subsquests, get_class=get_class, get_disabled=get_disabled, ur=ur,
                uqrated=uqrated, can_edit=can_edit, commentform=commentform, filetype=filetype,
                filename=filename, urlpath=urlpath, anstext=anstext, qname=qname, chosenai=chosenai,
                eventowner=editable, eventid=eid, projid=0, nodes=nodes, links=links, redraw='true',
                myconverter=myconverter, ai_comment=ai_comment, got_ai=got_ai)


@action('urgency', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def urgency():
    # This allows users to record or update their assessment of the urgency or
    # importance of an action as this helps with prioritising the actions that
    # are required - next step is to attempt to get the view sorted and will
    # retrieve this as part of main index controller

    qid = int(request.json['questid'])
    urg = int(request.json['urgency'])
    if auth.user is None:
        return 'You must be logged in to record urgency'

    questrows = db(db.question.id == qid).select()
    quest = questrows.first()
    totratings = quest.totratings or 0

    # find out if user has rated the question already
    qcs = db((db.uqrating.auth_userid == auth.user_id) & (db.uqrating.questionid == qid)).select()
    qc = qcs.first() if qcs else None

    if not qc:
        db.uqrating.insert(questionid=qid, auth_userid=auth.user_id, urgency=urg)
        responsetext = 'Your assessment has been recorded'
        totratings += 1
    else:
        qc.update_record(urgency=urg)
        responsetext = 'Your assessment has been updated'

    urgent = (((quest.urgency * totratings) + urg) / (totratings + 1))
    db(db.question.id == qid).update(urgency=urgent, totratings=totratings)
    return responsetext


@action('importance', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def importance():
    # This allows users to record or update their assessment of the urgency or
    # importance of an action as this helps with prioritising the actions that
    # are required - next step is to attempt to get the view sorted and will
    # retrieve this as part of main index controller

    qid = int(request.json['questid'])
    imp = int(request.json['importance'])
    if auth.user is None:
        return 'You must be logged in to record urgency'

    questrows = db(db.question.id == qid).select()
    quest = questrows.first()
    totratings = quest.totratings or 0

    # find out if user has rated the question already
    qcs = db((db.uqrating.auth_userid == auth.user_id) & (db.uqrating.questionid == qid)).select()
    qc = qcs.first() if qcs else None

    if not qc:
        db.uqrating.insert(questionid=qid, auth_userid=auth.user_id, importance=imp)
        responsetext = 'Your assessment has been recorded'
        totratings += 1
    else:
        qc.update_record(importance=imp)
        responsetext = 'Your assessment has been updated'

    importnce = (((quest.importance * totratings) + imp) / (totratings + 1))
    db(db.question.id == qid).update(importance=importnce, totratings=totratings)
    return responsetext
