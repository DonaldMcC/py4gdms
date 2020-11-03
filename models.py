"""
This file defines the database models
"""

from .common import db, auth, T, session
from py4web import Field, request
from pydal.validators import *
import datetime

not_empty = IS_NOT_EMPTY()
# TODO setup auth extra fields again to extent still required

db.define_table('resolve',
                Field('resolve_name', 'string', default='Standard', label='Name',
                      requires=[not_empty, IS_NOT_IN_DB(db, 'resolve.resolve_name')]),
                Field('description', 'text', default='Explain how the resolution method works',
                      label='Description of resolution method'),
                Field('resolve_method', 'string', default='Network', requires=IS_IN_SET(['Network', 'Vote'])),
                Field('responses', 'integer', default=3, label='Number of Responses before evaluation'),
                Field('consensus', 'double', default=100, label='Percentage Agmt required to resolve'),
                Field('userselect', 'boolean', default=True, label='Allow users to select to answer'),
                Field('adminresolve', 'boolean', default=True,
                      label='Allow event owners to resolve on behalf of group'),
                format='%(resolve_name)s')


db.define_table('website_parameters',
                Field('system_scope', 'string'),
                Field('website_name', label=T('Website name'), comment=T('Not currently used')),
                Field('website_init', 'boolean', default=False, label=T('Website Setup'),
                      comment=T('Set to True once initialised')),
                Field('website_title', label=T('Website title'), comment=T('Displayed in title if not blank')),
                Field('website_subtitle', label=T('Website subtitle'), comment=T('Not used')),
                Field('website_url', label=T('Url'), comment=T('URL of the website used for emailing external links')),
                Field('longdesc', 'text', label=T('Long Description'), comment=T('Subject of the website')),
                Field('shortdesc', label=T('Url'), comment=T('Short Description of the website')),
                Field('level1desc', label=T('Level1Desc'), comment=T('First Location Level')),
                Field('level2desc', label=T('Level2Desc'), comment=T('Second Location Level')),
                Field('level3desc', label=T('Level3Desc'), comment=T('Third Location Level')),
                Field('copyright', label=T('Copyright'),
                      default='Has probably been eliminated on more advanced planets'),
                Field('self_resolve', 'boolean', default=True, label=T('Allow self resolved actions')),
                Field('self_answer', 'boolean', default=True, label=T('Allow self-answer questions')),
                Field('anon_resolve', 'boolean', default=False, label=T('Anonymous answers on resolve')),
                Field('force_language', label=T('Force a language (en, it, es, fr, ...)')),
                Field('google_analytics_id', label=T('Google analytics id'),
                      comment=T('Your Google Analytics account ID')),
                Field('seo_website_title', label=T('SEO : Website title'),
                      comment=T('Displayed in <title> tag of the HTML source code')),
                Field('seo_meta_author', label=T('SEO : Meta "author"'),
                      comment=T('Displayed in <meta author> tag of the HTML source code')),
                Field('seo_meta_description', label=T('SEO : Meta "description"'),
                      comment=T('Displayed in <meta description> tag of the HTML source code')),
                Field('seo_meta_keywords', label=T('SEO : Meta "keywords"'),
                      comment=T('Displayed in <meta keywords> tag of the HTML source code')),
                Field('seo_meta_generator', label=T('SEO : Meta "generator"'),
                      comment=T('Displayed in <meta generator> tag of the HTML source code')),
                Field('quests_per_page', 'integer', default=20, label=T('Questions Per Page'),
                      comment=T('Port of the mailserver (used to send email in forms)')),
                Field('comments_per_page', 'integer', default=20, label=T('Comments Per Page'),
                      comment=T('Port of the mailserver (used to send email in forms)')),
                Field('default_resolve_name', 'string', default='Standard', label='Default Resolve Name'))
db.website_parameters.website_url.requires = IS_EMPTY_OR(IS_URL())
db.website_parameters.default_resolve_name.requires = IS_EMPTY_OR(IS_IN_DB(db, 'resolve.resolve_name'))


db.define_table('category',
                Field('cat_desc', 'string', label='Category',
                      requires=[not_empty, IS_NOT_IN_DB(db, 'category.cat_desc'), IS_LOWER()]),
                Field('categorydesc', 'text', label='Description'),
                format='%(cat_desc)s')

