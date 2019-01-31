import json

class Tweet:

    def __init__(
        self,
        text,
        isBot,
        # MeaningCloud
        score_tag="",
        agreement="",
        subjectivity="",
        confidence=-1,
        irony="",
        # IndicoIO
        joy=-1.0,
        surprise=-1.0,
        fear=-1.0,
        sadness=-1.0,
        anger=-1.0):

        self.text = text
        self.isBot = isBot

        # MeaningCloud - Sentiment extraction
        # See MeaningCloud's documentation for
        # Sentiment Analysis for the definitions 
        # of the five attributes below
        self.score_tag = score_tag
        self.agreement = agreement
        self.subjectivity = subjectivity
        self.confidence = confidence
        self.irony = irony

        # Indico - EmotionExtraction
        self.joy = joy
        self.surprise = surprise
        self.fear = fear
        self.sadness = sadness
        self.anger = anger

    # Method that converts a Tweet to a JSON string
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def getCSVHeader():
        # Create a dummy tweet
        t = Tweet("", 1)
        # Get the JSON string of that tweet
        jsonStr = t.toJSON()
        # Get the JSON object of that string
        jsonObj = json.loads(jsonStr)
        # Get the keys of that JSON object
        jsonObjKeys = jsonObj.keys()
        # Make a list of the keys
        keysList = list(jsonObjKeys)
        return keysList

# t1 = Tweet(0, "Example", 1)
# print(t1.text)
# print(t1.isBot)
