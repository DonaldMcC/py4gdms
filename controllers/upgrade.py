import datetime
from py4web import action, request, redirect, URL, Flash
from ..common import db, authenticated, auth, session


# this will refactor question for the following changes
# Remove AI_Opinion question type
# Add question to knowledge engine none
# Need to think about what other changes

@authenticated()
@action('fixquestion', method=['POST', 'GET'])
@action.uses('fixquestion.html', session, db)
def fixquestions():
    # This should do data conversions if required - for AI change were potentially two
    # 1 Remove AI_Opionion - but just did this manually
    # 2 Add knowledge engine of none to questions -

    no_ke = db(db.knowledge.source == 'None').select(db.knowledge.id).first().id

    questions = db(db.question.id > 0).select()
    questcount = 0
    for question in questions:
        if not question['chosenai']:
            question['chosenai'] = no_ke
            question.update_record()
            questcount += 1

    return dict(questcount=questcount, message='Questions Updated')
