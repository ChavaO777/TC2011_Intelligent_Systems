# @author Salvador Orozco Villalever - A07104218
# @version 02/17/2019

import re
import time
from FeatureExtractor import FeatureExtractor
from Tweet import Tweet

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
                    # MeaningCloud's sentiment analysis features
                    ,score_tag=row[2]
                    ,agreement=row[3]
                    ,subjectivity=row[4]
                    ,confidence=row[5]
                    ,irony=row[6]
                    # Indico's emotion features
                    ,joy=float(row[7])
                    ,surprise=float(row[8])
                    ,fear=float(row[9])
                    ,sadness=float(row[10])
                    ,anger=float(row[11])
                    # ,self.tweetIsQuote(tweetText)
                    ,urlsCount=self.computeUrlsCountInTweet(tweetText)
                    ,mentionsCount=self.computeMentionsCountInTweet(tweetText)
                    ,isRetweet=self.isRetweet(tweetText)
                    ,wordsCount=self.computeWordsCount(tweetText)
                    ,hashtagsCount=self.computeHashstagsCount(tweetText)
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

    def tweetIsQuote(self, tweet):

        # The following regular expression helps identify tweets that are quotes
        # 
        # E.g.
        # 1. @AndyChaney_ Imagination is more important than knowledge. - Albert Einstein
        # 2. For success attitude is equally as important as ability. - Harry F. Banks
        strRegexPattern = "[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7Ea-zA-Z\sä”0-9…ß]+"
        quoteRegex = strRegexPattern + " - " + strRegexPattern
        
        return self.stringMatchesRegex(tweet, quoteRegex)

    def isRetweet(self, tweet):

        # The following regular expression helps identify tweets that are retweets
        # 
        # E.g.
        # 1. RT @chazzpalminteri: To all my students out there--keep strong and shine the white light.
        # 2. RT @BeingSalmanKhan: http://t.co/iYEkVeRnlm
        retweetRegexPattern = "^RT.*"
        
        return self.stringMatchesRegex(tweet, retweetRegexPattern)

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