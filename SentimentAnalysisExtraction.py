# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

from CSVHandler import CSVHandler
from SentimentExtractor import SentimentExtractor

dataset_file_pathToFile = 'datasets'
dataset_file_name = 'train.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name
requestIntervalSeconds = 3

sentimentExtractor = SentimentExtractor("meaningCloud_APIKey", ".env.json", dataset_file_path, requestIntervalSeconds)
sentimentExtractor.extractFeatures()

# Name of the file with the results
resultsFile = dataset_file_pathToFile + '/' + 'RESULTS_' + dataset_file_name
myCSVWriter = CSVHandler(resultsFile, sentimentExtractor.tweetList)
myCSVWriter.writeTweetsToFile()