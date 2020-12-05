
import datetime
from py4web import action, request, abort, redirect, URL
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated


@auth.requires_login()
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

    if db(db.evt.evt_name == "Unspecified").isempty():
        locid = db(db.locn.location_name == 'Unspecified').select(db.locn.id).first().id
        evid = db.evt.insert(evt_name="Unspecified", locationid=locid, evt_shared=True,
                             startdatetime=request.utcnow - datetime.timedelta(days=10),
                             enddatetime=request.utcnow - datetime.timedelta(days=9))

    # Now adding resolved as normal option to assist with test and support chain of thought
    if db(db.resolve.resolve_name == "Standard").isempty():
        resolveid = db.resolve.insert(resolve_name="Standard")

    if db(db.resolve.resolve_name == "Single").isempty():
        resolveid = db.resolve.insert(resolve_name="Single")

    return locals()

