# @author Salvador Orozco Villalever - A07104218
# @version 01/28/2019

# Python script for the sentiment analysis extraction 

from CSVHandler import CSVHandler
from MiscellaneousFeaturesExtractor import MiscellaneousFeaturesExtractor

# Set the data set path file
dataset_file_pathToFile = 'datasets/with_extra_features'
dataset_file_name = 'SentimentAnalysis_Emotion_MiscellaneousFeatures_test.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name

# Set the request's interval
requestIntervalSeconds = 0.0001

# Instantiate a MiscellaneousFeaturesExtractor
miscellaneousFeaturesExtractor = MiscellaneousFeaturesExtractor(dataset_file_path, requestIntervalSeconds, apiKeyName="namesAPI_APIKey",pathToApiKeyFile=".env.json")
miscellaneousFeaturesExtractor.extractFeatures()

# Write the results to a new CSV file.
resultsFile = dataset_file_pathToFile + '/' + 'PLUS_NEW-FEATURES_' + dataset_file_name
myCSVWriter = CSVHandler(resultsFile, miscellaneousFeaturesExtractor.tweetList)
myCSVWriter.writeTweetsToFile()