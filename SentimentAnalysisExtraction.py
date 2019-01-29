# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

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
dataset_file_name = 'train_lite.csv'
dataset_file = dataset_file_pathToFile + '/' + dataset_file_name
tweetLang = 'en'

tweetsList = []
wrongRequestTweetIds = []
CSV_FileHeaders = ''

with open(dataset_file, 'rb') as f:

    # Tweet counter
    counter = 0
    # Flag to know whether the first line of the file (column names)
    # has been read
    headerPassed = False 

    for line in f:

        line = line.decode(errors='ignore')
        row = line.split(',')

        if headerPassed == False:
            headerPassed = True
            # Store the headers of the CSV file
            CSV_FileHeaders = row
            continue

        t = tweet.Tweet(row[0], int(row[1]))
        text = t.text
        sentiment_response = meaningcloud.SentimentResponse(meaningcloud.SentimentRequest(license_key, lang=tweetLang, txt=text, txtf='plain').sendReq())

        if (sentiment_response.isSuccessful()):
            
            # print("\nThe request to 'Sentiment analysis' finished successfully!\n")
            t.score_tag = sentiment_response.getGlobalScoreTag()
            t.agreement = sentiment_response.getGlobalAgreement()
            t.subjectivity = sentiment_response.getSubjectivity()
            t.confidence = sentiment_response.getGlobalConfidence()
            t.irony = sentiment_response.getIrony()
            tweetsList.append(t)

        else:
            requestStatusCode = sentiment_response.getStatusCode()
            requestStatusMsg = sentiment_response.getStatusMsg()
            print("Tweet id = " + str(t.id) + "; request status code = " + str(requestStatusCode) + "; request status msg = " + str(requestStatusMsg))
            wrongRequestTweetIds.append(counter)

        counter += 1
    
print("\ncounter = " + str(counter))

if len(wrongRequestTweetIds) == 0:

    print("All " + str(counter) + " requests were successful.")

else:

    print("The requests for the following tweets failed:\n")
    print(wrongRequestTweetIds)


resultsFile = dataset_file_pathToFile + '/' + 'RESULTS_' + dataset_file_name

with open(resultsFile, 'w', newline='') as csvfile:
    fieldnames = tweet.Tweet.getCSVHeader()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for tweet in tweetsList:

        # Get the JSON string of that tweet
        jsonStr = tweet.toJSON()
        # Get the JSON object of that string
        jsonObj = json.loads(jsonStr)
        writer.writerow(jsonObj)