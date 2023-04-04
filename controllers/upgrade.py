import datetime
from ..common import db, authenticated, auth

# this will refactor question for the following changes
# Remove AI_Opinion question type
# Add question to knowledge engine none
# Need to think about what other changes

@authenticated()
def fixquestions():
    '''This will remove the (EU) etc from all existing continents, countries and subdivisions and once done should be fine to just run the new add countries and add continents  - will do continents first and then countries and then subdivisions'''

    continents = db(db.continent.id > 0).select()
    count_conts = 0
    for continent in continents:
        if continent.continent_name[-1] == ')':
            continent.continent_name = continent.continent_name[:-5]
            continent.update_record()
            count_conts += 1


    return dict(count_conts=count_conts, count_countries=count_countries,
                count_subs=count_subs, count_countrycont=count_countrycont, count_subcountry=count_subcountry,
                message='Suffixes removed from geog setup')