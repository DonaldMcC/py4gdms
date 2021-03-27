from .common import db, auth


def check_liked(items):
    query = db.item_like.created_by == auth.user_id
    query &= db.item_like.item_id.belongs(items.as_dict().keys())
    liked_ids = [row.item_id for row in db(query).select()]
    for item in items:
        item["liked"] = item.id in liked_ids
    return


def get_disabled(ans, useranswer):
    return 'disabled title=You_already_answered ' if ans == useranswer else ' title=Click_to_Answer '


def get_class(qtype='quest', answer=1, framework='Bulma'):
    # Function to return button classes - only supporting Bulma.css for now
    # is-success and is-danger for agree disagree on issues and approve disapprove on actions
    if qtype != 'quest':  # issue or action
        btnclass = 'is-success' if answer == 1 else 'is-danger'
    else:
        btnclass = ''
    btnclass += 'button is-small is-rounded '
    return btnclass


def get_items(qtype='action', status=None, x=0, y=10, event=None, eventstatus='Open', project=None, execstatus=None):
    query = make_query(qtype, status, event, eventstatus, project, execstatus)
    leftjoin = make_leftjoin(status)
    if eventstatus == 'Archived':
        sortby = ~db.eventmap.id
    else:
        sortby = db.question.priority|~db.question.id if status == 'Resolved' else ~db.question.id
    return db(query).select(left=leftjoin, orderby=[sortby], limitby=(x, y))


def make_query(qtype='quest', status=None, event=None, eventstatus='Open', project=None, execstatus=None):
    if eventstatus == 'Archived':
        if qtype == 'quest':
            query = (db.eventmap.qtype == 'quest')
        elif qtype == 'action':
            # query = (db.question.qtype == 'action') & (db.question.execstatus != 'Completed')
            query = (db.eventmap.qtype == 'action')
        else:
            query = (db.eventmap.qtype == 'issue')
        if status:
            query &= (db.eventmap.status == status)
        if event:
            query &= (db.eventmap.eventid == event)
    else:
        if qtype == 'quest':
            query = (db.question.qtype == 'quest')
        elif qtype == 'action':
            # query = (db.question.qtype == 'action') & (db.question.execstatus != 'Completed')
            query = (db.question.qtype == 'action')
        else:
            query = (db.question.qtype == 'issue')
        if status:
            query &= (db.question.status == status)
        if event:
            query &= (db.question.eventid == event)
        if project:
            events = db(db.evt.projid == project).select(db.evt.id)
            eventlist = [row.id for row in events] if events else []
            query &= (db.question.eventid.belongs(eventlist))
        if execstatus:
            if execstatus == 'Incomplete':
                query &= (db.question.execstatus != 'Completed')
            else:
                query &= (db.question.execstatus == 'Completed')
    return query


def make_leftjoin(status):
    if status != 'Archived':
        leftjoin = db.userquestion.on((db.question.id == db.userquestion.questionid)
                                        & (db.userquestion.auth_userid == auth.user_id))
    else:
        leftjoin = db.userquestion.on((db.eventmap.questid == db.userquestion.questionid)
                                        & (db.userquestion.auth_userid == auth.user_id))
    return leftjoin