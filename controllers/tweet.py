
import datetime
from py4web import action, request, redirect, URL, Flash
from py4web.utils.form import Form, FormStyleBootstrap4
from ..bs4inline import FormStyleBootstrap4inline
from ..common import db, session, auth
from ..grid_helpers import GridActionButton
from py4web.utils.grid import Grid, GridClassStyleBootstrap5, GridClassStyle
from ..libs.datatables import DataTablesField, DataTablesRequest, DataTablesResponse
from pydal.validators import *
from ..twitter_client import publish
from ..ndsfunctions import score_question
from .network import request_link
from pydal.tools.tags import Tags
groups = Tags(db.auth_user, tag_table=db.auth_user_tag_groups)

flash = Flash()


@action('tweeter', method=['GET', 'POST'])
@action.uses('tweets.html', session, db, flash, auth.user)
def tweeter():
    # Aim to get this reasonably working without actually publishing first - so this just puts records into
    # the tweets table now - most likely this will be little used other than for testing but similar to comments
    # table we could allow almost anything to be tweeted in due course
    # post_tweet = False
    form = Form(db.tweets, formstyle=FormStyleBootstrap4inline)
    if form.accepted:
        redirect(URL('tweetgrid'))
    return dict(form=form)


@action('tweetgrid', method=['POST', 'GET'])
@action('tweetgrid/<path:path>', method=['POST', 'GET'])
@action.uses('tweetgrid.html', session, db, flash, auth.user)
def tweetgrid(path=None):
    if not 'manager' in groups.get(auth.get_user()['id']):
        redirect(URL('not_authorized'))
    pre_action_buttons = [
        lambda row: (
            GridActionButton(
                url=URL("tweet"),
                text=f"Tweet {row.tweet_text}",
                icon="fa-redo",
                message=f"Do you want to tweet {row.tweet_text}?",
                append_id=True,
            )
        )
        if row.status == 'To Send'
        else None
    ]
    GRID_DEFAULTS = dict(rows_per_page=15,
                         include_action_button_text=True,
                         search_button_text='Filter',
                         formstyle=FormStyleBootstrap4inline,
                         grid_class_style=GridClassStyleBootstrap5)

    query = db.tweets.id > 0

    fields = [db.tweets.status, db.tweets.tweet_text, db.tweets.requestdate, db.tweets.media_id]
    orderby = [~db.tweets.id]
    search_queries = [['Search by Name', lambda value: db.tweets.id == value]]

    grid = Grid(path,
                query,
                fields=fields,
                headings=['Status', 'Tweet', 'Date', 'Tweet ID'],
                orderby=orderby,
                pre_action_buttons=pre_action_buttons,
                search_queries=search_queries,
                deletable=True,
                **GRID_DEFAULTS)
    return dict(grid=grid)


@action("tweet/<recid>", method=['GET', 'POST'])
@action.uses('tweet.html', session, db, auth.user)
def tweet(recid=0):
    # TODO probably want this to be signed URL to not have open tweet option
    # this might be a scheduled routine but may need some sort of review first - which might be automated
    # with gpt or the like

    # so now we would be looking to:
    # 1 get the record from the tweet and probalby also the corresponding base record as and when table is populated
    #   which it should be automatically but never manually
    # 2 for now tweet the first x characters plus potentially the media stuff from the source table once that is filled
    # 3 get the tweet id returned and always updated and the key criteria to allow tweeting will be that this
    #   field is blank
    #   Having done that we then return to tweet grid - perhaps with flash message or the like

    tweet_rec = db(db.tweets.id == recid).select().first()
    redirect(URL('tweetgrid')) if not tweet_rec else print(tweet_rec)
    parent_rec = None

    if tweet_rec['parenttable'] and tweet_rec['parentid']:
        if tweet_rec['parenttable'] == 'question':
            parent_rec = db(db.question.id == tweet_rec['parentid']).select().first()
    if parent_rec:
        tweeturl = URL('viewquest', str(tweet_rec['parentid']), scheme='https')
    else:
        tweeturl = URL('index', scheme='https')

    print(tweeturl)
    # TODO this will go in try except presently - but not sure what errors are likely yet
    pub_result = publish('{} {}'.format(tweeturl, tweet_rec.tweet_text))
    print(pub_result)
    #  So think we come back to this bit in a bit
    #        quest = db(db.tweeter.id == form.vars['id']).select().first()
    #        #TODO revisit below for v2 of APIeventgrid.htmleventgrid.html
    tweet_rec.media_id = pub_result.data['id']
    tweet_rec.status = 'Sent'
    tweet_rec.tweet_date = datetime.datetime.utcnow()
    # So these will end up as https://twitter.com/newglobalstrat/status/1703326031413641356
    # ie always a prefix of status and then the media ID
    tweet_rec.update_record()

    if parent_rec:
        parent_rec.media_id = pub_result.data['id']
        parent_rec.update_record()
    db.commit()
    redirect(URL('tweetgrid'))
    return
