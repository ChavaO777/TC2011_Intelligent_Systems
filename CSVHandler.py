# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

import json
import csv
from Tweet import Tweet

# Class to handle CSV file operations for the tweet lists
class CSVHandler:

    def __init__(self, csvFilePath, tweetList):

        self.csvFilePath = csvFilePath
        self.tweetList = tweetList

    # Method to write to a CSV file
    def writeTweetsToFile(self):

        # Write to the specified CSV file
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