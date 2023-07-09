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
# Also visit: www.web2py.com
# or Groups: http://groups.google.com/group/web2py
# For details on the web framework used for this development
#
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be

import os
import datetime
from yatl.helpers import XML
from py4web import URL
from .common import db


def qtypename(item):
    return 'question' if item == 'quest' else item


def get_filetype(filename):
    # print(filename)
    not_used, file_extension = os.path.splitext(filename)
    ext = file_extension.lower()
    # print(ext)
    if ext == '.jpg' or ext == '.jpeg':
        return 'image'
    elif ext == '.mp4':
        return 'video/mp4'
    elif ext == '.mp3' or ext == '.wav':
        return 'audio/mpeg'
    # print(ext)
    return None


def convxml(value, tag, sanitize=False, trunc=False, trunclength=40):
    value = str(value)
    value = value.replace('\n', ' ').replace('\r', '')
    if trunc:
        value = truncquest(value, trunclength, wrap=0, mark=False)
    return '<' + tag + '>' + XML(str(value), sanitize=sanitize) + '</' + tag + '>'


def convrow(row, dependlist='', hasdepend=False):
    # pDepend is a list of taskst that this item depends upon
    # pLink will be the url to edit the action which can be derived from the row id
    # expect dependlist will need to be stripped
    colorclass = gantt_colour(row.question.startdate, row.question.enddate, row.question.perccomplete)
    if row.question.startdate == row.question.enddate:
        milestone = 1
    else:
        milestone = 0
    plink = URL('submit', 'question_plan')
    projrow = '<task>'
    projrow += convxml(row.question.id, 'pID')
    projrow += convxml(row.question.questiontext, 'pName', True, False)
    projrow += convxml(row.question.startdate, 'pStart')
    projrow += convxml(row.question.enddate, 'pEnd')
    projrow += convxml(colorclass, 'pClass')
    projrow += convxml(plink, 'pLink')
    projrow += convxml(milestone, 'pMile')
    projrow += convxml(row.question.responsible, 'pRes', True)
    projrow += convxml(row.question.perccomplete, 'pComp')
    projrow += convxml('1', 'pOpen')
    projrow += convxml('', 'pParent')

    if hasdepend:
        projrow += convxml('1', 'pGroup')
    else:
        projrow += convxml('0', 'pGroup')

    projrow += convxml(dependlist, 'pDepend')
    projrow += convxml('A caption', 'pCaption')
    projrow += convxml(row.question.notes, 'pNotes', True)
    projrow += '</task>'
    return projrow


def get_colour(startdate, enddate, percomplete):
    if startdate and enddate:
        now = datetime.datetime.now()
        dayselapsed = max(now - startdate, datetime.timedelta(days=0)).days
        daysduration = max(enddate - startdate, datetime.timedelta(days=0)).days
        percelapsed = min((100 * dayselapsed) / daysduration, 100) if daysduration else 0

        if percomplete == 100:
            return 'gtaskyellow'
        elif now < startdate:
            return 'gtaskblue'
        elif now > enddate:
            return 'gtaskred'
        elif percelapsed > percomplete:
            return 'gtaskpurple'
        else:
            return 'gtaskgreen'
    else:
        return 'gtaskpink'  # not sure ever worth returning as no bar without dates


def gantt_colour(startdate, enddate, percomplete=0, gantt=True):
    """
    .gtaskyellow, Complete
    .gtaskblue, Not started and before startdate
    .gtaskred, Overdue and not complete
    .gtaskgreen, Started and on track
    .gtaskpurple, Started and behind schedule
    .gtaskpink Later
     gantt is a flag to allow coding of plan rows with same logic """
    colorclass = get_colour(startdate, enddate, percomplete)
    colorclass = colorclass if gantt else colorclass[1:]
    return colorclass


def score_question(questid, answer=0):
    """
    This routine is now called for all answers to questions but a couple of changes 
    a) only ever two answers to a question
    b) question may go back below threshold and be unresolved at an time
    c) thresholds are minimum number of answers and %age level eg 3 and 60% would take the answer that 2 peopel went
       for
    """
    quest = db(db.question.id == questid).select().first()
    resmethod = db(db.resolve.id == quest.resolvemethod).select().first()
    if answer == '1':
        quest.numanswer1 += 1
    elif answer == '2':
        quest.numanswer2 += 1

    numanswers = quest.numanswer1 + quest.numanswer2
    origstatus = quest.status
    if numanswers >= resmethod.responses:
        if ((100 * quest.numanswer1) / numanswers >= resmethod.consensus or
                (100 * quest.numanswer2) / numanswers >= resmethod.consensus):
            quest.status = 'Resolved'
            quest.resolvedate = datetime.datetime.utcnow()
            if quest.numanswer1 > quest.numanswer2:
                quest.correctans = 1
            else:
                quest.correctans = 2
        else:
            quest.status = 'In Progress'
            quest.correctans = 0
    quest.update_record()
    db.commit()
    returnmsg = f'Item changed to status {quest.status}' if origstatus != quest.status else f'Item still {quest.status}'
    return returnmsg


