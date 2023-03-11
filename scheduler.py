# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Site (Pythonanywhere)
#   http://netdecisionmaking.com/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
# This should send email summaries to users on an immediate, daily, weekly or monthly schedule if requested in
# their user profile
# We will have a last run date against the user which gets updated when the email is sent unless a resend flag
# included
# If immediate users get emails on question submission, resolution etc - otherwise should also run daily
# think we iterate through all users and just look at user and lastrun date versus todays date to get the list
# of users due a notification - then we work out what we want to send them which should be a subfunction
# which could still have the run type and we should be able to run the notification immediately with user
# and runtype

import datetime
from ndsfunctions import score_question, resulthtml, truncquest, getrundates
from .common import settings, scheduler, db, Field


def notify_email(user, notifytype):

    return success or failure


def get_users_notification(notifytype):
    # notifytype can be immediate, daily, weekly or monthly
    # so collect all users check last run parameter and call
    # notify_email for each user with matching notifytype
    # think intial call can always be immediate but that can also be called
    # with daily/weekly/monthly
    # think we can prequery this if no items since last run but if there are
    # then lets run it

    rows = db(db.auth.id == id).select(db.notifytype==notifytype)

    for user in rows:
        result = notify_email(user, notifytype)


    return ''


def activity(id=0, resend=False, period='Week', format='html', source='default'):
    # This will be triggered from runactivity function below which figures out if 
    # this needs to be run and on success rolls the run date forward for the next
    # period this just formats the message and formats for sending via email

    if id:
        rows = db(db.email_runs.id == id).select()
        # if record status not equal to planned then log not sending to console and lets go with
        # only resending by id number
    else:
        rows = db((db.email_runs.runperiod == period) & (db.email_runs.status == 'Planned')).select()

    if rows is None:
        return 'No matching parameter record found'

    parameters = rows.first()
    params = db(db.website_parameters.id > 0).select().first()

    if params:
        stripheader = params.website_url[7:]
    else:
        stripheader = 'website_url_not_setup'

    startdate = parameters.datefrom
    enddate = parameters.dateto

    crtquery = (db.question.createdate >= startdate) & (db.question.createdate <= enddate)
    resquery = (db.question.resolvedate >= startdate) & (db.question.resolvedate <= enddate)
    challquery = (db.question.challengedate >= startdate) & (db.question.challengedate <= enddate)

    orderstr = db.question.createdate
    resolvestr = db.question.resolvedate
    challstr = db.question.challengedate

    allsubmitted = db(crtquery).select(orderby=orderstr)
    resolved = db(resquery).select(orderby=resolvestr)
    challenged = db(challquery).select(orderby=challstr)

    sender = mail.settings.sender
    subject = 'NDS Activity Report'
    
    # get users for type of run
    if parameters.runperiod == 'Day':
        userquery = (db.auth_user.emaildaily == True)
        periodtext = 'Daily'
    elif parameters.runperiod == 'Week':
        userquery = (db.auth_user.emailweekly == True)
        periodtext = 'Weekly'
    elif parameters.runperiod == 'Month':
        periodtext = 'Monthly'
        userquery = (db.auth_user.emailmonthly == True)
    else:
        return 'Invalid run period parameter - must be Day, Week or Month'

    users = db(userquery).select()
    message = ''
    for user in users:
        to = user.email
        # will change above to create allsubmitteds and then do a filter
        message = '<html><body><h1> ' + periodtext + ' Activity Report</h1>'

        # should be able to make personal as well
        # can do the row exclusions later

        # section below is basically taken from activtiy.i file in the view

        message += "<h1>Items Resolved</h1>"
        if resolved:
            message += """<table style="border: 1px solid DarkGreen;"><thead><tr>
                        <th width="5%">Type</th>
                        <th width="55%">Item Text</th>
                        <th width="15%">Answer</th>
                        <th width="8%"># Agree</th>
                        <th width="8%"># Disagree</th>
                        <th width="9%">Resolved</th>
                    </tr>
                </thead>
                    <tbody>"""
            for row in resolved:
                itemurl = URL('viewquest', 'index', args=[row.id], scheme='http', host=stripheader)
                itemtext = truncquest(row.questiontext)
                message += """<tr>
                <th><a href=%s>%s</a></th>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>

                </tr>""" % (itemurl, row.qtype, itemtext, row.correctanstext, row.othercounts[3],
                            row.othercounts[3], row.resolvedate)
            message += " </tbody></table>"
        else:
            message += "<h3>No items resolved in the period.</h3>"

        message += "<h1>Items Submitted</h1>"
        if submitted:
            message += """<table style="border: 1px solid black;"><thead><tr>
                        <th width="5%">Type</th>
                        <th width="60%">Item Text</th>
                        <th width="13%">Scope</th>
                        <th width="12%">Category</th>
                        <th width="10%">Status</th>
                    </tr>
                </thead>
                    <tbody>"""
            for row in submitted:
                itemurl = URL('viewquest', 'index', args=[row.id], scheme='http', host=stripheader)
                itemtext = row.questiontext
                message += """<tr>
                <th><a href=%s>%s</a></th>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>""" % (itemurl, row.qtype, itemtext, row.scopetext, row.category, row.status)
            message += " </tbody></table>"
        else:
            message += "<h3>No items submitted in the period.</h3>"

        message += "<h1>Items Challenged</h1>"
        if challenged:
            message += """<table style="border: 1px solid DarkOrange;"><thead><tr>
                        <th width="5%">Level</th>
                        <th width="55%">Question</th>
                        <th width="15%">Answer</th>
                        <th width="8%"># Agree</th>
                        <th width="8%"># Disagree</th>
                        <th width="9%">Challenged</th>
                    </tr>
                </thead>
                    <tbody>"""
            for row in challenged:
                itemurl = URL('viewquest', 'index', args=[row.id], scheme='http', host=stripheader)
                itemtext = row.questiontext
                message += """<tr>

                <th><a href=%s>%s</a></th>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                </tr>""" % (itemurl, row.qtype, itemtext, row.correctanstext, row.othercounts[3],
                            row.othercounts[3], row.resolvedate)
            message += " </tbody></table>"
        else:
            message += "<h3>No items challenged in the period.</h3>"
            
        message += '<p>This report covers the period from %s to %s.</p>' % (str(startdate), str(enddate))

        # TODO this should move to module as may be repeated
        params = db(db.website_parameters.id > 0).select().first()
        if params:
            stripheader = params.website_url[7:]
        else:
            stripheader = 'website_url_not_setup'
        if login == 'socialauth':
            controller = 'user'
            itemurl = URL('plugin_social_auth', controller, args=['profile'], scheme='http', host=stripheader)
        else:
            controller = 'user'
            itemurl = URL('default', controller, args=['profile'], scheme='http', host=stripheader)

        footer = '<br><br><p>Login then manage your email preferences at ' + itemurl + '</p>'

        message += footer
        message += '</body></html>'

        if resolved or challenged or submitted:
            send_email(to, mail.settings.sender, subject, message)
        else:
            if debug:
                print(subject, message)
                send_email(to, mail.settings.sender, subject, message)
    print(message)

    return 'run successful'

    
