"""
This file defines the database models
"""

from .common import db, Field
from pydal.validators import *
import time, datetime

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#
# widget=bsdatepicker_widget()
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

db.commit()
