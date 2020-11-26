import io
import json
#from ._Handler import * #v2
from streaming._Handler_v2 import * #v2
from tweepy import StreamListener

class Listener(StreamListener):
    """
    Estende StreamListener di tweepy
    Classe per armeggiare con i tweet raccolti dallo Streamer
    """
    def __init__(self, twitter_db, topic, limit):
        self.count = 0
        self.limit = limit
        self.topic = topic
        #self.handler = Handler(twitter_db, topic, limit) #v2
        self.handler = Handler_v2(twitter_db, topic, limit) #v2

    def on_data(self, data):
        try:
            self.count += 1
            # go_on = self.handler.enqueue(json.loads(data)) #v2
            go_on = self.handler.pr_enqueue(json.loads(data)) #v2
            if go_on:
                #self.handler.handle() #v2
                self.handler.call_preprocess()
            else:
                print('\n' + "///// Tweet of " + self.topic + " topic limit reached... stopping now." + '\n')
                print('\n' + "only " + str(self.limit) + " tweets out of " + str(self.count) + " had user:location field" + '\n')
                return False
        except Exception as e:
            print("Listener error on on_data function: ", str(e))
            return False
        return True

    def on_error(self, status):
        if (status == 420):  # API conneting attemps reached, ci si ferma.
            return False
        print(status)

#------------------------------------------------------------------------------#

    # QUA SI ARMEGGIA - si ma non serve più niente
    # def handle(self, tweet):
    #     kw = self.getKeyword(tweet)
    #     print("got 1 from " + kw)
    #     try:
    #         with io.open(kw+".txt", 'a', encoding="utf-8") as f:
    #             f.write(str(tweet))
    #             f.write('\n')
    #     except Exception as e:
    #         print("Listener error on handle function: ", str(e))
    #         return False
    #     return True
    #
    #
    # def getKeyword(self, tweet):
    #     for kw in self.filters["track"]:
    #         try:
    #             if kw in tweet["text"].lower():
    #                 return kw
    #             elif "retweeted_status" in tweet:
    #                 if "extended_tweet" in tweet["retweeted_status"]:
    #                     if kw in tweet["retweeted_status"]["extended_tweet"]["full_text"].lower():
    #                         return kw
    #             elif "extended_tweet" in tweet:
    #                 if kw in tweet["extended_tweet"]["full_text"].lower():
    #                     return kw
    #         except Exception as e:
    #             print("Error on getKW: ", str(e), '\n', str(tweet))
    #     return "_missed" # non si è capito perchè è arrivato
