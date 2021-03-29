"""
This file defines the database models
"""
from .common import db, auth, T
from py4web import Field
from pydal.validators import *
import datetime

not_empty = IS_NOT_EMPTY()
# TODO setup auth extra fields again to extent still required

db.define_table('resolve',
                Field('resolve_name', 'string', default='Standard', label='Name',
                      requires=[not_empty, IS_NOT_IN_DB(db, 'resolve.resolve_name')]),
                Field('responses', 'integer', default=3, label='Min Number of Responses before resolution'),
                Field('consensus', 'decimal(4,4)', default=60,
                      requires=IS_DECIMAL_IN_RANGE(50.01, 100, error_message='Must be in range 50.01 to 100'),
                      label='Percentage Agmt required to resolve'),
                Field('Defaultresolve', 'boolean', default=False),
                Field('adminresolve', 'boolean', default=True,label='Allow event owners to resolve on behalf of group'),
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
                Field('self_resolve', 'boolean', default=True, label=T('Allow self resolved actions')),
                Field('self_answer', 'boolean', default=True, label=T('Allow self-answer questions')),
                Field('anon_resolve', 'boolean', default=False, label=T('Anonymous answers on resolve')),
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
                      comment=T('Port of the mailserver (used to send email in forms)')))
db.website_parameters.website_url.requires = IS_EMPTY_OR(IS_URL())

# this was to support document download from site eg manuals setup instructions etc
db.define_table('download',
                Field('title'),
                Field('download_file', 'upload'),
                Field('description', 'text'),
                Field('download_version', 'string', default='1'),
                format='%(title)s')
db.download.title.requires = IS_NOT_IN_DB(db, db.download.title)