# this schedules email when admin/datasteup has been completed
# gets called from admin.py datasetup
def schedule_email_runs(duedate=datetime.datetime.today()):
    scheduler.queue_task(runactivity, start_time=duedate, period=600, repeats=0)
    print('Email task scheduled for ')
    print(duedate)
    return True


def runactivity():
    # This would action all emails after the end date if run then
    # will refresh the dates for now but that may possibly also need to archive the record
    # will then call activity if necessary to actually run - otherwise do nothing
    result = 'starting run activity'

    currtime = datetime.datetime.today()
    to_run = db((db.email_runs.dateto <= currtime) & (db.email_runs.status == 'Planned')).select()
    if to_run:
        for row in to_run:
            runresult = activity(period=row.runperiod)
            print(runresult)
            newstartdate, newenddate = getrundates(period=row.runperiod, startdate=row.dateto)
            row.update_record(datefrom=newstartdate, dateto=newenddate)
            db.commit()
    else:
        print('No scheduled emails this period')
    return result


def send_email(to, sender, subject, message):
    result = mail.send(to=to, sender=sender, subject=subject, message=message)
    return result


def email_resolved(questid):
    scheduler.queue_task(send_email_resolved, pvars=dict(questid=questid), period=600)
    return True


# this is called from ndsfunctions if resolved
def send_email_resolved(questid):
    # For now this will find the resolved question and
    # check if owner wants to be notified if so email will be sent
    # else do nothing - may extend to sending to respondents in due course

    quest = db(db.question.id == questid).select().first()
    owner = db(db.auth_user.id == quest.auth_userid).select().first()

    if owner.emailresolved:
        subject = 'Item resolved: ' + str(truncquest(quest.questiontext, 100, wrap=0, mark=False))
        message = resulthtml(quest.questiontext, quest.correctanstext, questid)
        send_email(owner.email, mail.settings.sender, subject, message)

    return True
