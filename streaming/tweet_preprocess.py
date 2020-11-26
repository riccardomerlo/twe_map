"""
Serie di funzioni dedicaate all'intero preprocess di un tweet:

Step 1: Localizzazione
Step 2: Sentiment analysis
"""

import re
from . import avaliable_countries as AVC
from textblob import TextBlob
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from googletrans import Translator

#------------------------------------------------------------------------------#

"""
Variabili globali script
"""

GEO = Nominatim(user_agent="pippo_al_mc")
TRANS = Translator()

#------------------------------------------------------------------------------#

"""
Preprocessing main
Lancia i diversi tipi di analisi → geoloc, sentiment, ....
"""

def start_preprocess(tweet):

    out = {
            "tweet": tweet,
            # "text": eng_translation(full_tweet_text(tweet)), # alcuni non vanno da studiare
            # "text": tweet["text"], # usate questo se gli errori translate sono troppi o non li volete (però niente sentiment se non in ing)
            "text": eng_translation(tweet["text"]),
            "location": None,
            "sentiment": None
          }

    if tweet["user"]["location"]:
        location = localize(tweet["user"]["location"])
        if location:
            out["location"] = location
            if tweet["text"]:
                sentiment = analyze_sentiment(out["text"])
                if sentiment:
                    out["sentiment"] = sentiment
            return out
        else:
            return False
    else:
        return False


#------------------------------------------------------------------------------#

"""
Geolocalizzazione tramite campo user:location
"""

def localize(user_location):
    try:
        user_geo_location = GEO.geocode(user_location, addressdetails=True, language='en')
        if user_geo_location:
            user_country = correct_synonyms(user_geo_location.raw["address"]["country"])
            if user_country in AVC.countries:
                location = nearest((user_geo_location.latitude, user_geo_location.longitude), AVC.countries[user_country])
                return {"country": user_country, "city": location}
            else:
                print("// DISCARDED LOCATION: user-> " + user_location + ", " + user_country + " not found in avaliable_countries.py")
                return False
        else:
            return False
    except Exception as e:
        print("error in localize -> " + str(e))
        return False

def nearest(user_coor, cities):
    distances = {}
    for i,city in enumerate(cities):
        city_coor = (city["coor"]["lat"], city["coor"]["long"])
        distances[str(i)] = great_circle(user_coor, city_coor)
    return cities[int(min(distances, key=distances.get))]

def correct_synonyms(country_name):
    if (country_name=="United States"): # Da notare che se geolocalizzo come United States allora è perchè user:location è "USA" o simili -> verrà scelta come città Denver in colorado perchè è in centro agli stati uniti
        return "United States of America"
    else:
        return country_name

#------------------------------------------------------------------------------#

"""
Sentiment analysis sul testo del tweet o retweet (? da definire bene il campo)
Prima dell'analisi il testo è tradotto
"""

def analyze_sentiment(text):
    try:
        if text:
            analysis = TextBlob(clean_tweet_text(text))
            if analysis.sentiment.polarity > 0:
                return {"polarity": analysis.sentiment.polarity, "sentiment": "positive"}
            elif analysis.sentiment.polarity == 0:
                return {"polarity": analysis.sentiment.polarity, "sentiment": "neutral"}
            else:
                return {"polarity": analysis.sentiment.polarity, "sentiment": "negative"}
        else:
            return False
    except Exception as e:
        print("\n" + "Fail in sentiment analysis \n" + str(e) +"\n")
        return False

def clean_tweet_text(text):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

def eng_translation(text):
    try:
        tr = TRANS.translate(text)
        if tr.text:
            return tr.text
        else:
            return False
    except Exception as e:
        print("\n" + "fail in translation -> " + str(e)  + " -> return text in original language")
        return text

#------------------------------------------------------------------------------#

def full_tweet_text(tweet):
    try:
        if ("retweeted_status" in tweet):
            if ("extended_tweet" in tweet["retweeted_status"]):
                return tweet["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                return tweet["retweeted_status"]["text"]
        else:
            return tweet["extended_tweet"]["full_text"]
    except Exception as e:
        print("\n" + "failing while exctracting full text due to \n" + str(e) + "\n" + "returning text may be truncated")
        return tweet["text"]

#------------------------------------------------------------------------------#
