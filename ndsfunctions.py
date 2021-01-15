# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/gdms
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

import builtins
import datetime
import calendar
from yatl.helpers import XML
from py4web import action, request, abort, redirect, URL
from .common import db, session, T, cache, auth

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
    colorclass = gantt_colour(row.startdate, row.enddate, row.perccomplete)
    if row.startdate == row.enddate:
        milestone = 1
    else:
        milestone = 0
    plink = URL('submit', 'question_plan')
    projrow = '<task>'
    projrow += convxml(row.id, 'pID')
    projrow += convxml(row.questiontext, 'pName', True, False)
    projrow += convxml(row.startdate, 'pStart')
    projrow += convxml(row.enddate, 'pEnd')
    projrow += convxml(colorclass, 'pClass')
    projrow += convxml(plink, 'pLink')
    projrow += convxml(milestone, 'pMile')
    projrow += convxml(row.responsible, 'pRes', True)
    projrow += convxml(row.perccomplete, 'pComp')
    projrow += convxml('1', 'pOpen')
    projrow += convxml('', 'pParent')

    if hasdepend:
        projrow += convxml('1', 'pGroup')
    else:
        projrow += convxml('0', 'pGroup')

    projrow += convxml(dependlist, 'pDepend')
    projrow += convxml('A caption', 'pCaption')
    projrow += convxml(row.notes, 'pNotes', True)
    projrow += '</task>'
    return projrow


def gantt_colour(startdate, enddate, percomplete=0, gantt=True):
    """
    .gtaskyellow, Complete
    .gtaskblue, Not started and before startdate
    .gtaskred, Overdue and not complete
    .gtaskgreen, Started and on track
    .gtaskpurple, Started and behind schedule
    .gtaskpink Later  
    
    ganntt is now a flag to allow coding of plan rows with same logic """

    if startdate and enddate:
        now = datetime.datetime.now()
        dayselapsed = max(now - startdate, datetime.timedelta(days=0)).days
        daysduration = max(enddate - startdate, datetime.timedelta(days=0)).days

        if daysduration:
            percelapsed = min((100 * dayselapsed) / daysduration, 100)
        else:
            percelapsed = 0

        if percomplete == 100:
            colorclass = 'gtaskyellow'
        elif now < startdate:
            colorclass = 'gtaskblue'
        elif now > enddate:
            colorclass = 'gtaskred'
        elif percelapsed > percomplete:
            colorclass = 'gtaskpurple'
        else:
            colorclass = 'gtaskgreen'
    else:
        colorclass = 'gtaskpink'  # not sure ever worth returning as no bar without dates

    if gantt is False:
        colorclass = colorclass[1:]

    return colorclass


def resulthtml(questiontext, answertext, id=0, output='html'):
    """This formats the email for sending from the schedule on email resolution
    """

    params = db(db.website_parameters.id > 0).select().first()
    stripheader = params.website_url[7:]  # to avoid duplicated header
    if output == 'html':
        result = '<p>' + questiontext + r'</p>'
        result += r'<p>Users have resolved the correct answer is:</p>'
        result += '<p>' + answertext + r'</p>'
        result += URL('viewquest', 'index', args=[id], scheme='http', host=stripheader)
        result = '<html>' + result + r'</html>'
    else:
        result = questiontext + '/n Users have resolved the correct answer is: /n' + answertext
    return result


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
    print('Ihave'+str(questid))
    if answer == '1':
        quest.numanswer1 += 1
    elif answer == '2':
        quest.numanswer2 += 1

    numanswers = quest.numanswer1 + quest.numanswer2
    print(numanswers)
    if numanswers >= resmethod.responses:
        if ((100 * quest.numanswer1) / numanswers >= resmethod.consensus or
            (100 * quest.numanswer2) / numanswers >= resmethod.consensus):
            print('resolved')
            quest.status = 'Resolved'
            quest.resolvedate = datetime.datetime.utcnow()
            if quest.numanswer1 > quest.numanswer2:
                quest.correctans = 1
            else:
                quest.correctans = 2
        else:
            #Just may need an unresolvedate - lets just use resolveddate as unresolvedate for now
            quest.status = 'In Progress'
            quest.correctans = 0
            quest.resolvedate = datetime.datetime.utcnow()

    quest.update_record()
    db.commit()

    return quest.status


def most_common(lst):
    """ initial discussion on ways of doing this at:
    http://stackoverflow.com/questions/1518522/python-most-common-element-in-a-list
    >>> most_common(['a','b','c','b'])
    ('b', 2)
    
    """
    return max(((item, lst.count(item)) for item in set(lst)), key=lambda a: a[1])


