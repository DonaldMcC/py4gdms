# File for new functions to support the following
#  1 AI Generation of issues, questions and actions
#  2 AI answering of questions
#  3 AI full review of events
# For now most of these will operated at an event level and there
# should be fairly common approach along the following lines
#
# 1 Get all the items in an event
# 2 Go through one by one starting from the earliest creation date
# 3 Either generate, answer or comment on the item
# 4 Navigate to the next item (probably in the original list for now
# Will revert to extra depth later - actually now thinking we only ever do 1 layer and just re-run and
# that will automatically generate another layer.  Also maybe %age and probabilistic creation may
# be the way to go this will use the new job scheduler I anticipate and create in the background
# with logging - so think the traversal is simple and we do first
# when we come to contacting the AI for an item we probably want to see if we can combine with the interactive way
# but these are currently only suggestions and have not been structured into questions, actions and issues - probably
# fine to do that just need to fiddle about a bit with questions

from .common import db
from .settings import AI_MODE, AI_MODEL
from .ndsqueries import get_items
import json

try:
    from openai import OpenAI
    from .settings import AI_MODEL
    from .settings_private import OPENAI_API_KEY
    oai = True
except ImportError as error:
    oai = False


def add_item(item, basedict):
    """This will actually create the items required.  Let's say it can either be supplied with
    the details or it will go get them as we may want a more general add_item capability eg to call
    interactively from viewquest suggestions.  The thinking is that basedict can be very limited.
    However we might want to pass any field in question but we are generally happy to take the
    default if notthing specified and wasn't necessarily planning to include in the dict in that case"""

    # From review majority of fields not required
    # but link to auth_user probably goes now that we allow ai_content  - think that just means auth_user
    # can be null and move on probably won't break until we have some content
    # Field('resolvemethod', 'reference resolve',
    # Field('chosenai', 'reference knowledge', label='AI/Knowledge Engine'),
    print(db.question._insert(qtype='quest', eventid=item['eventid'], questiontext='new question',
                              factopinion='Fact', answertext='', answer1='', answer2='', aianswer=''))
    questiondict = dict(myfield='somevalue')
    db.question[None] = questiondict


def review_item(item, ai_model):
    """This should take an item and identify the current number of links and would then use the parameters
    for whether or not to create new linked items to decide to create new items.  If a new item is
    required we will call add_item """
    print(item)
    return


def answer_item(item, ai_model):
    # should support answering an item and can be called from viewquest for interactive use
    # event traversal use should also be possible and we would then store answer separately
    # and rescore the question
    setup = 'A'
    scenario = 'answer'
    print(item.questiontext)
    answers = (item.answer1, item.answer2, item.answer3, item.answer4)
    if AI_MODE == 'Test':
        resulttext = ('json {"answer": 1, "reason": "poverty}',item.questiontext)
    else:
        resulttext = openai_query(item.questiontext, scenario, setup, AI_MODEL, AI_MODE, item.id, answers)
    result =resulttext[0]
    openbracket = result.find('{')
    closebracket = result.rfind('}' )
    resultjson = json.loads(result[openbracket:closebracket+1])

    print(resultjson)
    return resultjson['answer']


def generate_items(qtext, scenario, setup, qid, format='text'):
    # should support generating more questions from an item and can be called from viewquest for interactive use
    # event traversal
    # TODO consider if always switch to JSON and get possible answers or stick with text to review and then put
    # into question  but this means two different sets of prompts - think we go two routes
    setup = 'A'
    print(qtext)
    answers=None
    if AI_MODE == 'Test':
        resulttext = f'generate items {qtext}'
    else:
        resulttext = openai_query(qtext, scenario, setup, AI_MODEL, AI_MODE, qid, answers)

    return resulttext


def generate_answers(qtext, scenario, setup, qid, format='text'):
    # should support generating more questions from an item and can be called from viewquest for interactive use
    # event traversal
    # TODO consider if always switch to JSON and get possible answers or stick with text to review and then put
    # into question  but this means two different sets of prompts - think we go two routes
    setup = 'A'
    print(qtext)
    answers=None
    if AI_MODE == 'Test':
        resulttext = f'generate items {qtext}'
    else:
        resulttext = openai_query(qtext, scenario, setup, AI_MODEL, AI_MODE, qid, answers)

    return resulttext


