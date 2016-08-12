#import numpy as np
import csv

def tweets(stock):
   tweets = []
   with open(stock+'.csv','r') as csvfile:
       plots = csv.reader(csvfile,delimiter=',')
       for row in plots:
           tweets.append(row[2])
       print(tweets[1:])
        
tweets('YHOO')