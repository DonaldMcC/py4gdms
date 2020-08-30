"""
This file defines the database models
"""

from .common import db
from py4web import Field
from pydal.validators import *
import datetime

not_empty = IS_NOT_EMPTY()

# Define your table below
#
# db.define_table('thing', Field('name'))
#
# always commit your models to avoid problems later
#
# db.commit()
#

# TODO setup auth again

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
                      label='Owner'),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                format='%(proj_name)s')

# Field('auth_userid', 'reference auth_user', writable=False, readable=False, default=auth.user_id),

db.define_table('locn',
                Field('location_name', label='Location Name', requires=[not_empty,
                                                                        IS_NOT_IN_DB(db, 'locn.location_name')]),
                Field('address1', label='Address 1', writable=False, readable=False),
                Field('address2', label='Address 2', writable=False, readable=False),
                Field('address3', label='Address 3', writable=False, readable=False),
                Field('address4', label='Address 4', writable=False, readable=False),
                Field('addrcode', label='Postal Code', writable=False, readable=False),
                Field('addrurl', label='Location Website'),
                Field('continent', default='Unspecified', label='Continent'),
                Field('country', default='Unspecified', label='Country'),
                Field('subdivision', default='Unspecified', label='Subdivision'),
                Field('coord', label='Lat/Longitude'),  # ignore values in this field
                Field('locn_long', 'double', default=0.0, label='Latitude', writable=False, readable=False),
                Field('locn_lat', 'double', default=0.0, label='Longitude', writable=False, readable=False),
                Field('description', 'text'),
                Field('locn_shared', 'boolean', label='Shared', default=True,
                      comment='Allows other users to link events'),
                Field('createdate', 'datetime',  default=datetime.datetime.utcnow(), writable=False, readable=False),
                format='%(location_name)s')

# Field('evt_owner', 'reference auth_user', writable=False, readable=False, default=auth.user_id,
#                      label='Owner'),

db.define_table('evt',
                Field('evt_name', label='Event Name'),
                Field('locationid', 'reference locn', label='Location'),
                Field('projid', 'reference project', label='Project'),
                Field('eventurl', label='Event Website'),
                Field('status', 'string', default='Open',
                      requires=IS_IN_SET(['Open', 'Archiving', 'Archived'])),
                Field('answer_group', 'string', default='Unspecified', label='Restrict Event to Group'),
                Field('startdatetime', 'datetime', label='Start Date Time',
                      default=(datetime.datetime.utcnow() + datetime.timedelta(days=10))),
                Field('enddatetime', 'datetime', label='End Date Time',
                      default=(datetime.datetime.utcnow() + datetime.timedelta(days=11))),
                Field('description', 'text'),
                Field('evt_shared', 'boolean', default=True, label='Shared Event',
                      comment='Allows other users to link questions'),
                Field('createdate', 'datetime', default=datetime.datetime.utcnow(), writable=False, readable=False),
                Field('next_evt', 'integer', default=0, label='Next Event'),
                Field('prev_evt', 'integer', default=0, label='Previous Event'),
                Field('recurrence', 'string', default='None',
                      requires=IS_IN_SET(['None', 'Daily', 'Weekly', 'Bi-weekly', 'Monthly', 'Quarterly'])),
                format='%(evt_name)s')

db.evt.eventurl.requires = IS_EMPTY_OR(IS_URL())
db.evt.startdatetime.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                                                     minimum=datetime.datetime(2014, 6, 15, 00, 00),
                                                     maximum=datetime.datetime(2021, 12, 31, 23, 59),
                                                     error_message='must be YYYY-MM-DD HH:MM::SS!')
db.evt.enddatetime.requires = IS_DATETIME_IN_RANGE(format=T('%Y-%m-%d %H:%M:%S'),
                                                   minimum=datetime.datetime(2014, 6, 15, 00, 00),
                                                   maximum=datetime.datetime(2021, 12, 31, 23, 59),
                                                   error_message='must be YYYY-MM-DD HH:MM::SS!')

db.evt.evt_name.requires = [not_empty, IS_NOT_IN_DB(db, 'evt.evt_name')]

db.commit()
