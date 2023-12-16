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
from ..common import db, authenticated, auth
from pydal.tools.tags import Tags
groups = Tags(db.auth_user, tag_table=db.auth_user_tag_groups)


@action('admin', method=['POST', 'GET'])
@action('tweetgrid/<path:path>', method=['POST', 'GET'])
@action.uses('admin.html', session, db, flash, auth.user)
def  admin():
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
    # require tweaking if new engines are added
    if db(db.knowledge.source == "None").isempty():
        kid = db.knowledge.insert(source="None", title="None", defaultknowledge=True)

    if db(db.knowledge.source == "Wolfram").isempty():
        kid = db.knowledge.insert(source="Wolfram", title="Wolfram Alpha")

    if db(db.knowledge.source == "Wikipedia").isempty():
        kid = db.knowledge.insert(source="Wikipedia", title="Wikipedia")

    if db(db.knowledge.source == "GPT3").isempty():
        kid = db.knowledge.insert(source="GPT3", title="OpenAI GPT-3")

    # create current user in manager group if not presently there - this allows actual tweetting
    # as yet no other user admin functions setup
    managers = db(groups.find(['manager'])).select()
    print('man', len(managers))
    if not len(managers):
        groups.add(auth.user_id, 'manager')

    return locals()
