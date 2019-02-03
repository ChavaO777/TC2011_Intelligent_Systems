import json

class JSONHandler:

    @staticmethod
    def readKeyValue(pathToFile, keyName):
    
        with open(pathToFile) as f:
            data = json.load(f)
        
        return data[keyName]