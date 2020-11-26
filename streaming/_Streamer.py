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
        keep_going = True
        listener = Listener(twitter_db, topic, listener_limit)

        while(keep_going):
            try:
                keep_going = False
                stream = Stream(self.authenticator.authenticate(), listener)
                stream.filter(track=sf["track"], is_async=sf["is_async"])
            except Exception as e:
                print("Error on streamer: \n" + str(e) + "\n" + "try to resume..")
                resume_limit  = listener.get_remaining()
                listener = Listener(twitter_db, topic, resume_limit)
                keep_going = True