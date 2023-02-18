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

# This controller provides functions to create links between items

"""
    exposes:
    https://..../[app]/network/linkrequest - ajax call to create links
    https://..../[app]/network/ajaxquest - ajax call to create question with ajax
    https://..../[app]/network/graph - main d3 interactive graph
    https://..../[app]/network/no_questions - display if no questions
"""

import json
from ..d3js2py import getd3graph
from ..common import db, authenticated, auth, session
from py4web import request, redirect, URL


@authenticated()
def linkrequest():
    # this is called when a link is requested from the graph or event function
    # at present we are keeping limited audit trail on link requests - only last updater
    # and last action and the basic rule is that the last action cannot be repeated
    # we don't currently know if this function will also be used for deletions but
    # currently it won't as there is no action in the args only the source and target links
    # so action for now is to establish if the link already exists and if not create it
    # if it exists the number of requests increases and last user and action are updated.

    # now proposing to have an action as arg 3 which could be delete or agree
    # with link - this should be OK
    # and wil style the links a bit based on this too

    sourceid = request.json['sourceid']
    targetid = request.json['targetid']
    linkaction = request.json['action']

    # sourcerecs = db(db.question.questiontext == sourceid).select(db.question.id, orderby=~db.question.createdate)
    # targetrecs = db(db.question.questiontext == targetid).select(db.question.id, orderby=~db.question.createdate)

    responsetext = 'Item ' + str(sourceid) + ' linked with ' + str(targetid)
    query = (db.questlink.sourceid == sourceid) & (db.questlink.targetid == targetid)
    linkrows = db(query).select().first()

    if linkrows is None:
        db.questlink.insert(sourceid=sourceid, targetid=targetid)
        # Now also need to add 1 to the numagreement or disagreement figure
        # It shouldn't be possible to challenge unless resolved
        responsetext += ' Link Created'
    else:
        # link exists
        if linkaction == 'create':
            if linkrows.createdby == auth.user_id:
                responsetext = responsetext + ' ' + 'You updated last no change made'
            else:
                agrcount = linkrows.createcount + 1
                linkrows.update_record(createcount=agrcount)
        elif linkaction == 'delete':
            if linkrows.createdby == auth.user_id and linkrows.createcount == 1:
                db(db.questlink.id == linkrows.id).delete()
                responsetext = 'Link deleted'
            else:
                if linkrows.lastdeleter == auth.user_id:
                    responsetext = responsetext + ' ' + 'You deleted last no change made'
                else:
                    delcount = linkrows.deletecount + 1
                    if delcount >= linkrows.createcount:
                        status = 'Deleted'
                    else:
                        status = 'Active'
                    linkrows.update_record(lastaction='delete', deletecount=delcount, lastdeleter=auth.user_id,
                                           status=status)
                    responsetext = 'Deletion count updated'
    return responsetext


@authenticated()
def nodedelete():
    # this is called via ajax when a node deletion request is received from an eventmap
    # there are various situations to consider:
    # if you are the owner of the question and it is draft status then you may delete and it is a full deletion
    # if you are the event owner or the event is shared then you may delete any question from the event and
    # if this is not your own draft question then the question gets moved back to the unspecified event
    # if the event is not shared and you are not the event owner then you cannot delete anything
    # if event is shared and question is in draft status

    nodestring = request.json['nodeid']
    eventid = request.json['eventid']
    # action = request.json['action']

    if nodestring.isdigit():
        nodeid = int(nodestring)
    else:
        sourcetext = nodestring.replace("_", " ")  # This will do for now - other chars may be problem
        sourcerecs = db(db.question.questiontext == sourcetext).select(
            db.question.id, orderby=~db.question.createdate)
        if sourcerecs:
            nodeid = sourcerecs.first().id
        else:
            responsetext = 'Target of link could not be found'
            return responsetext

    if eventid == 0:
        responsetext = 'No event set node deletion not possible'
    else:
        quest = db(db.question.id == nodeid).select().first()
        if quest.auth_userid == auth.user_id and quest.status == 'Draft':
            db(db.questlink.sourceid == nodeid).delete()
            db(db.questlink.targetid == nodeid).delete()
            db(db.question.id == nodeid).delete()
            responsetext = 'Question deleted'
        else:
            responsetext = 'Question removed from event'
            unspecevent = db(db.event.event_name == 'Unspecified').select(db.event.id).first()
            db(db.question.id == nodeid).update(eventid=unspecevent['id'])
    return responsetext


@authenticated()
def ajaxquest():
    # this is called when a draft item is created on the graph
    # Only the item text will be received via ajax and the rest will
    # be added later by std form editing and that capability may be available via ajax as 
    # well at some point

    results = dict()
    if len(request.vars) < 1:
        # sourceid = request.args[0]
        # targetid = request.args[1]
        result = 'no variable passed so not creating item'
        results['result'] = result
        return json.dumps(results)

    itemtext = request.vars['itemtext']

    if request.vars['eventid']:
        eventid = int(request.vars['eventid'])
    else:
        eventid = db(db.event.event_name == 'Unspecified').select(db.event.id).first()['id']

    if auth.user is None:
        result = 'You must be logged in to create links'
        results['result'] = result
        return json.dumps(results)

    serverid = db.question.insert(questiontext=itemtext, status='Draft', eventid=eventid)
    result = 'Item created'

    results['serverid'] = serverid
    results['result'] = result
    results['id'] = request.vars['id']
    return json.dumps(results)


@authenticated()
def graph():
    """This is new interactive graph using D3 still very much work in progress mainly based on
    https://bl.ocks.org/cjrd/6863459
    but there have been a fair number of amendments to meet perceived needs"""
    #  This is currently loaded only by search but will probably also look to use this with newindex

    redraw = "true"
    numlevels = request.args(0, cast=int, default=1)
    basequest = request.args(1, cast=int, default=0)

    idlist = session.get('networklist') if session.get('networklist') else [basequest]

    if not idlist:
        redirect(URL('no_questions'))

    projid = 0
    eventrowid = 0

    quests, nodes, links, resultstring = getd3graph('search', idlist, 'open', numlevels)
    return dict(resultstring=resultstring, eventmap=quests, links=links, nodes=nodes, projid=projid,
                eventrowid=eventrowid, redraw=redraw, eventowner='false')


@authenticated()
def move():
    # This will allow moving the position of questions on an eventmap - but not on a general map at present
    # as no obvious way to save them - however think we will comment out the code if not authorised
    stdwidth = 1000
    stdheight = 1000

    questid = int(request.json['sourceid'])
    newxpos = int(request.json['sourceposx'])
    newypos = int(request.json['sourceposy'])

    # ensure xpos and ypos within range
    newxpos = max(0, min(newxpos, stdwidth))
    newypos = max(0, min(newypos, stdheight))
    questrec = db(db.question.id == questid).select().first()

    if auth.user is None:
        responsetext = 'You must be logged in to save movements'
    elif questrec.eventid == 0:
        responsetext = 'No event set - movements not saved'
    else:
        event = db((db.event.id == questrec.eventid) & (db.event.projid == db.project.id)).select().first()
        if event.event.status == 'Open' and (event.project.proj_shared == True or
                                             event.project.proj_owner == auth.user_id):
            questrec.update_record(xpos=newxpos, ypos=newypos)
            db.commit()
            responsetext = 'Element moved'
        else:
            if event.event.status != 'Open':
                responsetext = 'Move not saved - event is archiving and map cannot be changed'
            else:
                responsetext = 'Move not saved - you must be owner of ' + event.event_name + 'to save changes'
    return responsetext
