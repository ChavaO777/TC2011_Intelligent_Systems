from EmotionExtractor import EmotionExtractor
from CSVHandler import CSVHandler

dataset_file_pathToFile = 'datasets'
dataset_file_name = 'RESULTS_SentimentAnalysis_01-29-2019_train.csv'
dataset_file_path = dataset_file_pathToFile + '/' + dataset_file_name
requestIntervalSeconds = 0.1

emotionExtractor = EmotionExtractor("indico_APIKey", ".env.json", dataset_file_path, requestIntervalSeconds)
emotionExtractor.setAPIKey()
emotionExtractor.extractFeatures()

# Name of the file with the results
resultsFile = dataset_file_pathToFile + '/' + 'FULL-RESULTS_MeaningCloud-Indico_train.csv' 
myCSVWriter = CSVHandler(resultsFile, emotionExtractor.tweetList)
myCSVWriter.writeTweetsToFile()