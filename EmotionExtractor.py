import indicoio
import time
from FeatureExtractor import FeatureExtractor
from Tweet import Tweet

# Class for performing the emotion extraction from Indico

class EmotionExtractor(FeatureExtractor):

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
                # - text,
                # - isBot,
                # - score_tag
                # - agreement
                # - subjectivity
                # - confidence
                # - irony
                # 
                t = Tweet(
                    row[0],
                    int(row[1]),
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6]
                    )

                text = t.text
                tweetEmotionResponse = indicoio.emotion(text)
                emotionList = list(tweetEmotionResponse.items())

                # joy
                t.joy = emotionList[0][1]

                # surprise
                t.surprise = emotionList[1][1]

                # fear
                t.fear = emotionList[2][1]

                # sadness
                t.sadness = emotionList[3][1]

                # anger
                t.anger = emotionList[4][1]

                self.tweetList.append(t)

                counter += 1
                print("Tweets analyzed so far: " + str(counter))
                # Wait for a few seconds before making a new request
                time.sleep(self.requestIntervalSeconds)

    def setAPIKey(self):
        indicoio.config.api_key = self.apiKey