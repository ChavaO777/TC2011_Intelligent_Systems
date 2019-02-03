# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

from CSVHandler import CSVHandler
from SentimentAnalysisExtractor import SentimentAnalysisExtractor

# Set the data set path file
dataset_file_pathToFile = 'datasets'
dataset_file_name = 'train.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name

# Set the request's interval
requestIntervalSeconds = 3

# Instantiate a SentimentAnalysisExtractor
sentimentAnalysisExtractor = SentimentAnalysisExtractor("meaningCloud_APIKey", ".env.json", dataset_file_path, requestIntervalSeconds)
sentimentAnalysisExtractor.extractFeatures()

# Write the results to a new CSV file.
resultsFile = dataset_file_pathToFile + '/' + 'RESULTS_' + dataset_file_name
myCSVWriter = CSVHandler(resultsFile, sentimentAnalysisExtractor.tweetList)
myCSVWriter.writeTweetsToFile()