def truncquest(questiontext, maxlen=600, wrap=0, mark=True):
    if questiontext is None:
        return ''
    txt = questiontext if len(questiontext) < maxlen else questiontext[0:maxlen] + '...'
    return txt


def creategraph(itemids, numlevels=0, intralinksonly=True):
    """
    :param itemids: list
    :param numlevels: int
    :param intralinksonly: boolean
    :return: graph details

    Now think this will ignore eventmap and do no layout related stuff which means events are irrelevant for this
    function it should get links for itemids in an iterable manner and so build of network.py  mainly
    when called from event it will have a list of item ids only from the event already established

    """
    query = db.question.id.belongs(itemids)
    quests = db(query).select()

    if intralinksonly:
        # in this case no need to get other questions
        intquery = (db.questlink.targetid.belongs(itemids)) & (db.questlink.status == 'Active') & (
            db.questlink.sourceid.belongs(itemids))
        links = db(intquery).select()
    else:
        parentlist = itemids
        childlist = itemids
        links = None
        # just always have actlevels at 1 or more and see how that works
        # below just looks at parents and children - to get partners and siblings we could repeat the process
        # but that would extend to ancestors - so probably need to add as parameter to the query but conceptually
        # this could be repeated n number of times in due course

        # these may become parameters not sure
        # change back to true once working
        getsibs = False
        getpartners = False

        for x in range(numlevels):
            # ancestor proces
            if parentlist:
                parentlinks = db((db.questlink.targetid.belongs(parentlist)) &
                                 (db.questlink.status == 'Active')).select()
                if links and parentlinks:
                    links = links | parentlinks
                elif parentlinks:
                    links = parentlinks
                if parentlinks:
                    mylist = [y.sourceid for y in parentlinks]
                    query = db.question.id.belongs(mylist)
                    parentquests = db(query).select()

                    quests = quests | parentquests
                    parentlist = [y.id for y in parentquests]
                    if getsibs:
                        sibquery = db.questlink.sourceid.belongs(parentlist) & (
                                db.questlink.status == 'Active')
                        siblinks = db(sibquery).select()
                        if siblinks:
                            links = links | siblinks
                            mylist = [y.targetid for y in siblinks]
                            query = db.question.id.belongs(mylist)
                            sibquests = db(query).select()
                            quests = quests | sibquests
                        # parentquery = db.questlink.targetid.belongs(parentlist)
                        # child process starts
            if childlist:
                childlinks = db((db.questlink.sourceid.belongs(childlist)) & (
                        db.questlink.status == 'Active')).select()
                if links and childlinks:
                    links = links | childlinks
                elif childlinks:
                    links = childlinks
                if childlinks:
                    mylist = [y.targetid for y in childlinks]
                    query = db.question.id.belongs(mylist)
                    childquests = db(query).select()
                    quests = quests | childquests
                    childlist = [y.id for y in childquests]
                    if getpartners:
                        partquery = db.questlink.targetid.belongs(childlist)
                        partlinks = db(partquery).select()
                        if partlinks:
                            links = links | partlinks
                            mylist = [y.sourceid for y in partlinks]
                            query = db.question.id.belongs(mylist) & (db.questlink.status == 'Active')
                            partquests = db(query).select()
                            quests = quests | partquests
                            # childquery = db.questlink.sourceid.belongs(childlist)

    questlist = [y.id for y in quests]
    # print('links', links)
    if links:
        linklist = links
        links = [(y.sourceid, y.targetid) for y in links]
    else:
        linklist = []
    return dict(questlist=questlist, linklist=linklist, quests=quests, links=links, resultstring='OK')


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def getlinks(questlist):
    intquery = (db.questlink.targetid.belongs(questlist)) & (db.questlink.status == 'Active') & (
        db.questlink.sourceid.belongs(questlist))
    intlinks = db(intquery).select()
    return intlinks


def getstrdepend(intlinks, id):
    dependlist = [x.sourceid for x in intlinks if x.targetid == id]
    strdepend = str(dependlist)[1:max(len(str(dependlist)) - 1, 1)]
    return strdepend


def get_gantt_data(quests):
    projxml = "<project>"
    questlist = [x.question.id for x in quests]
    intlinks = getlinks(questlist)

    for i, row in enumerate(quests):
        projxml += convrow(row, getstrdepend(intlinks, row.question.id), True)

    projxml += '</project>'
    return XML(projxml)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    # Can run with -v option if you want to confirm tests were run
    _test()
