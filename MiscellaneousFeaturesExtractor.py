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
                text = row[0]

                t = Tweet(
                    text
                    ,int(row[1])
                    ,row[2]
                    ,row[3]
                    ,row[4]
                    ,row[5]
                    ,float(row[6])
                    ,self.tweetIsQuote(text)
                    )

                self.tweetList.append(t)

                counter += 1
                print("Tweets analyzed so far: " + str(counter))
                # Wait for a few seconds before making a new request
                time.sleep(self.requestIntervalSeconds)

    def tweetIsQuote(self, tweet):

        # The following regular expression helps identify tweets that are quotes
        # 
        # E.g.
        # 1. @AndyChaney_ Imagination is more important than knowledge. - Albert Einstein
        # 2. For success attitude is equally as important as ability. - Harry F. Banks
        stringWithSpecialCharactersRegex = "[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7Ea-zA-Z\sä”0-9…ß]+"
        quoteRegex = stringWithSpecialCharactersRegex + " - " + stringWithSpecialCharactersRegex
        pattern = re.compile(quoteRegex)
        matchResults = pattern.match(tweet)

        try:
            if matchResults.string != None:
                return 1

            return 0

        except:
            return 0


        