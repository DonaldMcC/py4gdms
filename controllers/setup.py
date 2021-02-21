import datetime
from py4web import action, redirect, URL
from ..common import db, session, auth, authenticated, unauthenticated


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
        locid = db.locn.insert(location_name="Unspecified", locn_shared=True,
                               description='The unspecified location is used as a default for all events that are not'
                                           'allocated a specific location')

    if db(db.project.proj_name == "Unspecified").isempty():
        projid = db.project.insert(proj_name="Unspecified",
                               description='The unspecified project is used as a default for all project that are not'
                                           'allocated a specific project')

    if db(db.evt.evt_name == "Unspecified").isempty():
        locid = db(db.locn.location_name == 'Unspecified').select(db.locn.id).first().id
        projid = db(db.locn.location_name == 'Unspecified').select(db.locn.id).first().id
        evid = db.evt.insert(evt_name="Unspecified", locationid=locid, projid=projid, evt_shared=True,
                             startdatetime=datetime.datetime.utcnow() - datetime.timedelta(days=10),
                             enddatetime=datetime.datetime.utcnow() - datetime.timedelta(days=9))

    if db(db.resolve.resolve_name == "Standard").isempty():
        resolveid = db.resolve.insert(resolve_name="Standard", Defaultresolve=True)

    if db(db.resolve.resolve_name == "Single").isempty():
        resolveid = db.resolve.insert(resolve_name="Single", responses=1)

    return locals()
