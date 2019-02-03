# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

# Script for extracting emotions using Indico's emotion extraction API
from EmotionExtractor import EmotionExtractor
from CSVHandler import CSVHandler

# Set the data set path file
dataset_file_pathToFile = 'datasets'
dataset_file_name = 'RESULTS_SentimentAnalysis_01-29-2019_train.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name

# Set the request's interval
requestIntervalSeconds = 0.1

# Instantiate an EmotionExtractor
emotionExtractor = EmotionExtractor("indico_APIKey", ".env.json", dataset_file_path, requestIntervalSeconds)
emotionExtractor.setAPIKey()
emotionExtractor.extractFeatures()

# Write the results to a new CSV file.
resultsFile = dataset_file_pathToFile + '/' + 'FULL-RESULTS_SentimentAnalysis_Emotion_train.csv' 
myCSVWriter = CSVHandler(resultsFile, emotionExtractor.tweetList)
myCSVWriter.writeTweetsToFile()