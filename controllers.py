"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated


@unauthenticated()
@action("index")
@action.uses(auth, "index.html")
def index():
    user = auth.get_user()
    message = T("Hello {first_name}".format(**user) if user else "Hello")
    return dict(message=message, flash="Hello world")



@action("new_project")
@action.uses('new_project.html', session)
def new_project():
    # This allows creation and editing of projects by their owner
    # 'answer_group' removed as no other security functions for projects and events yet - not currently needed
    #fields = ['proj_name', 'description', 'proj_url', 'startdate', 'enddate', 'proj_shared']
    #projid = request.args(0, default=None)
    #if projid is not None:
    #    record = db.project(projid)
    #    if record.proj_owner != auth.user_id:
    #        session.flash = 'Not Authorised - projects can only be edited by their owners'
    #        redirect(URL('new_project'))
    #    form = SQLFORM(db.project, record, fields=fields)
    #else:
    form = Form(db.project)

    #if form.validate():
    #    if projid is not None:
    #        if form.deleted:
    #            db(db.project.id == projid).delete()
    #            response.flash = 'Project deleted'
    #            redirect(URL('default', 'index'))
    #        else:
    #            record.update_record(**dict(form.vars))
    #            response.flash = 'Project updated'
    #            redirect(URL('default', 'index'))
    #    else:
    #        form.vars.id = db.project.insert(**dict(form.vars))
    #        session.flash = 'Project Created'
    #        redirect(URL('accept_project', args=[form.vars.id, auth.user_id]))
    #elif form.errors:
    #    response.flash = 'form has errors'
    #else:
    #    response.flash = 'please fill out the form'

    return dict(form=form)