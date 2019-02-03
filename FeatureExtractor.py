import json
from JSONHandler import JSONHandler

class FeatureExtractor:

    def __init__(self, apiKeyName, pathToApiKeyFile, datasetFilePath, requestIntervalSeconds, tweetList=[]):

        self.apiKeyName = apiKeyName
        self.pathToApiKeyFile = pathToApiKeyFile
        self.apiKey = self.readAPIKey()
        self.datasetFilePath = datasetFilePath
        self.requestIntervalSeconds = requestIntervalSeconds
        self.tweetList = tweetList

    def extractFeatures(self):
        pass

    def setAPIKey(self):
        pass

    def readAPIKey(self):

        return JSONHandler.readKeyValue(self.pathToApiKeyFile, self.apiKeyName)