def check_change(lst, numrequired, unchangedvalue):
    """ 
    >>> check_change(['a','b','c','b'],2,'a')
    'b'
    
    >>> check_change(['a','b','c','b'],3,'a')
    'a'
    
    """
    result, qty = most_common(lst)
    if qty < numrequired:
        result = unchangedvalue
    return (result)


def getindex(qtype, status):
    """This returns the index for questcounts which is a list of integers based on the 6 possible status and 3 question
       types so it is an index based on two factors want 0, 1 or 2 for issue, question and action and then 0 through 5
       for draft, in progress, etc - current flaw is that resolved actions go to agreed but we also have an agreed count
       - however that should not use this
    :param qtype: string
    :param status: string

    >>> getindex('quest','In Progress')
    7
    """

    if status == 'Agreed':
        status = 'Resolved'

    qlist = ['issue', 'quest', 'action']
    slist = ['Draft', 'In Progress', 'Resolved', 'Agree', 'Disagree', 'Rejected']

    i = qlist.index(qtype) if qtype in qlist else None
    j = slist.index(status) if status in slist else None

    return (i * 6) + j


def userdisplay(userid):
    """This should take a user id and return the corresponding
       value to display depending on the users privacy setting"""
    usertext = userid
    userpref = db(db.auth_user.id == userid).select().first()
    if userpref.privacypref == 'Standard':
        usertext = userpref.first_name + ' ' + userpref.last_name
    else:
        usertext = userid
    return usertext


def scopetext(scopeid, continent, country, subdivision):
    """This returns the name of the relevant question scope """

    scope = db(db.scope.id == scopeid).select(db.scope.description).first().description
    if scope == 'Global':
        activetext = 'Global'
    elif scope == 'Continental':
        activetext = db(db.continent.id == continent).select(
            db.continent.continent_name).first().continent_name
    elif scope == 'National':
        activetext = db(db.country.id == country).select(
            db.country.country_name).first().country_name
    else:
        activetext = db(db.subdivision.id == subdivision).select(
            db.subdivision.subdiv_name).first().subdiv_name

    return activetext


def truncquest(questiontext, maxlen=600, wrap=0, mark=True):
    if questiontext is None:
        return ''
    if mark:
        if len(questiontext) < maxlen:
            #txt = MARKMIN(questiontext)
            txt = questiontext
        else:
            #txt = MARKMIN(questiontext[0:maxlen] + '...')
            txt = questiontext[0:maxlen] + '...'
    else:
        if len(questiontext) < maxlen:
            txt = questiontext
        else:
            txt = questiontext[0:maxlen] + '...'
    return txt


def disp_author(userid):
    if userid is None:
        return ''
    else:
        user = db.auth_user(userid)
        return '%(first_name)s %(last_name)s' % userid


def update_numanswers(userid):
    # This just increments numb users
    isauth = session.auth or None
    if isauth and userid == auth.user.id:  # This should always be the case
        numquests = auth.user.numquestions + 1
        db(db.auth_user.id == auth.user.id).update(numquestions=numquests)
        auth.user.update(numquestions=numquests)
        db.commit()
    return True


def score_challenge(questid, successful, level):
    """
    This will reward those that raised a challenge if the answer has changed
    it may also spawn an issue of scoring users who previously thought they
    got it wrong but now got it right - thinking is we wouldn't remove
    points from those that were previously considered right
    :param successful:
    :param questid:
    :param level:
    """

    unpchallenges = db((db.questchallenge.questionid == questid) &
                               (db.questchallenge.status == 'In Progress')).select()

    # should get the score based on the level of the question
    # and then figure out whether
    # get the score update for a question at this level

    scoretable = db(db.scoring.scoring_level == level).select().first()

    if scoretable is not None:
        if successful is True:
            challengescore = scoretable.rightchallenge
        else:
            challengescore = scoretable.wrongchallenge
    else:
        if successful is True:
            challengescore = 30
        else:
            challengescore = -10

    for row in unpchallenges:
        user = db(db.auth_user.id == row.auth_userid).select().first()
        scoretable = db(db.scoring.scoring_level == user.userlevel).select().first()
        nextlevel = scoretable.nextlevel

        updscore = challengescore + user.score

        if updscore > nextlevel:
            userlevel = user.userlevel + 1
        else:
            userlevel = user.userlevel

        db(db.auth_user.id == row.auth_userid).update(score=updscore, userlevel=userlevel)

    db.commit()
    return


def getitem(qtype):
    if qtype == 'quest':
        item = 'question'
    elif qtype == 'action':
        item = 'action'
    else:
        item = 'issue'
    return item


