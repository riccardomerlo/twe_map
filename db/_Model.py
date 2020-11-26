import time

class Model():
    """
    Classe per gestire/controllare/costruire gli schemi json dei documenti da memorizzare
    """
    def __init__(self):
        pass

    def tweet_model(self, topic, analysis):
        #cast a timestamp della stringa Date
        x = time.strptime(analysis["tweet"]["created_at"], '%a %b %d %H:%M:%S %z %Y')
        analysis["tweet"]["created_at"] = time.strftime('%Y/%m/%d %H:%M:%S', x)

        #cast a float delle coordinate
        analysis["location"]["city"]["coor"]["lat"] = float(analysis["location"]["city"]["coor"]["lat"])
        analysis["location"]["city"]["coor"]["long"] = float(analysis["location"]["city"]["coor"]["long"])

        tweet_doc = {"time": analysis["tweet"]["created_at"],
                     "text": analysis["text"],
                     "topic": topic,
                     "location":  analysis["location"] if analysis["location"] else "null",
                     "sentiment": analysis["sentiment"] if analysis["sentiment"] else "null"}
        return tweet_doc
