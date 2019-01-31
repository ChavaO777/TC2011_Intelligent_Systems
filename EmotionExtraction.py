import indicoio
import json
import csv
import tweet
import time

with open('.env.json') as f:
    data = json.load(f)

# Required data for API calls
indicoio.config.api_key = data["indico_APIKey"]

dataset_file_pathToFile = 'datasets'
dataset_file_name = 'RESULTS_SentimentAnalysis_01-29-2019_train.csv'
dataset_file = dataset_file_pathToFile + '/' + dataset_file_name

# List of tweets
tweetsList = []
# Tweet counter
counter = 0
# List of the IDs of tweets whose requests failed
wrongRequestTweetIds = []

requestIntervalSeconds = 0.1

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
        t = tweet.Tweet(
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

        tweetsList.append(t)

        counter += 1
        # Reached 1543 on the first try!
        print("Tweets analyzed so far: " + str(counter))
        # Wait for a few seconds before making a new request
        time.sleep(requestIntervalSeconds)

# Name of the file with the results
resultsFile = dataset_file_pathToFile + '/' + 'FULL-RESULTS_MeaningCloud-Indico_train.csv' 
# resultsFile = dataset_file_pathToFile + '/' + 'LITE___-RESULTS_MeaningCloud-Indico_train.csv' 

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