import json
import csv
from Tweet import Tweet

class CSVHandler:

    def __init__(self, csvFilePath, tweetList):

        self.csvFilePath = csvFilePath
        self.tweetList = tweetList

    def writeTweetsToFile(self):

        # Write to a new CSV file
        with open(self.csvFilePath, 'w', newline='') as csvfile:
            
            # Write the header of the CSV file
            fieldnames = Tweet.getCSVHeader()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write the rows of the CSV file
            for currentTweet in self.tweetList:

                # Get the JSON string of that tweet
                tweetJsonStr = currentTweet.toJSON()
                # Get the JSON object of that string
                tweetJsonObj = json.loads(tweetJsonStr)
                # Write the row in the CSV file
                writer.writerow(tweetJsonObj)