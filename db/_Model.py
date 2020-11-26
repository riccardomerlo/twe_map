class Model():
    """
    Classe per gestire/controllare/costruire gli schemi json dei documenti da memorizzare
    """
    def __init__(self):
        pass

    def tweet_model(self, topic, analysis):
        tweet_doc = {"time": analysis["tweet"]["created_at"],
                     "text": analysis["text"],
                     "topic": topic,
                     "location":  analysis["location"] if analysis["location"] else "null",
                     "sentiment": analysis["sentiment"] if analysis["sentiment"] else "null"}
        return tweet_doc
