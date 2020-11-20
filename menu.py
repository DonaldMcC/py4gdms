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
from yatl.helpers import DIV, LI, UL, A, SELECT, CAT

#Below for reference
class MENU():
    """
    Used to build menus
    Args:
        _class: defaults to 'web2py-menu web2py-menu-vertical'
        ul_class: defaults to 'web2py-menu-vertical'
        li_class: defaults to 'web2py-menu-expand'
        li_first: defaults to 'web2py-menu-first'
        li_last: defaults to 'web2py-menu-last'
    Use like::
        menu = MENU([['name', False, URL(...), [submenu]], ...])
        {{=menu}}
    """

    tag = 'ul'

    def __init__(self, data, **args):
        self.data = data
        self.attributes = args
        self.components = []
        if '_class' not in self.attributes:
            self['_class'] = 'web2py-menu web2py-menu-vertical'
        if 'ul_class' not in self.attributes:
            self['ul_class'] = 'web2py-menu-vertical'
        if 'li_class' not in self.attributes:
            self['li_class'] = 'web2py-menu-expand'
        if 'li_first' not in self.attributes:
            self['li_first'] = 'web2py-menu-first'
        if 'li_last' not in self.attributes:
            self['li_last'] = 'web2py-menu-last'
        if 'li_active' not in self.attributes:
            self['li_active'] = 'web2py-menu-active'
        if 'mobile' not in self.attributes:
            self['mobile'] = False

    def serialize(self, data, level=0):
        if level == 0:
            ul = UL(**self.attributes)
        else:
            ul = UL(_class=self['ul_class'])
        for item in data:
            if isinstance(item, LI):
                ul.append(item)
            else:
                (name, active, link) = item[:3]
                if isinstance(link, DIV):
                    li = LI(link)
                elif 'no_link_url' in self.attributes and self['no_link_url'] == link:
                    li = LI(DIV(name))
                elif isinstance(link, dict):
                    li = LI(A(name, **link))
                elif link:
                    li = LI(A(name, _href=link))
                elif not link and isinstance(name, A):
                    li = LI(name)
                else:
                    li = LI(A(name, _href='#',
                              _onclick='javascript:void(0);return false;'))
                if level == 0 and item == data[0]:
                    li['_class'] = self['li_first']
                elif level == 0 and item == data[-1]:
                    li['_class'] = self['li_last']
                if len(item) > 3 and item[3]:
                    li['_class'] = self['li_class']
                    li.append(self.serialize(item[3], level + 1))
                if active or ('active_url' in self.attributes and self['active_url'] == link):
                    if li['_class']:
                        li['_class'] = li['_class'] + ' ' + self['li_active']
                    else:
                        li['_class'] = self['li_active']
                if len(item) <= 4 or item[4] is True:
                    ul.append(li)
        return ul

    def serialize_mobile(self, data, select=None, prefix=''):
        if not select:
            select = SELECT(**self.attributes)
        custom_items = []
        for item in data:
            # Custom item aren't serialized as mobile
            if len(item) >= 3 and (not item[0]) or (isinstance(item[0], DIV) and not (item[2])):
                # ex: ('', False, A('title', _href=URL(...), _title="title"))
                # ex: (A('title', _href=URL(...), _title="title"), False, None)
                custom_items.append(item)
            elif len(item) <= 4 or item[4] is True:
                select.append(OPTION(CAT(prefix, item[0]),
                                     _value=item[2], _selected=item[1]))
                if len(item) > 3 and len(item[3]):
                    self.serialize_mobile(
                        item[3], select, prefix=CAT(prefix, item[0], '/'))
        select['_onchange'] = 'window.location=this.value'
        # avoid to wrap the select if no custom items are present
        html = DIV(select, self.serialize(custom_items)) if len(custom_items) else select
        return html

    def xml(self):
        if self['mobile']:
            return self.serialize_mobile(self.data, 0).xml()
        else:
            return self.serialize(self.data, 0).xml()



sub_menu = [('Create Location', False, URL('location', 'new_location')),
            ('Create Project', False, URL('project', 'new_project')),
            ('Create Event', False, URL('event', 'new_event')),
            ('Create Group', False, URL('accessgroups', 'new_group')),
            ('Create Issue', False, URL('submit', 'new_question/issue')),
            ('Create Question', False, URL('submit', 'new_question/quest')),
            ('Self Ans Question', False, URL('submit', 'new_question/selfquest')),
            ('Create Action', False, URL('submit', 'new_question/action'))]

appmenu = [
    ('About', False, '#',
     [('Home', False, URL('default', 'index')),
      ('Search', False, URL('search', 'newsearch')),
      ('About NDS', False, URL('about', 'index')),
      ('FAQ', False, URL('about', 'faq')),
      ('Presentation', False, URL('about', 'present')),
      ('Enhancements', False, URL('about', 'enhance')),
      ('Privacy Policy', False, URL('about', 'privacy')),
      ('Downloads', False, URL('about', 'download'))]),
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
