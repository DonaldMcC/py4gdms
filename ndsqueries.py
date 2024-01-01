from .common import db, auth
import pprint

try:
    from openai import OpenAI
    from .settings_private import OPENAI_API_KEY
    oai = True
except ImportError as error:
    oai = False


def get_disabled(ans, useranswer):
    return 'disabled title=You_already_answered ' if ans == useranswer else ' title=Click_to_Answer '


def get_classBulma(qtype='quest', answer=1):
    # Function to return button classes - only supporting Bulma.css for now
    # is-success and is-danger for agree disagree on issues and approve disapprove on actions

    btnclass = ''
    if qtype != 'quest':  # issue or action
        btnclass = 'is-success ' if answer == 1 else 'is-danger '
    btnclass += 'button is-small is-rounded'
    return btnclass


def get_classBootstrap(qtype='quest', answer=1):
    # Function to return button classes - only supporting Bulma.css for now
    # is-success and is-danger for agree disagree on issues and approve disapprove on actions
    btnclass = ''
    if qtype != 'quest':  # issue or action
        btnclass = 'btn-success ' if answer == 1 else 'btn-danger '
    btnclass += 'btn btn-small'
    return btnclass


def get_class(qtype='quest', answer=1, framework='Bootstrap'):
    # Function to return button classes - only supporting Bulma.css for now
    # is-success and is-danger for agree disagree on issues and approve disapprove on actions
    if framework == 'Bulma':
        return get_classBulma(qtype, answer)
    else:
        return get_classBootstrap(qtype, answer)


def check_liked(item, eventstatus, table='question'):
    if eventstatus == 'Archived':
        itemid = item.eventmap.questid
    else:
        itemid = item.question.id
    query = (db.itemlike.createdby == auth.user_id) & (db.itemlike.parenttable == table)
    query &= (db.itemlike.parentid == itemid)
    liked = db(query).select()
    return True if liked else False


def get_items(qtype='action', status=None, x=0, y=8, event=None, eventstatus='Open',
              project=None, execstatus=None, qid=None):
    query = make_query(qtype, status, event, eventstatus, project, execstatus, qid)
    leftjoin = make_leftjoin(eventstatus)
    if eventstatus == 'Archived':
        sortby = ~db.eventmap.id
    else:
        sortby = db.question.priority | ~db.question.id if status == 'Resolved' else ~db.question.id
    items = db(query).select(left=leftjoin, orderby=[sortby], limitby=(x, y))
    for item in items:
        item["liked"] = check_liked(item, eventstatus)
    return items


def make_query(qtype='quest', status=None, event=None, eventstatus='Open', project=None, execstatus=None, qid=None):
    if eventstatus == 'Archived':
        if qtype == 'quest':
            query = (db.eventmap.qtype == 'quest')
        elif qtype == 'action':
            query = (db.eventmap.qtype == 'action')
        else:
            query = (db.eventmap.qtype == 'issue')
        if status:
            query &= (db.eventmap.status == status)
        if event:
            query &= (db.eventmap.eventid == event)
        if qid:
            query &= (db.eventmap.questid == qid)
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
            events = db(db.event.projid == project).select(db.event.id)
            eventlist = [row.id for row in events] if events else []
            query &= (db.question.eventid.belongs(eventlist))
        if execstatus:
            if execstatus == 'Incomplete':
                query &= (db.question.execstatus != 'Completed')
            else:
                query &= (db.question.execstatus == 'Completed')
        if qid:
            query &= (db.question.id == qid) 
    return query


def make_leftjoin(eventstatus):
    if eventstatus != 'Archived':
        leftjoin = db.userquestion.on((db.question.id == db.userquestion.questionid)
                                      & (db.userquestion.auth_userid == auth.user_id))
    else:
        leftjoin = db.userquestion.on((db.eventmap.questid == db.userquestion.questionid)
                                      & (db.userquestion.auth_userid == auth.user_id))
    return leftjoin


def get_messages(chosenai, scenario, setup, qtext):
    """
    :param chosenai:
    :param scenario:
    :param setup:
    :param qtext:
    :return:

    This should populate the prompts for openai only currently but most likely other LLMs can be added at some point
    idea is that these are served first the system prompts and then the user prompts for chosenai, scenario and setup
    We then serialise them into list of items to return hopefully
            {"role": "system", "content": "You are providing advice to make the world better "},
    """
    # need to change this query to use the title of the chosen ai or pass the integer
    query = ((db.prompt.chosenai == chosenai) & (db.prompt.scenario == scenario) & (db.prompt.setup == setup)
             & (db.prompt.status == 'Active'))
    sortby = db.prompt.prompttype, db.prompt.sequence
    prompts = db(query).select(orderby=[sortby])

    message = []
    userprompt = {"role": "user", "content": qtext}
    written_userprompt = False
    for row in prompts:
        dictrow = {"role": row.prompttype, "content": row.prompt_text}
        if not written_userprompt and row.sequence > 50:
            message.append(userprompt)
            written_userprompt = True
        message.append(dictrow)

    if not written_userprompt:
        message.append(userprompt)

    return message


def openai_query(qtext, scenario, setup='A'):
    #qtext = request.json['questiontext']
    #scenario = request.json['scenario']
    #setup = 'A'
    client = OpenAI(api_key=OPENAI_API_KEY)

    chosenai = db(db.knowledge.title == 'OpenAI GPT-3').select().first()
    messages = get_messages(chosenai.id, scenario, setup, qtext)
    #for item in messages:
    #    print(type(item), item)
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=messages, max_tokens=300, temperature=0.1)

    return completion.choices[0].message.content
