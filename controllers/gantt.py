# - Coding UTF8 -
#
# Networked Decision Making
# A framework for groups to make decisions asynchronously as asynchronous communication has proved highly
# successful and popular yet meetings persist for group decision making
#
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://www.netdecisionmaking.com/
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

# This controller provides gantt chart items

from ..ndsfunctions import get_gantt_data, update_action
from ..common import db, auth, session
from py4web import action, request, URL
from yatl.helpers import XML
from ..ndsqueries import get_items
import xml.etree.ElementTree as ET


@action("allgantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def allgantt():
    eventrow = None
    eid = None
    res_actions = get_items(event=eid, status='Resolved', execstatus='Incomplete')
    projxml = get_gantt_data(res_actions) if res_actions else "<project></project>"
    return dict(project=XML(projxml), quests=res_actions, eventrow=eventrow)


@action("gantt", method=['GET', 'POST'])
@action.uses('gantt.html', session, db, auth.user)
def gantt():
    eid = session.get('eventid', None)
    eventrow = None
    if eid:
        eventrow = db(db.event.id == eid).select().first()
        res_actions = get_items(event=eid, status='Resolved')
    else:  # only incomplete actions as too many otherwise
        res_actions = get_items(event=eid, status='Resolved', execstatus='Incomplete')
    projxml = get_gantt_data(res_actions) if res_actions else "<project></project>"
    # print(projxml)
    return dict(project=XML(projxml), quests=res_actions, eventrow=eventrow)


def process_gantt(xmlstring):
    myroot = ET.fromstring(xmlstring)
    # print(myroot)
    print(myroot.tag)
    print(myroot[0].attrib)
    print(myroot[1].tag)
    for child in myroot.iter():
        if child.tag == 'task':
            for element in child.iter():
                # so this seems to get what is required data wise
                # just need to figure out what elements we need - seems to be resource if that is mapped
                # to responsible on the way out plus % complete and start and end dates
                # should potentially be a shared function to update based on pcost being the id and these values
                #print(element.tag, element.text)
                match element.tag:
                    case 'pCost':
                        recid = element.text
                    case 'pRes':
                        resp = element.text
                    case 'pComp':
                        perc = element.text
                    case 'pStart':
                        startdate = element.text
                    case 'pEnd':
                        enddate = element.text
                    case _:
                        pass
            update_action(recid, resp, perc, startdate, enddate)
    return 'yes'


@action('exp_gantt', method=['POST', 'GET'])
@action.uses(session, db, auth.user)
def exp_gantt():
    # This will receive updates to the dates if users choose to save edits on the gantt chart
    ganttxml = request.json['ganttxml']
    if auth.user is None:
        return 'You must be logged in to save changes'
    responsetext = 'OK to update'
    # print(ganttxml)
    process_gantt(ganttxml)
    # questrows = db(db.question.id == qid).select()
    # quest = questrows.first()

    return responsetext
