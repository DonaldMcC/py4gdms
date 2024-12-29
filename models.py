"""
This file defines the database models
"""
from pydal.validators import IS_DECIMAL_IN_RANGE
from pydal.validators import *
from . import settings
from .common import db, T
from py4web import Field
import datetime

not_empty = IS_NOT_EMPTY()

db.define_table('resolve',
                Field('resolve_name', 'string', default='Standard', label='Name',
                      requires=[not_empty, IS_NOT_IN_DB(db, 'resolve.resolve_name')]),
                Field('responses', 'integer', default=3, label='Min Number of Responses before resolution'),
                Field('consensus', 'decimal(4,4)', default=63,
                      requires=IS_DECIMAL_IN_RANGE(50.01, 100, error_message='Must be in range 50.01 to 100'),
                      label='Percentage Agmt required to resolve'),
                Field('Defaultresolve', 'boolean', label='Default Resolution Method', default=False),
                Field('adminresolve', 'boolean', label='Allow event owners to resolve'),
                Field('owner', 'reference auth_user', readable=False, writable=False, label='Submitter'),
                Field('desc', 'text', label='Description'),
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
                Field('download_file', 'upload', uploadfolder=settings.UPLOAD_FOLDER),
                Field('description', 'text'),
                Field('download_version', 'string', default='1'),
                format='%(title)s')
db.download.title.requires = IS_NOT_IN_DB(db, db.download.title)


db.define_table('knowledge',
                Field('source'),
                Field('title'),
                Field('defaultknowledge', 'boolean', label='Default Knowledge Engine', default=False),
                format='%(title)s')


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
                Field('locn_long', 'double', default=0.0, writable=False, readable=False),
                Field('locn_lat', 'double', default=0.0, writable=False, readable=False),
                Field('description', 'text'),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('createdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False),
                Field('locked', 'boolean', readable=False, writable=False),
                format='%(location_name)s')
db.locn.addrurl.requires = IS_EMPTY_OR(IS_URL())


