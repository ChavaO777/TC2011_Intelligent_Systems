import csv

import tweet

with open('datasets/train.csv', 'rb') as f:

    counter = 0

    for line in f:

        line = line.decode(errors='ignore')
        row = line.split(',')
        t = tweet.Tweet(row[0], row[1])
        
        if counter%101 == 0:
            print(t.text + " -> " + t.isBot)
        
        counter += 1
    
# print("counter = " + str(counter))