db.define_table('locn',
                Field('location_name', label='Location Name', unique=True, notnull=True),
                Field('address1', label='Address 1'),
                Field('address2', label='Address 2'),
                Field('address3', label='Address 3'),
                Field('address4', label='Address 4'),
                Field('addrcode', label='Postal Code'),
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
db.locn.addrurl.requires = IS_EMPTY_OR(IS_URL())

db.define_table('project',
                Field('proj_name', label='Project Name', unique=True, notnull=True),
                Field('proj_url', label='Project Website'),
                Field('proj_status', 'string', label='Project Status', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('answer_group', 'string', default='Unspecified', label='Restrict Project to Group'),
                Field('startdate', 'date', label='Start Date', default=datetime.datetime.utcnow),
                Field('enddate', 'date', label='End Date', default=(datetime.datetime.utcnow)),
                Field('description', 'text'),
                Field('proj_shared', 'boolean', label='Shared Project', comment='Allows other users to link events'),
                Field('proj_owner', 'reference auth_user', writable=False, readable=False,
                      label='Owner', default=auth.user_id),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False),
                format='%(proj_name)s')


db.define_table('event',
                Field('event_name', label='Event Name', unique=False, notnull=True),
                Field('locationid', 'reference locn', label='Location'),
                Field('projid',  'reference project',  label='Project', notnull=True),
                Field('status', 'string', default='Open', requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('startdatetime', 'datetime', label='Start Date Time'),
                Field('enddatetime', 'datetime', label='End Date Time'),
                Field('description', 'text'),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False),
                Field('next_event', 'integer', default=0, writable=False, readable=False, label='Next Event'),
                Field('prev_event', 'integer', default=0, writable=False, readable=False, label='Previous Event'),
                Field('recurrence', 'string', default='None',
                      requires=IS_IN_SET(['None', 'Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'])),
                format='%(event_name)s')


db.define_table('question',
                Field('qtype', 'string', label='Item Type',
                      requires=IS_IN_SET(['quest', 'action', 'issue']), default='quest'),
                Field('questiontext', 'text', label='Question Action Issue', requires=not_empty),
                Field('status', 'string', default='In Progress',
                      requires=IS_IN_SET(['Draft', 'In Progress', 'Resolved', 'Rejected']),
                      comment='Select draft to defer for later editing'),
                Field('auth_userid', 'reference auth_user', readable=False, writable=False, label='Submitter',
                      default=auth.user_id, notnull=True),
                Field('factopinion', 'string', default='Opinion',
                      requires=IS_IN_SET(['Fact', 'Opinion']), label='Fact or Opinion',
                      comment='Factual questions should be answered by either submitter or knowledge engines'),
                Field('answertext', 'text', label='Fact Answer'),
                Field('answer1', 'string'),
                Field('answer2', 'string'),
                Field('numanswer1', 'integer', default=0, readable=False, writable=False),
                Field('numanswer2', 'integer', default=0, readable=False, writable=False),
                Field('correctans', 'integer', readable=False, writable=False, label='Correct Ans'),
                Field('urgency', 'decimal(6,2)', default=5, readable=False, writable=False, label='Urgency'),
                Field('importance', 'decimal(6,2)', default=5, readable=False, writable=False, label='Importance'),
                Field('totratings', 'integer', default=0, readable=False, writable=False,
                      label='Total numbers of ratings'),
                Field('numlike', 'integer', default=0, readable=False, writable=False,
                      label='Total numbers of likes'),
                Field('priority', 'decimal(6,2)', readable=False, compute=lambda r: r['urgency'] * r['importance'],
                      writable=False, label='Priority'),
                Field('resolvemethod', 'reference resolve', label='Resolution Method', notnull=True),
                Field('createdate', 'datetime', readable=False, writable=False, default=datetime.datetime.utcnow,
                      label='Date Submitted'),
                Field('resolvedate', 'datetime', readable=False, writable=False, label='Date Resolved'),
                Field('responsible', label='Responsible'),
                Field('startdate', 'datetime', readable=False, writable=False,
                      default=(datetime.datetime.utcnow), label='Date Action Starts'),
                Field('enddate', 'datetime', readable=False, writable=False,
                      default=(datetime.datetime.utcnow), label='Date Action Ends'),
                Field('eventid', 'reference event', label='Event'),
                Field('shared_editing', 'boolean', default=True, label='Shared Edit',
                      comment='Allow anyone to edit action status and dates'),
                Field('xpos', 'double', default=0.0, label='xcoord'),
                Field('ypos', 'double', default=0.0, label='ycoord'),
                Field('perccomplete', 'integer', default=0, label='Percent Complete',
                      requires=IS_INT_IN_RANGE(0, 101, error_message='Must be between 0 and 100')),
                Field('notes', 'text', label='Notes',
                      comment='General notes about question - may also document answers from knowledge engines'),
                Field('execstatus', 'string', label='Execution Status', default='Proposed',
                      requires=IS_IN_SET(['Proposed', 'Planned', 'In Progress', 'Completed'])))

db.question.correctanstext = Field.Lazy(lambda row: ((row.question.correctans == 1 and row.question.answer1) or
                                                     (row.question.correctans == 2 and row.question.answer2) or ''))

#db.question.resolvemethod.default = db(db.website_parameters.id > 0).select(
#    db.website_parameters.id).first().id or None
# So thinking that we just support two answers for everything - and maybe Yes No is simple enough for everything that
# is an action, issue or question (not of fact).  Questions of fact should generally be referred to knowledge engines
# but probably want answertext as well - they are not generally ciruclated - as should be answered at creation

db.define_table('userquestion',
                Field('questionid', db.question, writable=False, notnull=True),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, notnull=True),
                Field('answer', 'integer', default=0, label='My Answer'),
                Field('reject', 'boolean', default=False),
                Field('answerreason', 'text', label='Reasoning'),
                Field('ansdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False))

db.define_table('uqrating',
                Field('questionid', db.question, writable=False, notnull=True),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, notnull=True),
                Field('urgency', 'integer', default=5,
                      requires=IS_INT_IN_RANGE(1, 11, error_message='Must be between 1 and 10')),
                Field('importance', 'integer', default=5,
                      requires=IS_INT_IN_RANGE(1, 11, error_message='Must be between 1 and 10')),
                Field('ratingdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False))


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
                Field('createdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False))

# below is being adapted to hold comments against any object
db.define_table('comment',
                Field('parentid', 'integer', writable=False, readable=False),
                Field('parenttable', 'string', default='question', writable=False, readable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('comment', 'text', requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='OK', writable=False, readable=False,
                      requires=IS_IN_SET(['OK', 'NOK'])),
                Field('numreject', 'integer', default=0, writable=False, readable=False),
                Field('usersreject', 'list:integer', writable=False, readable=False),
                Field('commentdate', 'datetime', default=datetime.datetime.utcnow, writable=False, readable=False))

db.comment.parenttable.requires = IS_IN_SET(['question', 'project', 'event'])

db.define_table('eventmap',
                Field('eventid', 'reference event', notnull=True),
                Field('questid', 'reference question', notnull=True),
                Field('xpos', 'double', default=0.0, label='xcoord'),
                Field('ypos', 'double', default=0.0, label='ycoord'),
                Field('qtype', 'string', writable=False, requires=IS_IN_SET(['quest', 'action', 'issue'])),
                Field('status', 'string', default='In Progress', requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('questiontext', 'text', writable=False, label='Question'),
                Field('answer1', 'string', writable=False),
                Field('answer2', 'string', writable=False),
                Field('correctans', 'integer', readable=False, writable=False, label='Correct Ans'),
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
                      requires=IS_IN_SET(['Draft', 'In Progress', 'Resolved', 'Rejected', 'Admin Resolved']),
                      comment='Select draft to defer for later editing'),
                Field('notes', 'text', label='Notes'))


db.eventmap.correctanstext = Field.Lazy(lambda row: ((row.eventmap.correctans == 1 and row.eventmap.answer1) or
                                                     (row.eventmap.correctans == 2 and row.eventmap.answer2) or ''))

# will also support likes against any item including comments
db.define_table("itemlike",
                Field('parentid', 'integer'),
                Field('parenttable', 'string', default='question'),
                Field('createdby', 'reference auth_user', default=auth.get_user().get("id")),
                Field('liketype', 'string', default='like'),
                Field('likedate', 'datetime', default=datetime.datetime.utcnow))

db.commit()