# this was to support document download from site eg manuals setup instructions etc
db.define_table('download',
                Field('title'),
                Field('download_file', 'upload'),
                Field('description', 'text'),
                Field('download_version', 'string', default='1'),
                format='%(title)s')
db.download.title.requires = IS_NOT_IN_DB(db, db.download.title)


db.define_table('locn',
                Field('location_name', label='Location Name', requires=[not_empty,
                                                                        IS_NOT_IN_DB(db, 'locn.location_name')]),
                Field('address1', label='Address 1', writable=False, readable=False),
                Field('address2', label='Address 2', writable=False, readable=False),
                Field('address3', label='Address 3', writable=False, readable=False),
                Field('address4', label='Address 4', writable=False, readable=False),
                Field('addrcode', label='Postal Code', writable=False, readable=False),
                Field('addrurl', label='Location Website'),
                Field('country', default='Unspecified', label='Country'),
                Field('subdivision', default='Unspecified', label='Subdivision'),
                Field('coord', label='Lat/Longitude'),  # ignore values in this field
                Field('locn_long', 'double', default=0.0, label='Latitude', writable=False, readable=False),
                Field('locn_lat', 'double', default=0.0, label='Longitude', writable=False, readable=False),
                Field('description', 'text'),
                Field('locn_shared', 'boolean', label='Shared', default=True,
                      comment='Allows other users to link events'),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, default=auth.user_id),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False),
                format='%(location_name)s')
db.locn.location_name.requires = IS_NOT_IN_DB(db, db.locn.location_name)
db.locn.addrurl.requires = IS_EMPTY_OR(IS_URL())


