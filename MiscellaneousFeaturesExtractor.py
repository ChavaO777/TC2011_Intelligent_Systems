# @author Salvador Orozco Villalever - A07104218
# @version 02/17/2019

import re
import time
from FeatureExtractor import FeatureExtractor
from Tweet import Tweet
import wikipedia
import requests

# Class for extracting miscellaneous features
class MiscellaneousFeaturesExtractor(FeatureExtractor):

    def extractFeatures(self):
       
        # Tweet counter
        counter = 0

        # Open the data set file
        with open(self.dataSetFilePath, 'rb') as f:

            # Flag to know whether the first line of the file (column names)
            # has been read
            headerPassed = False 

            for line in f:

                line = line.decode(errors='ignore')
                row = line.split(',')

                # i.e. if this is the first line of the file
                if headerPassed == False:
                    headerPassed = True
                    continue

                # Instantiate a tweet. Assume that the 
                # current CSV file which is being read 
                # already contains the following features 
                # per tweet:
                # 
                # - text

                tweetText = row[0]

                t = Tweet(
                    # Text
                    tweetText
                    # Class
                    ,isBot=int(row[1])
                    ############################################
                    # MeaningCloud's sentiment analysis features
                    ############################################
                    ,score_tag=row[2]
                    ,agreement=row[3]
                    ,subjectivity=row[4]
                    ,confidence=row[5]
                    ,irony=row[6]
                    ###########################
                    # Indico's emotion features
                    ###########################
                    ,joy=float(row[7])
                    ,surprise=float(row[8])
                    ,fear=float(row[9])
                    ,sadness=float(row[10])
                    ,anger=float(row[11])
                    ########################
                    # Miscellaneous features
                    ########################
                    ,urlsCount=int(row[12])
                    ,mentionsCount=int(row[13])
                    ,isRetweet=row[14]
                    ,wordsCount=int(row[15])
                    ,hashtagsCount=int(row[16])
                    ,upperCaseLettersCount=int(row[17])
                    ,lowerCaseLettersCount=int(row[18])
                    ,upperCaseWordsCount=int(row[19])
                    ,nonAlphabeticalCharactersCount=int(row[20])
                    ,averageWordLength=float(row[21])
                    ,isFamousQuote=row[22]
                    ,isFollowMeTweet=row[23]
                    ,isCheckOutTweet=row[24]
                    # New feature to extract
                    )

                self.tweetList.append(t)

                counter += 1
                print("Tweets analyzed so far: " + str(counter))
                # Wait for a few seconds before making a new request
                time.sleep(self.requestIntervalSeconds)

    def stringMatchesRegex(self, text, regexPattern):

        pattern = re.compile(regexPattern)
        matchResults = pattern.match(text)

        try:
            if matchResults.string != None:
                return 1

            return 0

        except:
            return 0

    def computeRegexMatchesInText(self, text, regexPattern):

        matches = re.findall(regexPattern, text)
        return len(matches)

    def computeUrlsCountInTweet(self, tweet):

        # The following regular expressions helps count the amount of URLs in a given tweet
        # including abbreviations or cases in which the URL was truncated.

        # Examples of URLs or truncated URLs
        # http://t.co/umDSXYAWm6 
        # http://t.co
        # http://t
        # http://
        urlStringRegex = "https?:\/\/"
        return self.computeRegexMatchesInText(text=tweet, regexPattern=urlStringRegex)

    def computeMentionsCountInTweet(self, tweet):

        # The following regular expressions helps count the amount of mentions 
        # in a given tweet. Twitter IDs may contain both lower and uppercase letters,
        # underscores and numbers.
        # 
        # Examples of mentions
        # @username
        # @Username
        # @user_name
        # @_username
        # @_username_
        mentionStringRegex = "@[a-zA-Z0-9_]+"
        return self.computeRegexMatchesInText(text=tweet, regexPattern=mentionStringRegex)

    def isRetweet(self, tweet):

        # The following regular expression helps identify tweets that are retweets
        # 
        # E.g.
        # 1. RT @chazzpalminteri: To all my students out there--keep strong and shine the white light.
        # 2. RT @BeingSalmanKhan: http://t.co/iYEkVeRnlm
        retweetRegexPattern = "^RT.*"
        
        ans = self.stringMatchesRegex(tweet, retweetRegexPattern)

        if ans:
            return True
        
        return False

    # Method that computes the amount of words of a tweet, splitting them by
    # whitespace.
    def computeWordsCount(self, tweet):

        return len(tweet.split())

    # Method that determines whether a word is a hashtag
    def isHashtag(self, word):

        return word.startswith('#')

    # Method that computes the amount of hashtags in a tweet
    def computeHashstagsCount(self, tweet):

        tweetWords = tweet.split()

        hashtagsCount = 0

        for i in range(len(tweetWords)):

            if self.isHashtag(tweetWords[i]):
                hashtagsCount += 1

        return hashtagsCount

    def computeUpperCaseLettersCount(self, tweet):

        return len(re.findall(r'[A-Z]', tweet))

    def computeLowerCaseLettersCount(self, tweet):

        return len(re.findall(r'[a-z]', tweet))

    def computeUpperCaseWordsCount(self, tweet):

        tweetWords = tweet.split()
        return sum(1 for word in tweetWords if word.isupper())

    def computeNonAlphabeticalCharactersCount(self, tweet):

        return self.computeTweetLength(tweet) - len(re.findall(r'[a-zA-Z]', tweet))

    def computeTweetLength(self, tweet):

        return len(tweet)

    def computeAverageWordLength(self, tweet):

        # Get the tweet's words
        tweetWords = tweet.split()

        # Delete the mentions
        tweetWordsWithoutMentions = [x for x in tweetWords if not x.startswith("@")]

        # Compute the average word length and return it
        
        if len(tweetWordsWithoutMentions) == 0:
            return 0
            
        return sum(len(word) for word in tweetWordsWithoutMentions)/len(tweetWordsWithoutMentions)

    def tweetHasQuoteStructure(self, tweet):

        # The following regular expression helps identify tweets that are quotes
        # 
        # E.g.
        # 1. @AndyChaney_ Imagination is more important than knowledge. - Albert Einstein
        # 2. For success attitude is equally as important as ability. - Harry F. Banks
        strRegexPattern = "[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7Ea-zA-Z\sä”0-9…ß]+"
        quoteRegex = strRegexPattern + " - " + strRegexPattern
        
        return self.stringMatchesRegex(tweet, quoteRegex)

    # Method that extracts the author of a given quote
    # 
    # E.g.
    # If the quote is "The power of intuitive understanding will protect you from harm until the end of your days. - Lao Tsu",
    # then the author is "Lao Tsu".
    def extractQuoteAuthor(self, tweet):

        # The author corresponds to the string after the last hyphen
        quoteSections = tweet.split("-")
        quoteAuthor = quoteSections[len(quoteSections) - 1]

        print("1 quoteAuthor = " + quoteAuthor)

        i = 0

        while i < len(quoteAuthor) and not quoteAuthor[i].isalpha():
            i += 1

        j = len(quoteAuthor) - 1
        while j >= i and not quoteAuthor[j].isalpha() and not quoteAuthor[j] == '.':
            j -= 1

        # Delete the last dot if there exists one. E.g. 'John Doe.'
        if j == len(quoteAuthor) - 1 and quoteAuthor[j] == '.':
            j -= 1

        quoteAuthor = quoteAuthor[i:(j + 1)]

        print("2 quoteAuthor = " + quoteAuthor)

        return quoteAuthor

    # Method that searches a given topic on Wikipedia
    def performWikipediaSearch(self, searchTopic):

        try:
            topicWikipediaSearch = wikipedia.search(searchTopic)
        except:
            return False

        return True

    # Method that retrieves the page of a given topic on Wikipedia
    def getWikipediaPage(self, searchTopic):

        topicWikipediaPage = None

        try:
            topicWikipediaPage = wikipedia.page(searchTopic)
            # print("topicWikipediaPage = " + str(topicWikipediaPage))
        except:
            return None

        return topicWikipediaPage

    def computeLevenshteinDistance(self, s1, s2):

        if len(s1) > len(s2):
            s1, s2 = s2, s1

        distances = range(len(s1) + 1)
        for i2, c2 in enumerate(s2):
            distances_ = [i2+1]
            for i1, c1 in enumerate(s1):
                if c1 == c2:
                    distances_.append(distances[i1])
                else:
                    distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
            distances = distances_
        return distances[-1]

    # Method that determines whether a topic exists on Wikipedia.
    # It checks whether a given page exists.
    def topicExistsOnWikipedia(self, searchTopic):

        wikipediaPage = self.getWikipediaPage(searchTopic)

        # If the page wasn't found
        if not wikipediaPage:
            return False

        if searchTopic in wikipediaPage.original_title or wikipediaPage.original_title in searchTopic:
            return True

        # If the page was found, make sure it actually is relevant.
        # i.e. make sure the page is about the search topic by computing
        # the Levenshtein Distance between the search topic and the 
        # Wikipedia page title.
        MAXIMUM_DESIRED_LEVENSHTEIN_DISTANCE = 5
        levenshteinDistance = self.computeLevenshteinDistance(searchTopic, wikipediaPage.original_title)

        print("levenshteinDistance between '" + searchTopic + "' and '" + wikipediaPage.original_title + "' = " + str(levenshteinDistance))
        return levenshteinDistance < MAXIMUM_DESIRED_LEVENSHTEIN_DISTANCE
        # or self.performWikipediaSearch(searchTopic)

    def nameExistsOnNameAPI(self, name):

        nameWords = name.split(" ")

        # Get the last name
        lastName = nameWords[len(nameWords) - 1]
        positiveConfidenceTreshold = 0.55

        # Concatenate the rest of the full name assuming it is the first name
        firstName = " ".join(nameWords[0:(len(nameWords) - 1)])

        nameAPIKey = self.apiKey

        # url of the NameAPI.org endpoint:
        url = ("http://api.nameapi.org/rest/v5.3/parser/personnameparser?apiKey=" + nameAPIKey)

        # Dict of data to be sent to NameAPI.org:
        payload = {
            "inputPerson": {
                "type": "NaturalInputPerson",
                "personName": {
                    "nameFields": [
                        {
                            "string": firstName,
                            "fieldType": "GIVENNAME"
                        }, {
                            "string": lastName,
                            "fieldType": "SURNAME"
                        }
                    ]
                },
                "gender": "UNKNOWN"
            }
        }

        foundOnNameAPI = False

        # Proceed, only if no error:
        try:
            # Send request to NameAPI.org by doing the following:
            # - make a POST HTTP request
            # - encode the Python payload dict to JSON
            # - pass the JSON to request body
            # - set header's 'Content-Type' to 'application/json' instead of
            #   default 'multipart/form-data'
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            # Decode JSON response into a Python dict:
            resp_dict = resp.json()
            print(resp_dict)
            responseConfidence = resp.json()['matches'][0]['confidence']

            # Check the confidence to determine whether it was really a name
            foundOnNameAPI = responseConfidence > positiveConfidenceTreshold

        except requests.exceptions.HTTPError as e:
            print("Bad HTTP status code:", e)
        except requests.exceptions.RequestException as e:
            print("Network error:", e)

        return foundOnNameAPI

    def authorExistsInQuotesAuthorList(self, quoteAuthor):

        quoteAuthorsFileName = "datasets/with_extra_features/trainingDataSetQuoteAuthors.txt"

        with open(quoteAuthorsFileName) as f:
            quoteAuthorsFileContentList = f.readlines()

        # Remove whitespace characters like '\n' at the end of each line
        quoteAuthorsFileContentList = [x.strip() for x in quoteAuthorsFileContentList] 

        return any(quoteAuthor.lower() in author.lower() for author in quoteAuthorsFileContentList)

    # Method that determines whether a given string corresponds to a valid author.
    # It first checks in the list of authors in the training dataset. If it doesn't
    # find the author, it then proceeds to check on Wikipedia.
    def isValidAuthor(self, quoteAuthor):

        # Check if it's a proverb
        if "proverb" in quoteAuthor.lower() or "author" in quoteAuthor.lower() or "anonymous" in quoteAuthor.lower():
            return True

        if len(quoteAuthor.split(" ")) > 4:
            return False

        # Look for the author in the authors list
        authorFoundInList = self.authorExistsInQuotesAuthorList(quoteAuthor) 

        if authorFoundInList:
            print("Author found in list!")
            return True

        else:
            print("Author NOT found in list")

        authorFoundOnWikipedia = self.topicExistsOnWikipedia(quoteAuthor)
        authorFoundOnNameAPI = False

        if authorFoundOnWikipedia:
            print("Author '" + quoteAuthor + "' found on Wikipedia")

        else:
            print("Author '" + quoteAuthor + "' NOT found on Wikipedia")

            authorFoundOnNameAPI = (self.nameExistsOnNameAPI(quoteAuthor)) or ("prince" in quoteAuthor.lower())

            if authorFoundOnNameAPI:
                print("Author '" + quoteAuthor + "' found on NameAPI or name contains the string 'prince'.")

            else:
                print("Author '" + quoteAuthor + "' NOT found on NameAPI")

        
        return authorFoundOnWikipedia or authorFoundOnNameAPI

    def isFamousQuote(self, tweet):

        # Check whether the tweet is a quote
        if not self.tweetHasQuoteStructure(tweet):
            return False

        # Get the quote's author
        quoteAuthor = self.extractQuoteAuthor(tweet)

        return self.isValidAuthor(quoteAuthor)

    def tweetContainsSubString(self, tweet, substring):

        return substring in tweet.lower()   
    
    def isFollowMeTweet(self, tweet):

        return self.tweetContainsSubString(tweet, "follow me")

    def isCheckOutTweet(self, tweet):

        return self.tweetContainsSubString(tweet, "check out")

