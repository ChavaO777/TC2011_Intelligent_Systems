# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

from JSONHandler import JSONHandler

# Abstract class representing feature extractors
class FeatureExtractor:

    # Constructor of the class
    def __init__(self, apiKeyName, pathToApiKeyFile, dataSetFilePath, requestIntervalSeconds, tweetList=[]):

        # Name of the API key in the secret JSON file
        self.apiKeyName = apiKeyName
        # Path to the secret JSON file
        self.pathToApiKeyFile = pathToApiKeyFile
        # API key stored in the secret JSON file
        self.apiKey = self.readAPIKey()
        # Path to the data set file
        self.dataSetFilePath = dataSetFilePath
        # Interval between requests in seconds
        self.requestIntervalSeconds = requestIntervalSeconds
        # List of tweets whose features are to be extracted
        self.tweetList = tweetList

    # Abstract method for actually extracting the features
    def extractFeatures(self):
        pass

    # Method for reading the API key from a JSON file
    def readAPIKey(self):

        return JSONHandler.readKeyValue(self.pathToApiKeyFile, self.apiKeyName)