def getrundates(period='Day', startdate=datetime.datetime.today()):
    """
    :param startdate:
    :param period: Valid values are Day, Week or Month
    :return startdate, endate
    So this is a bit crude at moment but not sure I want calendar weeks and months either
    Leave for now
    """

    numdays = (period == 'Day' and 1) or (period == 'Week' and 7) or 30
    enddate = startdate + datetime.timedelta(days=numdays)
    return startdate, enddate


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

        # intlinks = db(intquery).select(cache=(cache.ram, 120), cacheable=True)
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
    #print('links', links)
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


def generate_thumbnail(image, nx=120, ny=120, static=False):
    """
    Makes thumbnail version of given image with given maximum width & height
    in uploads folder with filename based on original image name

    If static=True thumbnail will be placed in static/thumbnails
    so it can be used without the need of a download controller

    requires PIL
    """
    if not image:
        return
    try:
        import os
        from PIL import Image

        img = Image.open(os.path.join(request.folder, 'uploads', image))
        img.thumbnail((nx, ny), Image.ANTIALIAS)
        root, ext = os.path.splitext(image)
        thumb = '%s_thumb_%s_%s%s' % (root, nx, ny, ext)
        img.save(os.path.join(request.folder, 'uploads', thumb))
        if static:
            file_dir = os.path.join(request.folder, 'static', 'thumbnails')
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            img.save(os.path.join(file_dir, thumb))
            os.path.join(file_dir, thumb)
        return thumb
    except:
        return


def getstrdepend(intlinks, id):
    dependlist = [x.sourceid for x in intlinks if x.targetid == id]
    strdepend = str(dependlist)[1:max(len(str(dependlist)) - 1, 1)]
    return strdepend


def get_gantt_data(quests):
    projxml = "<project>"
    questlist = [x.id for x in quests]
    intlinks = getlinks(questlist)

    for i, row in enumerate(quests):
        projxml += convrow(row, getstrdepend(intlinks, row.id), True)

    projxml += '</project>'
    # print(projxml)
    return XML(projxml)


def get_col_headers(startdate):
    # Need to work out number of columns for recurrent tasks idea is that they are ordered but could be
    # mone daily, weekly, bi-weekly, monthly etc - think we will generate up to 14 buckets as a dictionary keyed
    # on the recurrence pattern - still got two problems - format to return and the start date issue - for format
    # let's calculate that actual date and also the suggested output format eg M T W for daily and poss short date
    # for all the rest - not convinced start date should be computed - seems it needs to be an input and while we
    # may already have on the form this may drop tasks that started before and are still recurring  - so we
    # need to change the query to pick recurring tasks that haven't ended at the start date and this can be
    # changed to just work from the start date and populate all possible headers

    recurtypes = [('Daily', 1), ('Weekly', 7), ('Bi-weekly', 14), ('Monthly', 30), ('Quarterly', 91)]
    colheads = {}
    for x in recurtypes:
        colheads[x[0]] = []
        for y in range(14):
            headerdate = startdate + datetime.timedelta(days=(y * x[1]))
            formatdate = getformat(headerdate, x[0])
            colheads[x[0]].append((headerdate, formatdate))
    return colheads


def getformat(headerdate, recurrence='daily'):
    return calendar.day_name[headerdate.weekday()][:2] + ' ' + str(headerdate.day)

def get_recurr_class(taskdate,complete=False):
    today = datetime.date.today()
    if complete:
        return "taskgreen"
    elif taskdate >= today:
        return "action-medium"
    else:
        return "taskred"

def get_recurr_cell(id, startdatetime, enddatetime, colheaders, j, complete):
    startdate = datetime.date(startdatetime.year, startdatetime.month, startdatetime.day)
    enddate = datetime.date(enddatetime.year, enddatetime.month, enddatetime.day)
    if (startdate <= colheaders[j][0] and enddate >= colheaders[j][0]):
        taskdt = colheaders[j][0] - startdate
        if complete and len(complete) > taskdt.days  :
            print(taskdt.days)
            print (complete)
            print('completed')
        if complete and len(complete) > taskdt.days and complete[taskdt.days]:
            taskdone = True
            checktask = 'checked'
            print('checked')
        else:
            print('else')
            taskdone = False
            checktask = ''
        style = get_recurr_class(colheaders[j][0], taskdone)
        cell_html = '<td style="text-align:center" class="' + style +'"> <input type = "checkbox" ' + checktask + '>  </td>'
    else:
        cell_html = '<td> </td>'
    return XML(cell_html)


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    # Can run with -v option if you want to confirm tests were run
    _test()