def get_messages(chosenai, scenario, setup, qtext, answers=None):
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
    query = ((db.prompt.chosenai == chosenai) & (db.prompt.scenario == scenario)
             & (db.prompt.setup == setup) & (db.prompt.status == 'Active'))
    sortby = db.prompt.sequence
    prompts = db(query).select(orderby=[sortby])
    print(prompts)
    print (scenario)
    message = []
    userprompt = {"role": "user", "content": qtext}
    answer_intro = {"role": "user",  "content": "And the possible answers are:"}
    if answers:
        answerlist = '\n'.join(answers)
        answerprompt = {"role": "user",  "content": answerlist}
    written_userprompt = False
    for row in prompts:
        # This writes prompts up to sequence 50 before the item and ones above 50 after it
        dictrow = {"role": row.role, "content": row.content}
        if not written_userprompt and row.sequence > 50:
            message.append(userprompt)
            if scenario[:6] == 'answer':
                message.append(answer_intro)
                message.append(answerprompt)
            written_userprompt = True

        message.append(dictrow)

    if not written_userprompt:
        message.append(userprompt)
        if scenario[:6] == 'answer':
            message.append(answer_intro)
            message.append(answerprompt)
    print(message)
    return message


def openai_query(qtext, scenario, setup='A', model=AI_MODEL, aimode='Prod', qid=None, answers=None):
    #So for now this is taking some text and looking up a scenario and a setup
    #The thinking was that setups could support basically different sets of prompts for
    #the same task to allow comparison and scenarios would cater to what we want the ai
    #to do.  eg comment on the text as an expert, answer the question, generate follow ons etc
    #I am not overly clear how best to handle the chat history - probably it will need to be
    #provided somehow at some point as in multi-user mode with one ID any other approach seems
    #challenging
    #we have also called this openai_query for now but clearly will be similarities with other
    #providers LLMs and we may want to setup a class with inheritance later for some of this -
    #but sticking with openai to get something working for now - and also ignoring history at
    #this point to keep simple
    if aimode == 'Test':
        db.ai_review.insert(parentid=qid, chosenai='GPT-4', ai_version=AI_MODEL,
                        review='test mode', prompts=qtext)
        return  f"Testing Mode {qtext}", "test"
    if len(qtext) < 10:
        db.ai_review.insert(parentid=qid, chosenai='GPT-4', ai_version=AI_MODEL,
                            review='too short', prompts=qtext)
        return  f"Text too short {qtext}", "short"
    client = OpenAI(api_key=OPENAI_API_KEY)
    chosenai = db(db.knowledge.title == 'OpenAI GPT-3').select().first()
    messages = get_messages(chosenai.id, scenario, setup, qtext, answers)
    #test option to get json response
    if answers:
        completion = client.chat.completions.create(model=model,
        messages=messages, max_tokens=300, temperature=0.1, response_format = {"type": "json_object"})
    else:
        completion = client.chat.completions.create(model=model,
            messages=messages, max_tokens=300, temperature=0.1)
    # will stick with logging except on initial question creation as then don't have qid and seems to be duplicating
    # the same information really
    if qid:
        db.ai_review.insert(parentid=qid, chosenai='GPT-4', ai_version=AI_MODEL,
                            review=completion.choices[0].message.content, prompts=messages)

    return completion.choices[0].message.content, messages


def get_event_items(eid, ai_action='answer', ai_mode='unanswered', ai_model = AI_MODEL):
    # This should provide basic navigation around an event to either review items. Answer as an ai
    # or generate more items
    eventrow = db(db.event.id == eid).select().first()
    items = get_items(qtype='all', status='all', event=eid, eventstatus=eventrow.status)
    visited = {}
    if ai_action == 'answer':
        func = answer_item
    else:
        func = review_item
    for item in items:
        result = func(item, ai_model)
        # for each answer we potentially then update and call score_question again