import praw
from .reddit import Reddit
import os
from dotenv import load_dotenv
from praw.models import MoreComments
from core_system.utils.voice import sanitize_text

load_dotenv()



def getRedditClientInstance() -> Reddit:
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent="Accessing Reddit threads",
        username=os.environ["REDDIT_USERNAME"],
        passkey=os.environ["REDDIT_PASSWORD"],
    )
    return Reddit(redditClient=reddit,sanitize_text=sanitize_text,MoreCommentsINSTANCE=MoreComments) 