# File for new functions to support the following
#  1 AI Generation of issues, questions and actions
#  2 AI answering of questions
#  3 AI full review of events
# For now most of these will operated at an event level and there
# should be fairly common approach along the following lines
#
# 1 Get all the items in an event
# 2 Go through one by one starting from the earliest creation date
# 3 Either generate, answer or comment on the itme
# 4 Navigate to the next item (probably in the original list for now
# Will revert to extra depth later - actually now thinking we only ever do 1 layer and just re-run and
# that will automatically generate another layer.  Also maybe %age and probabilistic creation may be the way to go
# this will use the new job scheduler I anticipate and create in the background with logging - so think the traversal
# is simple and we do first
# when we come to contacting the AI for an item we probably want to see if we can combine with the interactive way
# but these are currently only suggestions and have not been structured into questions, actions and issues - probably
# fine to do that just need to fiddle about a bit with questions

from ndsqueries import get_items

def add_item(parent, questiontext, answer1, answer2):
    """This will actually create the item required.  Let's say it can either be supplied with
    the details or it will go get them as we may want a more general add_item capability eg to call
    interactively from viewquest suggestions"""
    
    
    
def review_item(item):
    """This should take an item and identify the current number of links and would then use the parameters
    for whether or not to create new linked items to decide to create new items.  If a new item is
    required we will call add_item """
    print(item)
    
    quesiontext='Test Question'
    answer1='Yes'
    answer2='No'
    add_item(item.id, questiontext, answer1, answer2)
    return

def get_event_items(eid)
    eventrow = db(db.event.id == eid).select().first()
    items = get_items(qtype='all', status='all', event=eid, eventstatus=eventrow.status)
    visited = {}
    for item in items:
        review_item(item)

