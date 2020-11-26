import io
import json
import sys
import os
import re
import concurrent.futures
from streaming import tweet_preprocess as TWP
from threading import Thread
from textblob import TextBlob
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

class Handler_v2():
    """
    Classe che maneggia i tweet ricevuti dal listener.
    1. Il dato arriva in coda (pr_queue)
    2. Appena uno è accodato si fa preprocessing in multi-threading, per tutta la coda
    3. Il risultato di ogni singolo preprocess è accodato (st_queue)
    4. Appena uno risultato è accodato parte lo store, che prosegue sulla coda
    """
    def __init__(self, twitter_db, topic, limit):
        self.twitter_db = twitter_db
        self.topic = topic
        self.limit = limit
        self.pr_queue = []
        self.st_queue = []
        self.is_processing = False
        self.is_storing = False

    def pr_enqueue(self, t):
        if self.limit > 0:
            self.pr_queue.append(t)
            return True
        else:
            return False

    def pr_dequeue(self):
        if len(self.pr_queue) > 0:
            return self.pr_queue.pop(0)
        else:
            self.is_processing = False
            return False

    def st_enqueue(self, d):
        try:
            self.st_queue.append(d)
            return True
        except Exception as e:
            print("Error on enqueue for storing \n" + str(e))
            return False

    def st_dequeue(self):
        if len(self.st_queue) > 0:
            return self.st_queue.pop(0)
        else:
            self.is_storing = False
            return False

    def call_preprocess(self):
        if not self.is_processing:
            self.is_processing = True
            tweet = self.pr_dequeue()
            while (tweet):
                try:
                    Thread(target=self.preprocess_one(tweet)).start()
                    tweet = self.pr_dequeue()
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(str(e))
                    return
            self.is_processing = False
            return

    def preprocess_one(self, tweet):
        out = TWP.start_preprocess(tweet)
        self.st_enqueue(out)
        self.call_store()

    def call_store(self):
        if not self.is_storing:
            self.is_storing = True
            analysis_res = self.st_dequeue()
            while (analysis_res):
                try:
                    print("+1 " + self.topic)
                    self.twitter_db.store_tweet(self.topic, analysis_res)
                    self.limit -= 1
                    self.write_files(analysis_res["tweet"])
                    analysis_res = self.st_dequeue()
                except Exception as e:
                    print("error on call db.store \n" +str(e))
            self.is_storing = False
            return

#------------------------------------------------------------------------------#

    def show(self,tweet):
        try:
            print('----------------------------\n')
            print("- " + self.topic + " topic" + '\n')
            #print(tweet["text"] +'\n')
            return
        except Exception as e:
            print("error on show tweet text: \n" + str(e))
            return

    def write_files(self, tweet):
        try:
            with io.open(self.topic+".json", 'a', encoding="utf-8") as tf:
                json.dump(tweet, tf)
                tf.write('\n\n')
            with io.open(self.topic+"_geo.txt", 'a', encoding="utf-8") as gf:
                gf.write(str(tweet["user"]["location"]))
                gf.write('\n')
            return
        except Exception as e:
            return
