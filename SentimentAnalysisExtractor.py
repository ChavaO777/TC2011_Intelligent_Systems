# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

import time
from FeatureExtractor import FeatureExtractor
from Tweet import Tweet
import meaningcloud

# Class for performing the sentiment analysis extraction from MeaningCloud

class SentimentAnalysisExtractor(FeatureExtractor):

    def extractFeatures(self):

        # The language of the tweets
        tweetLang = 'en'
        # Tweet counter
        counter = 0
        # List of the IDs of tweets whose requests failed
        wrongRequestTweetIds = []

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
                # - text,
                # - isBot
                # 
                t = Tweet(row[0], int(row[1]))
                text = t.text
                sentiment_response = meaningcloud.SentimentResponse(meaningcloud.SentimentRequest(self.apiKey, lang=tweetLang, txt=text, txtf='plain').sendReq())

                if (sentiment_response.isSuccessful()):
                    
                    # Populate the remaining fields of this Tweet instance
                    t.score_tag = sentiment_response.getGlobalScoreTag()
                    t.agreement = sentiment_response.getGlobalAgreement()
                    t.subjectivity = sentiment_response.getSubjectivity()
                    t.confidence = sentiment_response.getGlobalConfidence()
                    t.irony = sentiment_response.getIrony()
                    self.tweetList.append(t)

                else:
                    # Let's see why the request failed
                    requestStatusCode = sentiment_response.getStatusCode()
                    requestStatusMsg = sentiment_response.getStatusMsg()
                    print("Tweet id = " + str(counter) + "; request status code = " + str(requestStatusCode) + "; request status msg = " + str(requestStatusMsg))
                    # Store this tweet ID for later. Another request will have to be made.
                    wrongRequestTweetIds.append(counter)

                counter += 1

                print("Tweets analyzed so far: " + str(counter))
                # Wait for a few seconds before making a new request
                time.sleep(self.requestIntervalSeconds)
            
            print("\nTotal analyzed tweets = " + str(counter))

            # If all requests succeeded
            if len(wrongRequestTweetIds) == 0:

                print("All " + str(counter) + " requests were successful.")

            else:

                print("The requests for the following tweets failed:\n")
                print(wrongRequestTweetIds)