# @author Salvador Orozco Villalever - A07104218
# @version 02/02/2019

import json

# Class to handle JSON file operations
class JSONHandler:

    @staticmethod
    def readKeyValue(pathToFile, keyName):
    
        with open(pathToFile) as f:
            data = json.load(f)
        
        return data[keyName]