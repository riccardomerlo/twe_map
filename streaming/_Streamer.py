from tweepy import Stream

from ._Auth import *
from ._Listener import *

class Streamer():
    """
    Classe per avviare lo streaming
    """
    def __init__(self):
        self.authenticator = Auth()

    def stream(self, twitter_db, sf, topic, listener_limit=10):
        listener = Listener(twitter_db, topic, listener_limit)
        stream = Stream(self.authenticator.authenticate(), listener)
        stream.filter(track=sf["track"], is_async=sf["is_async"])
