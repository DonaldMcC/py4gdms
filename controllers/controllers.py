# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/py4gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#   http://netdecisionmaking.com/gdmsdemo/
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


# This controller provides details about network decision making
# and access to the FAQ

from ..common import db, unauthenticated, authenticated


@unauthenticated()
def about():
    return dict(message="all done in the view")


@unauthenticated()
def privacy():
    return dict(message="all done in the view")


@unauthenticated()
def faq():
    return dict(message="all done in the view")


@unauthenticated()
def present():
    return dict(message="all done in the view")


@unauthenticated()
def enhance():
    return dict(message="all done in the view")


@authenticated()
def download():
    downloads = db().select(db.download.ALL, orderby=db.download.title)
    return dict(downloads=downloads)
