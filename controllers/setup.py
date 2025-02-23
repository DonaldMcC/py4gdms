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

# This controller provides the initial data setup routines

import datetime
from ..common import db, authenticated, auth, session
from py4web import action, request, redirect, URL, Flash
from pydal.tools.tags import Tags
groups = Tags(db.auth_user, tag_table=db.auth_user_tag_groups)
flash = Flash()


@action('admin', method=['POST', 'GET'])
@action('admin/<path:path>', method=['POST', 'GET'])
@action.uses('admin.html', session, db, flash, auth.user)
def admin():
    if not 'manager' in groups.get(auth.get_user()['id']):
        redirect(URL('not_authorized'))
    return locals()


@authenticated()
def datasetup():
    if db(db.website_parameters.id > 0).isempty():
        db.website_parameters.insert(website_name='NDS Test System', website_title='Net Decision Making',
                                     website_url='http://127.0.0.1:8000',
                                     longdesc='This is a test version of networked decision making',
                                     shortdesc='Test net decision making',
                                     level1desc='Contnent', level2desc='Countrie', level3desc='Area',
                                     seo_meta_author='Russ King',
                                     seo_meta_description='Platform for group decision making without meetings')

    if db(db.locn.location_name == "Unspecified").isempty():
        locid = db.locn.insert(location_name="Unspecified", locked=True, auth_userid=auth.user_id,
                               description='The unspecified location is used as a default for all events that are not'
                                           ' allocated a specific location')

    if db(db.project.proj_name == "Unspecified").isempty():
        projid = db.project.insert(proj_name="Unspecified", proj_shared=True, locked=True, proj_owner=auth.user_id,
                                   description='The unspecified project is used as a default for all events not '
                                               ' allocated a specific project')

    if db(db.event.event_name == "Unspecified").isempty():
        locid = db(db.locn.location_name == 'Unspecified').select(db.locn.id).first().id
        projid = db(db.locn.location_name == 'Unspecified').select(db.locn.id).first().id
        evid = db.event.insert(event_name="Unspecified", locationid=locid, projid=projid, locked=True,
                               startdatetime=datetime.datetime.utcnow() - datetime.timedelta(days=10),
                               enddatetime=datetime.datetime.utcnow() - datetime.timedelta(days=9))

    if db(db.resolve.resolve_name == "Standard").isempty():
        resolveid = db.resolve.insert(resolve_name="Standard", Defaultresolve=True)
    if db(db.resolve.resolve_name == "Single").isempty():
        resolveid = db.resolve.insert(resolve_name="Single", responses=1)
    if db(db.resolve.resolve_name == "Self").isempty():
        resolveid = db.resolve.insert(resolve_name="Self", responses=1,
                                      desc='Creator has resolved themselves or based on knowledge engine answers ')

    # These will require a degree of manual setup and the new_question js and new_quest js scripts at least will
    # require tweaking if new engines are added think we add gemini as second ai engine and put those in 
    # auth user table to allow them to generate and answer questions within the model will have the user ids created 
    # by this setup in knowledge table - plan to just setup openai first
    if db(db.knowledge.source == "None").isempty():
        kid = db.knowledge.insert(source="None", title="None", defaultknowledge=True)

    if db(db.knowledge.source == "Wolfram").isempty():
        kid = db.knowledge.insert(source="Wolfram", title="Wolfram Alpha")

    if db(db.knowledge.source == "Wikipedia").isempty():
        kid = db.knowledge.insert(source="Wikipedia", title="Wikipedia")

    if db(db.knowledge.source == "GPT3").isempty():
        uid = db.auth_user.insert(user="GPT", username='OpenAI', password='NotApplicable',
                                  first_name = 'OpenAI', last_name ='GPT')
        kid = db.knowledge.insert(source="GPT3", title="OpenAI GPT-3", uid=uid)

    # create current user in manager group if not presently there - this allows actual tweetting
    # as yet no other user admin functions setup
    managers = db(groups.find(['manager'])).select()
    print('man', len(managers))
    if not len(managers):
        groups.add(auth.user_id, 'manager')

    return locals()


@authenticated()
def aisetup():
    # This should create some default prompts for openai models currently potentially other LLMs
    # will use similar approach
    reset_ai = False

    # Think the general approach will be same as datasetup ie
    # first look for each of the relevant records
    # if there then unless reset_ai is True we do nothing
    # if true we would update it
    model = 'OpenAI GPT-3'
    aimodel = db(db.knowledge.title == model).select().first()
    if aimodel:
        ai = aimodel.id
    else:
        print(f'AI model {model} not found')
        return()

    # let go with scenario, prompt type sequence and prompt_test text in the list
    # so may need this to be more dynamic based on whether follow on is from question/issue/or action??

    prompts = [["answer", "system", 10, 'You are an expert providing guidance to improve the world'],
               ["answer", "user", 20, 'To do this you need to answer multiple choice questions'],
               ["answer", "user", 22, 'There can be up to 4 answers and you should provide the correct answer in JSON format'],
               ["answer", "user", 24, 'With the number and the reason for the chosen answer'],
               ["answer", "user", 48, 'The question is:'],
               ["gen_questions", "system", 1, 'You are an expert providing guidance to improve the world'],
               ["gen_questions", "user", 10, 'The following item has been identified'],
               ["gen_questions", "user", 60, 'Suggest 3 follow-on questions to further investigate the issue '],
               ["gen_questions", "user", 70, 'The questions should be in a format to support yes or no answers'],
               ["gen_actions", "system", 1, 'You are an expert providing guidance to improve the world'],
               ["gen_actions", "user", 10, 'The following issue has been identified'],
               ["gen_actions", "user", 60, 'Suggest 3 follow-on actions to address'],
               ["gen_issues", "system", 1, 'You are an expert providing guidance to improve the world'],
               ["gen_issues", "user", 10, 'The following item has been identified'],
               ["gen_issues", "user", 60, 'Suggest 3 further issues to investigate'],
               ["gen_answers", "user", 20, 'You are helping to create multiple choice questions for people to answer'],
               ["gen_answers", "user", 25, 'You should provide 4 possible answers to the question in JSON format with'],
               ["gen_answers", "user", 27, 'the number and text of each answer provided as separate fields'],
               ["gen_answers", "user", 30, 'At least one answer should be correct but the others need not be'],
               ["gen_answers", "user", 45, 'The question is:']
]

    for x in prompts:
        if db((db.prompt.scenario == x[0]) & (db.prompt.sequence == x[2])).isempty():
            db.prompt.insert(chosenai=ai, scenario=x[0], role=x[1], sequence=x[2], content=x[3])
        else:
            print(f'{x[0]}, {x[2]} already exists')

    return locals()
