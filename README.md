# TC2011_Intelligent_Systems
Repository for my Intelligent Systems course at Monterrey Institute of Technology

## Feature extraction

### Sentiment analysis extraction using MeaningCloud's API

- To execute the sentiment analysis extraction:
    -  Go to the 'SentimentAnalysisExtraction.py' script and define the following elements:
       - the data set file path to read tweets from
       - the request interval in seconds
    - Run the following command in bash:  
        $ SentimentAnalysisExtraction.py


### Emotion extraction using Indico's API

- To execute the emotion extraction:
    - Go to the 'EmotionExtraction.py' script and define the following elements:
        - the data set file path to read tweets from
        - the request interval in seconds
    - Run the following command in bash:  
        $ EmotionExtraction.py

#### Note:
Both processes require API keys which you can get on [MeaningCloud](https://www.meaningcloud.com) and [Indico](https://indico.io/). To prevent these secret keys from being published on GitHub, they were both stored in a JSON environment file called '.env.json' and this file's name was added to the .gitignore file.