db.define_table('project',
                Field('proj_name', label='Project Name'),
                Field('proj_url', label='Project Website'),
                Field('proj_status', 'string', label='Project Status', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('answer_group', 'string', default='Unspecified', label='Restrict Project to Group'),
                Field('startdate', 'date', label='Start Date',
                      default=datetime.datetime.utcnow()),
                Field('enddate', 'date', label='End Date',
                      default=(datetime.datetime.utcnow() + datetime.timedelta(days=365))),
                Field('description', 'text'),
                Field('proj_shared', 'boolean', default=True, label='Shared Project',
                      comment='Allows other users to link questions'),
                Field('proj_owner', 'reference auth_user', writable=False, readable=False,
                      label='Owner', default=auth.user_id),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                format='%(proj_name)s')
db.project.proj_name.requires = IS_NOT_IN_DB(db, db.project.proj_name)


db.define_table('evt',
                Field('evt_name', label='Event Name'),
                Field('locationid', 'reference locn', label='Location'),
                Field('projid', 'reference project', label='Project'),
                Field('status', 'string', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('startdatetime', 'datetime', label='Start Date Time',
                      default=(datetime.datetime.utcnow() + datetime.timedelta(days=10))),
                Field('enddatetime', 'datetime', label='End Date Time',
                      default=(datetime.datetime.utcnow() + datetime.timedelta(days=11))),
                Field('description', 'text'),
                Field('evt_shared', 'boolean', default=True, label='Shared Event',
                      comment='Allows other users to link questions'),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                Field('next_evt', 'integer', default=0, writable=False, readable=False, label='Next Event'),
                Field('prev_evt', 'integer', default=0, writable=False, readable=False, label='Previous Event'),
                Field('recurrence', 'string', default='None',
                      requires=IS_IN_SET(['None', 'Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'])),
                format='%(evt_name)s')
db.evt.evt_name.requires = [not_empty, IS_NOT_IN_DB(db, 'evt.evt_name')]


db.define_table('question',
                Field('qtype', 'string', label='Item Type',
                      requires=IS_IN_SET(['quest', 'action', 'issue']), default='quest'),
                Field('questiontext', 'text', label='Question Action Issue', requires=not_empty),
                Field('status', 'string', default='In Progress',
                      requires=IS_IN_SET(['Draft', 'In Progress', 'Resolved', 'Rejected']),
                      comment='Select draft to defer for later editing'),
                Field('auth_userid', 'reference auth_user', writable=False, label='Submitter', default=auth.user_id),
                Field('factopinion', 'string', default='Opinion',
                      requires=IS_IN_SET(['Fact', 'Opinion']), label='Fact or Opinion'),
                Field('answertext', 'text', label='Fact Answer', requires=not_empty,
                      comment='Factual questions should be answered by either submitter or knowledge engines '),
                Field('answer1', 'string'),
                Field('answer2', 'string'),
                Field('correctans', 'integer', writable=False, label='Correct Ans'),
                Field('urgency', 'decimal(6,2)', default=5, writable=False, label='Urgency'),
                Field('importance', 'decimal(6,2)', default=5, writable=False, label='Importance'),
                Field('priority', 'decimal(6,2)', compute=lambda r: r['urgency'] * r['importance'], writable=False,
                      label='Priority'),
                Field('othercounts', 'list:integer', default=[0, 0, 0, 0, 0, 0, 0, 0], readable=False, writable=False,
                      comment='numanswer1, numanswer2, numpass, numchallenges, numchallenged, numagree, numdisagree, numcomments'),
                Field('subquests', 'list:integer', writable=False),
                Field('resolvemethod', 'string', default='Standard', writable=False, label='Resolution Method'),
                Field('createdate', 'datetime', writable=False, default=datetime.datetime.utcnow(),
                      label='Date Submitted'),
                Field('resolvedate', 'datetime', writable=False, label='Date Resolved'),
                Field('challengedate', 'datetime', writable=False, label='Date Challenged'),
                Field('answerreasons', 'list:string', writable=False, label='Answer Reasons'),
                Field('responsible', label='Responsible'),
                Field('startdate', 'datetime', default=datetime.datetime.utcnow(), label='Date Action Starts'),
                Field('enddate', 'datetime', default=datetime.datetime.utcnow(), label='Date Action Ends'),
                Field('eventid', 'reference evt', label='Event'),
                Field('projid', 'reference project', label='Project'),
                Field('challenge', 'boolean', default=False),
                Field('shared_editing', 'boolean', default=True, label='Shared Edit',
                      comment='Allow anyone to edit action status and dates'),
                Field('xpos', 'double', writable=False, default=0.0, label='xcoord'),  # x pos on the eventmap
                Field('ypos', 'double', writable=False, default=0.0, label='ycoord'),  # y pos on the eventmap
                Field('perccomplete', 'integer', default=0, label='Percent Complete', requires=IS_INT_IN_RANGE(0, 101,
                                                                                                               error_message='Must be between 0 and 100')),
                Field('notes', 'text', label='Notes',
                      comment='General notes about question - may also document answers from knowledge engines'),
                Field('execstatus', 'string', label='Execution Status', default='Proposed',
                      requires=IS_IN_SET(['Proposed', 'Planned', 'In Progress', 'Completed'])))

# So thinking that we just support two answers for everything - and maybe Yes No is simple enough for everything that
# is an action, issue or question (not of fact).  Questions of fact should generally be referred to knowledge engines
# but probably want answertext as well - they are not generally ciruclated - as should be answered at creation


db.define_table('userquestion',
                Field('questionid', db.question, writable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('status', 'string', default='In Progress', writable=False, readable=False),
                Field('answer', 'integer', default=0, label='My Answer'),
                Field('reject', 'boolean', default=False),
                Field('urgency', 'integer', default=5, requires=IS_INT_IN_RANGE(1, 11,
                                error_message='Must be between 1 and 10')),
                Field('importance', 'integer', default=5, requires=IS_INT_IN_RANGE(1, 11,
                                error_message='Must be between 1 and 10')),
                Field('score', 'integer', default=0, writable='False'),
                Field('answerreason', 'text', label='Reasoning'),
                Field('ansdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                Field('resolvedate', 'datetime', writable=False, label='Date Resolved'))


db.define_table('questchallenge',
                Field('questionid', 'reference question', writable=False, readable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('status', 'string', default='In Progress', writable=False, readable=False),
                Field('challengereason', 'text'),
                Field('challengedate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False))

# this holds details of who has agreed and disagreed on the answer to a question
# no points are awarded for this at present but it may be configured to prevent
# challenges if the agreement to disagreement ratio is above some point this will also
# now support logging agreement to actions and so urgency and importance have been
# added to this table - however they are also picked up in userquestion - thinking is
# questions will not show this but actions will ie will pick-up in one place only
# Some users may want to record agreement without ranking immediately - but will
# accept their default values for now as no way of knowing if intended or not


db.define_table('questagreement',
                Field('questionid', 'reference question', writable=False),
                Field('auth_userid', 'reference auth_user', writable=False),
                Field('agree', 'integer', writable=False, readable=False),
                Field('agreedate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                Field('urgency', 'integer', default=0, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('importance', 'integer', default=0, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('agmt_level', 'integer', default=1, readable=False, writable=False))


db.define_table('questurgency',
                Field('questionid', 'reference question', writable=False),
                Field('auth_userid', 'reference auth_user', writable=False),
                Field('urgency', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('importance', 'integer', default=5, requires=IS_IN_SET([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])),
                Field('urge_level', 'integer', default=1, readable=False, writable=False))

# questlinks replaces priorquests and subsquests in the questtion table at present as
# list reference fields weren't going to be enough to provide funcionality to
# allow creation and deletion of links I now think the record gets deleted
# when delete count exceeds createcount and deletecount is also greater than one
# so that may mean that status can be a computed field but would need to be queried on
# so not a virtual field
# may need to rethink links as going more event focussed but some things may get carried over and others not??


db.define_table('questlink',
                Field('sourceid', 'reference question'),
                Field('targetid', 'reference question'),
                Field('linktype', 'string', default='Std', requires=IS_IN_SET(['Std', 'Conflict'])),
                Field('createdby', 'reference auth_user', default=auth.user_id),
                Field('createcount', 'integer', default=1),
                Field('deletecount', 'integer', default=0),
                Field('status', 'string', default='Active', requires=IS_IN_SET(['Draft', 'Active', 'Rejected'])),
                Field('lastdeleter', 'reference auth_user'),
                Field('lastaction', 'string', default='create'),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False))

# this holds comments for resolved questions
# it may be extended to allow comments against unresolved but not yet
# it will allow comments against actions that are proposed
# which is now a new status on actions where preceding question is not resolved
# and on follow-up questions

db.define_table('questcomment',
                Field('questionid', 'reference question', writable=False, readable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False,
                      default=auth.user_id),
                Field('qc_comment', 'text', requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='OK', writable=False, readable=False,
                      requires=IS_IN_SET(['OK', 'NOK'])),
                Field('numreject', 'integer', default=0, writable=False, readable=False),
                Field('usersreject', 'list:integer', writable=False, readable=False),
                Field('commentdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False))


db.define_table('eventmap',
                Field('eventid', 'reference evt'),
                Field('questid', 'reference question'),
                Field('xpos', 'double', default=0.0, label='xcoord'),
                Field('ypos', 'double', default=0.0, label='ycoord'),
                Field('qtype', 'string', writable=False, requires=IS_IN_SET(['quest', 'action', 'issue'])),
                Field('status', 'string', default='In Progress', requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('questiontext', 'text', writable=False, label='Question'),
                Field('answers', 'list:string', writable=False),
                Field('correctans', 'integer', default=-1, label='Correct Ans'),
                Field('answer_group', 'string', default='Unspecified', label='Submit to Group',
                      comment='Restrict answers to members of a group'),
                Field('urgency', 'decimal(6,2)', default=5, writable=False, label='Urgency'),
                Field('importance', 'decimal(6,2)', default=5, writable=False, label='Importance'),
                Field('priority', 'decimal(6,2)', compute=lambda r: r['urgency'] * r['importance'], writable=False,
                      label='Priority'),
                Field('auth_userid', 'reference auth_user', writable=False, label='Submitter', default=auth.user_id),
                Field('adminresolve', 'boolean', default=False,
                      label='True if answer or status adjusted by event owner'),
                Field('responsible', label='Responsible'),
                Field('eventlevel', 'integer', default=0),
                Field('masterquest', 'integer', default=0),
                Field('subquests', 'list:integer'),
                Field('queststatus', 'string', default='In Progress',
                      requires=IS_IN_SET(
                          ['Draft', 'In Progress', 'Resolved', 'Rejected', 'Admin Resolved']),
                      comment='Select draft to defer for later editing'),
                Field('notes', 'text', label='Notes'))


db.commit()
