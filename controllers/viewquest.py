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
    http://..../[app]/viewquest/index which has action, issue and question views
    http://..../[app]/viewquest/notshowing
    http://..../[app]/viewquest/comments
    http://..../[app]/viewquest/flagcomment  #  Ajax call
    http://..../[app]/viewquest/urgency  #  Ajax call
    http://..../[app]/viewquest/importance  #  Ajax call
    """

from ..common import db, auth, session
from py4web import action, request, redirect, URL
from py4web.utils.form import Form, FormStyleBulma
from ..ndsqueries import get_class, get_disabled


# For now not using this - everything is open
def can_view(status, qtype,  hasanswered, userid, owner):
    """Will be some doctests on this in due course and a table of condtions
    Basic rules are that for votes users can't see questions that they haven't answered
    vote style questions can be seen after expiry and never before and users can never see
    questions for groups they don't belong to.
    """

    viewable = False
    message = ''
    reason = 'OK to view'

    if userid == owner:  # think always allow owners to view questions whether votes or not
        viewable = True
    elif (status == 'In Progress' or status == 'Draft') and hasanswered is False:
        message = "You can't view this question as it's not resolved and you haven't answered it."
        reason = 'NotAnswered'
    else:
        viewable = True
    return viewable, reason, message


@action("viewquest/<qid>", method=['GET', 'POST'])
@action('viewquest', method=['POST', 'GET'])
@action.uses(session, db, auth.user, 'viewquest.html')
def viewquest(qid=0):
    # This will be a general view on question details and it will require the
    # question id as an argument Logic will be to only display the question if it
    # has been submitted, resolved or answered/passed by the user
    # This maintains the general privacy approach to questions that may be
    # subject to answer eventually if resolved then there will be a view option
    # However approach for actions is different - they can be viewed at any time
    # but the buttons at the bottom should be very similar

    # initialize variables as not used if action
    uqrated = False

    quests = db(db.question.id == qid).select() or redirect(URL('notshowing/' + 'NoQuestion'))
    quest = quests.first()
    uq = None
    ur = None
    uqanswered = False
    urgmessage = ''
    can_edit = False

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
        # Did the user answer the question
        if uqanswered:
            if quest['correctans'] == uq.answer:
                viewtext = 'Well done - you helped resolve this question.'
            else:
                viewtext = 'Your answer to this question disagrees with the resolved '
                'correct answer - you may want to request a challenge.'
        else:
            viewtext = "You haven't answered this question yet."
    elif quest['status'] == 'Rejected':
        viewtext = "This question has been rejected."
    else:
        # if not resolved can only say in progress and how many more answers are required
        # at present should only be here if
        # answered as we are not showing users unresolved and unanswered questions
        viewtext = 'This question is in progress.'
        # That will do for now - display of challenges and probably numanswers remaining
        # and level can be added later

    # need to get priorquests and subsquests as lists which may be empty for each quest now
    priorquestrows = db(db.questlink.targetid == quest.id).select(db.questlink.sourceid)
    subsquestrows = db(db.questlink.sourceid == quest.id).select(db.questlink.targetid)
    priorquests = [row.sourceid for row in priorquestrows]
    subsquests = [row.targetid for row in subsquestrows]

    commentform = Form(db.comments,  formstyle=FormStyleBulma)
    return dict(quest=quest, viewtext=viewtext, uqanswered=uqanswered, uq=uq, urgmessage=urgmessage,
                priorquests=priorquests, subsquests=subsquests, get_class=get_class, get_disabled=get_disabled, ur=ur,
                uqrated=uqrated, can_edit=can_edit, commentform=commentform)


# TODO - think will add this in some manner at some point -but below is web2py version
def comments():
    # This will be a general view on question comments it will require the
    # question id as an argument Logic will be to only display the comements if it
    # has been resolved
    # This maintains the general privacy approach to questions that may be
    # subject to answer eventually if resolved then there will be a view option
    # this needs the as_dict() treatment as well but lets debug viewquest first
    # and then do next - potentially this can be replaced with a plugin

    questid = request.args(0, cast=int, default=0) or redirect(URL('default', 'index'))

    session.questid = questid
    quest = db.question[questid]

    if quest is None:
        redirect(URL('viewquest', 'notshowing/' + 'NoQuestion'))

    return dict(quest=quest)


def notshowing():
    questid = request.args(1)
    shortreason = request.args(0)

    if shortreason == 'NotResolved':
        reason = "This question is not yet resolved and you haven't answered it"
    elif shortreason == 'NotAnswered':
        reason = 'You have not answered this question'
    elif shortreason == 'NotInGroup':
        reason = 'You do not have permission to view this item'
    elif shortreason == 'VoteInProg':
        quest = db(db.question.id == questid).select(db.question.duedate).first()
        reason = "Vote is still in progress so you can't see results. The vote concludes at " + str(quest.duedate)
    elif shortreason == 'NoQuestion':
        reason = 'This question does not exist'
    else:
        reason = 'Not Known'
    return dict(reason=reason, questid=questid, shortreason=shortreason)


# not yet setup - below is w2p version
def challenge():
    # This allows users to challenge resolved questions - whether or not they have answered them - users are not
    # allowed to challenge questions that are not currently in a state of resolved and this should be done by the
    # viewquestion function rather than the challenge ie option isn't available if question isn't resolved - actions
    # are similar and would only be challenged once they are in a state of Agreed

    chquestid = request.args[0]
    if auth.user is None:
        responsetext = 'You must be logged in to challenge a question'
    else:
        # find out if user has previously challenged the question - this will be a userchallenge record
        qcs = db((db.questchallenge.auth_userid == auth.user.id) & (db.questchallenge.questionid == chquestid)).select()
        qc = qcs.first()
        if qc is None:
            db.questchallenge.insert(questionid=chquestid, auth_userid=auth.user.id,
                                     challengereason=request.vars.challreason)
            # Now also need to add 1 to the numchallenges figure - I think this will reset when back to resolved and
            # It shouldn't be possible to challenge unless resolved
            questrows = db(db.question.id == chquestid).select()
            quest = questrows.first()
            numchallenges = quest.othercounts
            numchallenges[1] += 1
            newlevel = quest.question_level
            status = quest.status
            challenge = False
            if numchallenges[1] >= 3:
                numchallenges[2] += 1
                newlevel = quest.question_level + 2
                status = 'In Progress'
                challenge = True
            db(db.question.id == chquestid).update(status=status, question_level=newlevel, othercounts=numchallenges,
                                                   challengedate=request.utcnow, urgency=quest.urgency,
                                                   importance=quest.importance, challenge=challenge)
            responsetext = 'Challenge accepted'
        else:
            responsetext = 'You have already challenged this question and only 1 challenge is allowed at present'
    return 'jQuery(".w2p_flash").html("' + responsetext + '").slideDown().delay(1500).slideUp();' \
                                                          ' $("#target").html("' + responsetext + '");'


def flagcomment():
    # This allows users to record if they think a comment is inappropriate
    # if 3 separate users flag the comment then it is removed from display
    # permanently for now

    commentid = request.args[0]
    requesttype = request.args[1]

    if auth.user is None:
        responsetext = 'You must be logged in to flage inappropriate comments'
    else:
        comment = db(db.questcomment.id == commentid).select().first()

        if requesttype != 'admin':
            # check if user has previously challenged the question -
            # this will be an entry in the usersreject field

            if comment.usersreject is not None and auth.user.id in comment.usersreject:
                responsetext = 'You have already flagged this comment'
            else:
                responsetext = 'Rejection recorded'
                comment.numreject += 1
                if comment.usersreject is not None:
                    comment.usersreject.append(auth.user.id)
                else:
                    comment.usersreject = [auth.user.id]
                if comment.numreject > 2:
                    comment.status = 'NOK'
                comment.update_record()
        else:
            responsetext = 'Admin hide successful'
            comment.update_record(status='NOK')
    return responsetext


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
