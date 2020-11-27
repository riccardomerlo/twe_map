from streaming._Streamer import *
from db._Mongo import *

from threading import Thread

#------------------------------------------------------------------------------#

# TWEET STREAMING FILTERS
### 'track'         →   lista di keywords
### 'is_async'      →   stream su thread separato
### 'filter_level'  →   "none"|"low"|"medium", da capire
### 'language'      →   lista di sigle linguaggi BCP 47
### 'follow'        →   lista di ID utenti
### 'location'      →   lista di coppie long,lat. è possibile fare bbox con long1,lat1,long2,lat2 con 1 che è l'angolo sud-est
### 'count'         →   da capire
stream_filters = {

    "track": [ 'topic' ], # tutto minuscolo per favore

    #"locations": [-122.75,36.8, -121.75,37.8],

    "is_async": False

    # ... others
}

# TWEET LIMIT PER TOPIC
limit = 100

#------------------------------------------------------------------------------#

twitter_db = Mongo("twDB")

tweet_streamer = Streamer()

threads = []
for k in stream_filters["track"]:
    sf = stream_filters
    sf["track"] = [k]
    threads.append(Thread(target=tweet_streamer.stream(twitter_db, sf, k, limit)))

[t.start() for t in threads]

print('\n' + "done" + '\n')
