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
# Will revert to extra depth later