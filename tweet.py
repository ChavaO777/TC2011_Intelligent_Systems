# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

import json

# Class representing a tweet according to the features we've extracted so far.

class Tweet:

    def __init__(
        self
        ,text
        ,isBot=-1

        # MeaningCloud
        ,score_tag=""
        ,agreement=""
        ,subjectivity=""
        ,confidence=-1
        ,irony=""

        # ,IndicoIO
        ,joy=-100.0
        ,surprise=-100.0
        ,fear=-100.0
        ,sadness=-100.0
        ,anger=-100.0

        # Extra features
        ,urlsCount=-1
        ,mentionsCount=-1
        ,isRetweet=-1
        ,wordsCount=-1
        ,hashtagsCount=-1
        ,upperCaseLettersCount=-1
        ,lowerCaseLettersCount=-1
        ,upperCaseWordsCount=-1
        ,nonAlphabeticalCharactersCount=-1
        ,averageWordLength=-1.0
        ,isFamousQuote=False
        # ,isFollowMeTweet=False
        ):

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

        # Extra features
        self.urlsCount = urlsCount
        self.mentionsCount = mentionsCount
        self.isRetweet = isRetweet
        self.wordsCount = wordsCount
        self.hashtagsCount = hashtagsCount
        self.upperCaseLettersCount = upperCaseLettersCount
        self.lowerCaseLettersCount = lowerCaseLettersCount
        self.upperCaseWordsCount = upperCaseWordsCount
        self.nonAlphabeticalCharactersCount = nonAlphabeticalCharactersCount
        self.averageWordLength = averageWordLength
        self.isFamousQuote = isFamousQuote

    # Method that converts a Tweet to a JSON string
    def toJSON(self):
        
        return json.dumps(self, default=lambda o: o.__dict__)

    # Method that gets the appropriate CSV header according
    # to the class' attributes
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