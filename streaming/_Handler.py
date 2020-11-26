# import io
# import json
# import sys
# import re
# from streaming import avaliable_countries as AV_COUNTRIES
# from threading import Thread
# from textblob import TextBlob
# from geopy.geocoders import Nominatim
# from geopy.distance import great_circle

# class Handler():
#     """
#     Classe che maneggia i tweet ricevuti dal listener.
#     Arrivano in una coda, idea è multiprocessing.
#     """
#     def __init__(self, twitter_db, topic, limit):
#         self.twitter_db = twitter_db
#         self.topic = topic
#         self.limit = limit
#         self.queue = []
#         self.is_processing = False
#         self.geolocator = Nominatim(user_agent="sacro_quore") # evidentemente va bene qualsiasi minchiata come user_agent tranne "specify_your_app_name_here"

#     def enqueue(self, t):
#         if self.limit > 0:
#             self.queue.append(t)
#             return True
#         else:
#             return False

#     def dequeue(self):
#         if len(self.queue) > 0:
#             return self.queue.pop(0)
#         else:
#             self.is_processing = False
#             return False

#     def handle(self):
#         if not self.is_processing:
#             self.is_processing = True
#             tweet = self.dequeue()
#             while (tweet):
#                 try:
#                     Thread(target=self.analyze(tweet)).start()
#                     tweet = self.dequeue()
#                 except Exception as e:
#                     print("error on threading tweet \n" + str(e))
#                     return
#             self.is_processing = False
#             return

#     def show(self,tweet):
#         try:
#             print('----------------------------\n')
#             print("- " + self.topic + " topic" + '\n')
#             #print(tweet["text"] +'\n')
#             return
#         except Exception as e:
#             print("error on show tweet text: \n" + str(e))
#             return

#     def write_files(self, tweet):
#         try:
#             with io.open(self.topic+".txt", 'a', encoding="utf-8") as tf:
#                 tf.write(str(tweet))
#                 tf.write('\n')
#             with io.open(self.topic+"_geo.txt", 'a', encoding="utf-8") as gf:
#                 gf.write(str(tweet["user"]["location"]))
#                 gf.write('\n')
#             return
#         except Exception as e:
#             return

#     def localize(self, user_location):
#         user_geo_location = self.geolocator.geocode(user_location, addressdetails=True, language='en')
#         if user_geo_location:
#             user_country = self.correct_synonyms(user_geo_location.raw["address"]["country"])
#             if user_country in AV_COUNTRIES.countries:
#                 location = self.nearest((user_geo_location.latitude, user_geo_location.longitude), AV_COUNTRIES.countries[user_country])
#                 return {"country": user_country, "city": location}
#             else:
#                 print("// DISCARDED LOCATION: user-> " + user_location + ", " + user_country + " not found in avaliable_countries.py")
#                 return
#         else:
#             return

#     def nearest(self, user_coor, cities):
#         distances = {}
#         for i,city in enumerate(cities):
#             city_coor = (city["coor"]["lat"], city["coor"]["long"])
#             distances[str(i)] = great_circle(user_coor, city_coor)
#         return cities[int(min(distances, key=distances.get))]

#     def analyze(self, tweet):
#         try:
#             self.show(tweet)
#             if tweet["user"]["location"]:
#                 try:
#                     location = self.localize(tweet["user"]["location"])
#                     if location:
#                         self.limit -= 1
#                         self.twitter_db.store_tweet(self.topic, tweet, location)
#                         return
#                     else:
#                         return
#                 except Exception as e:
#                     print("error while localizing tweet: \n" + str(e) + "\n\n" + "tweet error: \n" + str(tweet) + "\n")
#                     return
#         except Exception as e:
#             print("User filed not found")

#     def correct_synonyms(self, country_name):
#         if (country_name=="United States"): # Da notare che se geolocalizzo come United States allora è perchè user:location è "USA" o simili -> verrà scelta come città Denver in colorado perchè è in centro agli stati uniti
#             return "United States of America"
#         else:
#             return country_name

#     def analyze_sentiment(self, tweet_text):
#         try:
#             analysis = TextBlob(self.clean_tweet(tweet_text))
#             if analysis.sentiment.polarity > 0:
#                 return {"polarity": analysis.sentiment.polarity, "sentiment": "positive"}
#             elif analysis.sentiment.polarity == 0:
#                 return {"polarity": analysis.sentiment.polarity, "sentiment": "neutral"}
#             else:
#                 return {"polarity": analysis.sentiment.polarity, "sentiment": "negative"}
#         except Exception as e:
#             print("\n" + "Fail in sentiment analysis \n" + str(e) +"\n")
#             return False

#     def clean_tweet_text(self, tweet_text):
#             return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet_text).split())
