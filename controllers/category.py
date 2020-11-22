# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#


from py4web import action, request, abort, redirect, URL
from py4web.utils.form import Form
from ..common import db, session, T, cache, auth, logger, authenticated, unauthenticated

@action("new_category", method=['GET', 'POST'])
@action.uses('new_category.html', session, db)
def new_category():
    form = Form(db.category)

    # if form.validate():
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
    # elif form.errors:
    #    response.flash = 'form has errors'
    # else:
    #    response.flash = 'please fill out the form'

    return dict(form=form)
