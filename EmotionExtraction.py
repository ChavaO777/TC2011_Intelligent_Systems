# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

# Script for extracting emotions using Indico's emotion extraction API
from EmotionExtractor import EmotionExtractor
from CSVHandler import CSVHandler

# Set the data set path file
dataset_file_pathToFile = 'datasets'
dataset_file_name = 'test_copy.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name

# Set the request's interval
requestIntervalSeconds = 0.1

# Instantiate an EmotionExtractor
emotionExtractor = EmotionExtractor(dataset_file_path, requestIntervalSeconds, "indico_APIKey", ".env.json")
emotionExtractor.setAPIKey()
emotionExtractor.extractFeatures()

# Write the results to a new CSV file.
resultsFile = dataset_file_pathToFile + '/' + 'test_copy_EmotionFeatures.csv' 
myCSVWriter = CSVHandler(resultsFile, emotionExtractor.tweetList)
myCSVWriter.writeTweetsToFile()