db.define_table('project',
                Field('proj_name', label='Project Name', unique=True, notnull=True),
                Field('proj_url', label='Project Website'),
                Field('proj_status', 'string', label='Project Status', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('answer_group', 'string', default='Unspecified', label='Restrict Project to Group'),
                Field('startdate', 'date', label='Start Date', default=datetime.datetime.now),
                Field('enddate', 'date', label='End Date', default=datetime.datetime.now),
                Field('description', 'text'),
                Field('proj_shared', 'boolean', default=True, label='Shared Project',
                      comment='Allows other users to link events'),
                Field('proj_owner', 'reference auth_user', writable=False, readable=False),
                Field('createdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False),
                Field('locked', 'boolean', readable=False, writable=False),
                Field('priority', 'decimal(6,2)', default=0),
                format='%(proj_name)s')
db.project.proj_url.requires = IS_EMPTY_OR(IS_URL())


db.define_table('event',
                Field('event_name', label='Event Name', unique=False, notnull=True),
                Field('locationid', 'reference locn', label='Location', notnull=True),
                Field('projid', 'reference project', label='Project', notnull=True),
                Field('status', 'string', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('startdatetime', 'datetime', label='Start Date Time'),
                Field('enddatetime', 'datetime', label='End Date Time'),
                Field('description', 'text'),
                Field('createdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False),
                Field('next_event', 'integer', default=0, writable=False, readable=False),
                Field('prev_event', 'integer', default=0),
                Field('recurrence', 'string',
                      requires=IS_IN_SET(['None', 'Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'])),
                Field('locked', 'boolean', readable=False, writable=False),
                format='%(event_name)s')


db.define_table('question',
                Field('qtype', 'string', label='Item Type', requires=IS_IN_SET(['quest', 'action', 'issue'])),
                Field('eventid', 'reference event', label='Event'),
                Field('questiontext', 'text', label='Item Details', requires=not_empty),
                Field('status', 'string', default='In Progress',
                      requires=IS_IN_SET(['Draft', 'In Progress', 'Resolved', 'Rejected'])),
                Field('resolvemethod', 'reference resolve', label='Resolution Method', notnull=True,
                      comment='Single allows one person to resolve others need consensus'),
                Field('auth_userid', 'reference auth_user', readable=False, writable=False,
                      label='Submitter'),
                Field('factopinion', 'string', default='Opinion', requires=IS_IN_SET(['Fact', 'Opinion']),
                      label='Fact/Opinion',
                      comment='Fact answered by submitter or knowledge engines,opinion requires options'),
                Field('answertext', 'text', label='Fact Answer'),
                Field('answer1', 'string'),
                Field('answer2', 'string'),
                Field('numanswer1', 'integer', default=0, readable=False, writable=False),
                Field('numanswer2', 'integer', default=0, readable=False, writable=False),
                Field('urgency', 'decimal(6,2)', default=5, readable=False, writable=False),
                Field('importance', 'decimal(6,2)', default=5, readable=False, writable=False),
                Field('totratings', 'integer', default=0, readable=False, writable=False),
                Field('numlike', 'integer', default=0, readable=False, writable=False),
                Field('priority', compute=lambda r: r['urgency'] * r['importance'],
                      readable=False, writeable=False),
                Field('createdate', 'datetime', readable=False, writable=False, default=datetime.datetime.now),
                Field('resolvedate', 'datetime', readable=False, writable=False),
                Field('responsible', label='Responsible'),
                Field('chosenai', 'reference knowledge', label='AI/Knowledge Engine'),
                Field('correctans', 'integer', label='Correct Answer', requires=IS_EMPTY_OR(IS_IN_SET([1, 2])),
                      comment='If populated status moves to resolved'),
                Field.Virtual('correctanstext', lambda row: (row['factopinion'] == 'Fact' and 'N/A')
                            or (row['correctans'] == 1 and row['answer1'])
                            or (row['correctans'] == 2 and row['answer2']) or '?'),
                Field('aianswer', 'text', label='Answer from AI/Knowledge Engine Lookup'),
                Field('notes', 'text', label='Notes'),
                Field('startdate', 'datetime', readable=False, writable=False, default=datetime.datetime.now),
                Field('enddate', 'datetime', readable=False, writable=False, default=datetime.datetime.now),
                Field('shared_editing', 'boolean', default=False, label='Shared Edit', comment='Allow anyone to edit'),
                Field('xpos', 'double', default=0.0, label='xcoord'),
                Field('ypos', 'double', default=0.0, label='ycoord'),
                Field('social_media', 'boolean', label='Post to Twitter'),
                Field('media_id', 'integer', readable=False, writable=False),
                Field('perccomplete', 'integer', default=0, label='Percent Complete',
                      requires=IS_INT_IN_RANGE(0, 101, error_message='Must be between 0 and 100')),
                Field('question_media', 'upload', label='Upload video or other supporting content (optional)',
                      uploadfolder=settings.UPLOAD_FOLDER, comment='mp4, mp3 and jpeg are currently supported'),
                Field('question_url', 'string', label='Link To Supporting Content',
                      comment='This will load in an iframe for users to review - content not copied'),
                Field('execstatus', 'string', label='Execution Status', default='Proposed',
                      requires=IS_IN_SET(['Proposed', 'Planned', 'In Progress', 'Completed'])))
db.question.question_url.requires = IS_EMPTY_OR(IS_URL())


db.define_table('tweets',
                Field('parentid', 'integer'),
                Field('parenttable', 'string', default='question', writable=False, readable=False),
                Field('tweet_text', 'text', requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='To Send', requires=IS_IN_SET(['To Send', 'Sent', 'Rejected'])),
                Field('requestdate', 'datetime', default=datetime.datetime.now, writable=False),
                Field('tweetdate', 'datetime', writable=False),
                Field('media_id', 'integer'),  # Note this is the twitter url that we get on the status post
                )


db.define_table('userquestion',
                Field('questionid', db.question, writable=False, notnull=True),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, notnull=True),
                Field('answer', 'integer', default=0, label='My Answer'),
                Field('reject', 'boolean', default=False),
                Field('answerreason', 'text', label='Reasoning'),
                Field('ansdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False))


db.define_table('uqrating',
                Field('questionid', db.question, writable=False, notnull=True),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False, notnull=True),
                Field('urgency', 'integer', default=5,
                      requires=IS_INT_IN_RANGE(1, 11, error_message='Must be between 1 and 10')),
                Field('importance', 'integer', default=5,
                      requires=IS_INT_IN_RANGE(1, 11, error_message='Must be between 1 and 10')),
                Field('ratingdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False))


db.define_table('questlink',
                Field('sourceid', 'reference question'),
                Field('targetid', 'reference question'),
                Field('linktype', 'string', default='Std', requires=IS_IN_SET(['Std', 'Conflict'])),
                Field('createdby', 'reference auth_user'),
                Field('createcount', 'integer', default=1),
                Field('deletecount', 'integer', default=0),
                Field('status', 'string', default='Active', requires=IS_IN_SET(['Draft', 'Active', 'Rejected'])),
                Field('lastdeleter', 'reference auth_user'),
                Field('lastaction', 'string', default='create'),
                Field('createdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False))


db.define_table('comment',
                Field('parentid', 'integer', writable=False, readable=False),
                Field('parenttable', 'string', default='question', writable=False, readable=False),
                Field('auth_userid', 'reference auth_user', writable=False, readable=False),
                Field('comment', 'text', requires=IS_NOT_EMPTY()),
                Field('status', 'string', default='OK', writable=False, readable=False,
                      requires=IS_IN_SET(['OK', 'NOK'])),
                Field('numreject', 'integer', default=0, writable=False, readable=False),
                Field('usersreject', 'list:integer', writable=False, readable=False),
                Field('commentdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False))
db.comment.parenttable.requires = IS_IN_SET(['question', 'project', 'event'])


db.define_table('eventmap',
                Field('eventid', 'reference event', notnull=True),
                Field('questid', 'reference question', notnull=True),
                Field('xpos', 'double', default=0.0, label='xcoord'),
                Field('ypos', 'double', default=0.0, label='ycoord'),
                Field('qtype', 'string', writable=False, requires=IS_IN_SET(['quest', 'action', 'issue'])),
                Field('status', 'string', default='In Progress', requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('factopinion', 'string', default='Opinion', requires=IS_IN_SET(['Fact', 'Opinion']),
                      label='Fact or Opinion',
                      comment='Factual questions should be answered by either submitter or knowledge engines'),
                Field('questiontext', 'text', writable=False, label='Question'),
                Field('answertext', 'text', label='Fact Answer'),
                Field('answer1', 'string', writable=False),
                Field('answer2', 'string', writable=False),
                Field('correctans', 'integer', readable=False, writable=False, label='Correct Ans'),
                Field('urgency', 'decimal(6,2)', default=5, writable=False, label='Urgency'),
                Field('importance', 'decimal(6,2)', default=5, writable=False, label='Importance'),
                Field('priority', 'decimal(6,2)', compute=lambda r: r['urgency'] * r['importance'],
                      readable=False, writable=False, label='Priority'),
                Field('numlike', 'integer', default=0, readable=False, writable=False),
                Field('auth_userid', 'reference auth_user', writable=False, label='Submitter'),
                Field('adminresolve', 'boolean', default=False,
                      label='True if answer or status adjusted by event owner'),
                Field('startdate', 'datetime', readable=False, writable=False, default=datetime.datetime.now),
                Field('enddate', 'datetime', readable=False, writable=False, default=datetime.datetime.now),
                Field('responsible', label='Responsible'),
                Field('chosenai', 'reference knowledge', label='AI/Knowledge Engine'),
                Field('eventlevel', 'integer', default=0),
                Field('masterquest', 'integer', default=0),
                Field('subquests', 'list:integer'),
                Field('queststatus', 'string', default='In Progress',
                      requires=IS_IN_SET(['Draft', 'In Progress', 'Resolved', 'Rejected', 'Admin Resolved']),
                      comment='Select draft to defer for later editing'),
                Field('perccomplete', 'integer', default=0, label='Percent Complete',
                      requires=IS_INT_IN_RANGE(0, 101, error_message='Must be between 0 and 100')),
                Field('execstatus', 'string', label='Execution Status', default='Proposed',
                      requires=IS_IN_SET(['Proposed', 'Planned', 'In Progress', 'Completed'])),
                Field('aianswer', 'text', label='Answer from AI/Knowledge Engine Lookup'),
                Field('notes', 'text', label='Notes'))
db.eventmap.correctanstext = Field.Virtual(lambda row: ((row.eventmap.correctans == 1 and row.eventmap.answer1) or
                                                        (row.eventmap.correctans == 2 and row.eventmap.answer2) or ''))

db.define_table("itemlike",
                Field('parentid', 'integer'),
                Field('parenttable', 'string', default='question'),
                Field('createdby', 'reference auth_user'),
                Field('liketype', 'string', default='like'),
                Field('likedate', 'datetime', default=datetime.datetime.now))


db.define_table('email_runs',
                Field('datecreate', 'datetime', default=datetime.datetime.now, writable=False),
                Field('daterun', 'datetime', writable=False),
                Field('runperiod', 'string', requires=IS_IN_SET(['Day', 'Week', 'Month'])),
                Field('datefrom', 'datetime'),
                Field('dateto', 'datetime'),
                Field('status', 'string', requires=IS_IN_SET(['Planned', 'Completed', 'Failed'])),
                Field('error', 'text'))


db.define_table('prompt',
                Field('chosenai', 'reference knowledge', label='AI/Knowledge Engine'),
                Field('scenario', 'string',
                      requires=IS_IN_SET(['answer', 'gen_actions', 'gen_questions', 'gen_issues',
                                          'rev_actions', 'rev_issues', 'rev_questions'])),
                Field('setup', 'string', default='A', label='Current prompt setup'),
                Field('prompttype', 'string', requires=IS_IN_SET(['system', 'user'])),
                Field('sequence', 'integer', comment='Use numbers above 50 if you want to come after item'),
                Field('status', 'string', default='Active', requires=IS_IN_SET(['Active', 'Inactive'])),
                Field('prompt_text', 'text', requires=IS_NOT_EMPTY()))


db.define_table('ai_review',
                Field('parentid', 'integer', writable=False, readable=False),
                Field('parenttable', 'string', default='question', writable=False, readable=False),
                Field('chosenai', 'string', label='AI/Knowledge Engine'),
                Field('ai_version', 'string', label='AI Version'),
                Field('scenario', 'string', default='Review'),
                Field('setup', 'string', default='A', label='Current prompt setup'),
                Field('status', 'string', default='Active', requires=IS_IN_SET(['Active', 'Inactive'])),
                Field('review', 'text', requires=IS_NOT_EMPTY()),
                Field('reviewdate', 'datetime', default=datetime.datetime.now, writable=False, readable=False))

# This will be system level defaults for generating new items
# may well make this configurable at event level later but lets see how it works first and stabilize
# setup
db.define_table('ai_item_generation',
                Field('maxitems', 'integer', default=20, label='Max Items'),
                Field('chosenai', 'string', label='AI/Knowledge Engine'),
                Field('ai_version', 'string', label='AI Version'),
                Field('numissues', 'integer', default=0, label='Number of Issues'),
                Field('numquestions', 'integer', default=1, label='Number of Questions'),
                Field('numactions', 'integer', default=1, label='Number of Actions'),
                Field('probissues', 'decimal(6,2)', default=0, label='%age probability of generating Issues'),
                Field('probquestions', 'decimal(6,2)', default=100, label='%age probability of generating Questions'),
                Field('probactions', 'decimal(6,2)', default=100, label='%age probablity of generating Actions'))

db.ai_item_generation.probissues.requires = IS_DECIMAL_IN_RANGE(0,100,'Must be between 0 and 100')
db.ai_item_generation.probquestions.requires = IS_DECIMAL_IN_RANGE(0,100,'Must be between 0 and 100')
db.ai_item_generation.probactions.requires = IS_DECIMAL_IN_RANGE(0,100,'Must be between 0 and 100')

db.commit()
