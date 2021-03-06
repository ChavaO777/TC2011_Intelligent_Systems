# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

from CSVHandler import CSVHandler
from SentimentAnalysisExtractor import SentimentAnalysisExtractor

# Set the data set path file
dataset_file_pathToFile = 'datasets/with_extra_features'
dataset_file_name = 'Emotion_test.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name

# Set the request's interval
requestIntervalSeconds = 0.5

# Instantiate a SentimentAnalysisExtractor
sentimentAnalysisExtractor = SentimentAnalysisExtractor(dataset_file_path, requestIntervalSeconds, "meaningCloud_APIKey", ".env.json")
sentimentAnalysisExtractor.extractFeatures()

# Write the results to a new CSV file.
resultsFile = dataset_file_pathToFile + '/' + 'RESULTS_SENTIMENT-ANALYSIS_' + dataset_file_name
myCSVWriter = CSVHandler(resultsFile, sentimentAnalysisExtractor.tweetList)
myCSVWriter.writeTweetsToFile()