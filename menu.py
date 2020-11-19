# -*- coding: utf-8 -*-
# - Coding UTF8 -
#
# Networked Decision Making
# Development Sites (source code): http://github.com/DonaldMcC/gdms
#
# Demo Sites (Pythonanywhere)
#   http://netdecisionmaking.com/nds/
#   http://netdecisionmaking.com/gdmsdemo/
#
# License Code: MIT
# License Content: Creative Commons Attribution 3.0
#
# Also visit: www.web2py.com
# or Groups: http://groups.google.com/group/web2py
# For details on the web framework used for this development
#
# With thanks to Guido, Massimo and many other that make this sort of thing
# much easier than it used to be

from py4web import response, URL

sub_menu = [('Create Location', False, URL('location', 'new_location')),
            ('Create Project', False, URL('project', 'new_project')),
            ('Create Event', False, URL('event', 'new_event')),
            ('Create Group', False, URL('accessgroups', 'new_group')),
            ('Create Issue', False, URL('submit', 'new_question/issue')),
            ('Create Question', False, URL('submit', 'new_question/quest')),
            ('Self Ans Question', False, URL('submit', 'new_question/selfquest')),
            ('Create Action', False, URL('submit', 'new_question/action'))]

response.menu = [
    ('About', False, '#',
     [('Home', False, URL('default', 'index')),
      ('Search', False, URL('search', 'newsearch')),
      ('About NDS', False, URL('about', 'index')),
      ('FAQ', False, URL('about', 'faq')),
      ('Presentation', False, URL('about', 'present')),
      ('Enhancements', False, URL('about', 'enhance')),
      ('Privacy Policy', False, URL('about', 'privacy')),
      ('Downloads', False, URL('about', 'download'))]),
      ('Create', False, '#',
       sub_menu),
      ('Answer', False, '#',
     [('Approve Issues', False, URL('answer', 'get_question/issue')),
      ('Answer Questions', False, URL('answer', 'get_question/quest')),
      ('Approve Actions', False, URL('answer', 'get_question/action'))]),
      ('Review', False, '#',
     [('Locations', False, URL('location', 'index')),
      ('Projects', False, URL('project', 'index')),
      ('Events', False, URL('event', 'index')),
      ('Groups', False, URL('accessgroups', 'index')),
      ('Activity', False, URL('review', 'newindex'))]),
      ('Plan', False, '#',
     [('Actions', False, URL('review', 'newindex')),
      ('Gantt', False, URL('gantt', 'index')),
      ('Recur', False, URL('review', 'newindex'))]),
      ('My NDS', False, '#',
     [('My Issues', False, URL('review', 'newindex')),
      ('My Questions', False, URL('review', 'newindex')),
      ('My Draft Items', False, URL('review', 'newindex')),
      ('My Actions', False, URL('review', 'newindex')),
      ('My Answers', False, URL('review', 'my_answers')),
      ('My Locations', False, URL('location', 'my_locations')),
      ('My Events', False, URL('event', 'my_events')),
      ('My Projects', False, URL('project', 'my_projects'))]),
]


#if auth.has_membership('manager'):
#    response.menu += [
#        (T('Admin'), False, '#', [(T('Admin'), False, URL('admin', 'index')),
#                                  (T('Upgrade'), False, URL('upgrade', 'index')),
#                                  ('Appadmin', False, URL('appadmin', 'manage', args=['auth']))])]
