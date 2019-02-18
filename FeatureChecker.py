# @author Salvador Orozco Villalever - A07104218
# @version 02/17/2019

import re

# Class for storing static methods to extract miscellaneous features
class FeatureChecker:

    @staticmethod
    def tweetIsQuote(tweet):

        # The following regular expression helps identify tweets that are quotes
        # 
        # E.g.
        # 1. @AndyChaney_ Imagination is more important than knowledge. - Albert Einstein
        # 2. For success attitude is equally as important as ability. - Harry F. Banks
        quoteRegex = "[\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7Ea-zA-Z\sä”0-9…ß]+ - [\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7Ea-zA-Z\sä”0-9…ß]+$"
        pattern = re.compile(quoteRegex)
        matchResults = pattern.match(tweet)

        try:
            return matchResults.string != None
            
        except:
            return False


        