# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

import time
import csv
import tweet
import json
from pprint import pprint
import meaningcloud

with open('.env.json') as f:
    data = json.load(f)

# Required data for API calls
license_key = data["meaningCloud_APIKey"]
dataset_file_pathToFile = 'datasets'
dataset_file_name = 'train.csv'
dataset_file = dataset_file_pathToFile + '/' + dataset_file_name
tweetLang = 'en'

# List of tweets
tweetsList = []
# Tweet counter
counter = 0
# List of the IDs of tweets whose requests failed
wrongRequestTweetIds = []

requestIntervalSeconds = 3

# Open the data set file
with open(dataset_file, 'rb') as f:

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

        # Instantiate a tweet
        t = tweet.Tweet(row[0], int(row[1]))
        text = t.text
        sentiment_response = meaningcloud.SentimentResponse(meaningcloud.SentimentRequest(license_key, lang=tweetLang, txt=text, txtf='plain').sendReq())

        if (sentiment_response.isSuccessful()):
            
            # Populate the remaining fields of this Tweet instance
            t.score_tag = sentiment_response.getGlobalScoreTag()
            t.agreement = sentiment_response.getGlobalAgreement()
            t.subjectivity = sentiment_response.getSubjectivity()
            t.confidence = sentiment_response.getGlobalConfidence()
            t.irony = sentiment_response.getIrony()
            tweetsList.append(t)

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
        time.sleep(requestIntervalSeconds)
    
print("\nTotal analyzed tweets = " + str(counter))

# If all requests succeeded
if len(wrongRequestTweetIds) == 0:

    print("All " + str(counter) + " requests were successful.")

else:

    print("The requests for the following tweets failed:\n")
    print(wrongRequestTweetIds)

# Name of the file with the results
resultsFile = dataset_file_pathToFile + '/' + 'RESULTS_' + dataset_file_name

# Write to a new CSV file
with open(resultsFile, 'w', newline='') as csvfile:
    
    # Write the header of the CSV file
    fieldnames = tweet.Tweet.getCSVHeader()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write the rows of the CSV file
    for tweet in tweetsList:

        # Get the JSON string of that tweet
        jsonStr = tweet.toJSON()
        # Get the JSON object of that string
        jsonObj = json.loads(jsonStr)
        # Write the row in the CSV file
        writer.writerow(jsonObj)