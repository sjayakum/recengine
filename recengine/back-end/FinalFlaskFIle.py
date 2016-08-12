
# coding: utf-8

# In[1]:

from flask import Flask 
from flask import request
from flask import send_file
import re
from cookielib import CookieJar
import urllib2
import time
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import urllib2
import cookielib
import datetime as dt
from cookielib import CookieJar
import matplotlib.dates as mdates
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import urllib2
import cookielib
import datetime as dt
from cookielib import CookieJar
import matplotlib.dates as mdates
import numpy as np





cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

app = Flask(__name__)
memberID = 1
def testFunct():
    #uname = request.args.get('username')
    uname =  str(request.args.get('username'))
    passwd = str(request.args.get('password'))
    con = sqlite3.connect('stock.db')
    con.text_factory = str
    cursor = con.cursor()
    cursor.execute("SELECT memid from details where username='"+uname+"';")
    con.commit()
    s = cursor.fetchone()
    return s[0]
    
 
@app.route("/api/aurora/logins",methods=['GET','POST'])
def mem():

    global memberID
    memberID = testFunct()
    x = str(testFunct())
    return None

@app.route("/api/aurora/trending",methods=['GET','POST'])
def hello():
        try:
        
            x = ['YHOO','UNFI','FDX','NMBL','OVAS','VZ','BEAT']
            y = [31.43,50.91,151.08,25.46,17.89,45.71,16.54]
        
            i=0
            trending = ''
            while i < 7:
                trending += x[i]
                trending +=','
                trending +=str(y[i])
                trending +=','
                i+=1
            
            return trending
        except Exception, e:
            print(str(e))


# In[2]:

@app.route("/api/aurora/addwatch",methods=['GET','POST'])
def addwatch(stock):
    
    con = sqlite3.connect('stock.db')
    con.text_factory = str
    cursor = con.cursor()
    memberId = mem()
    cursor.execute("INSERT INTO watchlist values("+memberId+",'"+stock+"');")
    


# In[3]:

@app.route("/api/aurora/getwatch",methods=['GET','POST'])
def getWatch():
        con = sqlite3.connect('stock.db')
        con.text_factory = str
        cursor = con.cursor()
        cursor.execute("SELECT * from watchlist;")
        con.commit()
        s = cursor.fetchall()
        stocks = []
        for k in s:
            stocks.append(k[1])
        price = []
        for m in stocks:
            price.append(stockPrice(m))
            
        watchlist = ''
        
        i=0
        while i<len(price):
            watchlist+=stocks[i]
            watchlist+=','
            watchlist+=str(price[i])
            watchlist+=','
            i+=1

        return watchlist


# In[4]:

def bytespdate2num(fmt,encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter


def stockPrice(stock):
    
     
    
    
    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+'YHOO'+'/chartdata;type=quote;range=1y/csv'
    source_code = opener.open(stock_price_url).read().decode()
    
    stock_data = []
    split_source = source_code.split('\n')
    
    for line in split_source:
        split_line = line.split(',')
        
        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)
            
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters = {0: bytespdate2num('%Y%m%d')})
                                                        
    return np.asscalar(np.float64(closep[-1]))
    
@app.route("/api/aurora/stockdetails/",methods=['GET','POST'])
#CHANGE HERE
def stockDetails():
    stock = str(request.args.get('stockname'))
    
    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1y/csv'
    source_code = opener.open(stock_price_url).read().decode()
    
    stock_data = []
    split_source = source_code.split('\n')
    
    for line in split_source:
        split_line = line.split(',')
        
        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)
            
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters = {0: bytespdate2num('%Y%m%d')})
                                                        
    y = np.asscalar(np.float64(closep[-1]))
    x = np.asscalar(np.float64(openp[-1]))
    
    
    #add the naiveBayesClassifier here
    #per = getSentiment(stock)
    #per = 45
    
    return stock+','+str(x)+','+str(y)+','+str(per)




# In[5]:

@app.route("/api/aurora/graph",methods=['GET','POST'])
def thegraph():
    graph_data('AKAM')
    filename = '/home/vagrant/base.png'
    return send_file(filename,mimetype='image/png')
@app.route("/api/aurora/graphdetails/",methods=['GET','POST'])
def graph_data():
    #stock = str(request.args.get('stockname'))
    stock = 'YHOO'
    fig = plt.figure()
    ax1 = plt.subplot2grid((1,1),(0,0))     
    
    
    stock_price_url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range=1y/csv'
    source_code = opener.open(stock_price_url).read().decode()
    
    stock_data = []
    split_source = source_code.split('\n')
    
    for line in split_source:
        split_line = line.split(',')
        
        if len(split_line) == 6:
            if 'values' not in line and 'labels' not in line:
                stock_data.append(line)
                
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters = {0: bytespdate2num('%Y%m%d')})
                                                         
    #dateconv = np.vectorize(dt.datetime.fromtimestamp)
    #date = dateconv(date)
    
    ax1.plot_date(date,closep,'-')
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    ax1.grid(True,color='r')
    ax1.xaxis.label.set_color('c')
    ax1.yaxis.label.set_color('r')
    #can put a if statement here
      
    
    opening = np.asscalar(np.float64(openp[-1])) #opening price
    closing = np.asscalar(np.float64(closep[-1])) #closing price
    
    if (closing - opening) > 0:
        ax1.fill_between(date, closep,0,alpha=0.5,facecolor='green', interpolate=True)
    else:
        ax1.fill_between(date, closep,0,alpha=0.5,facecolor='red', interpolate=True)
    ax1.axhline((closep[0]+closep[-1])/2,color='k',linewidth=3,label="average")
    
    plt.xlabel("Dates")
    plt.ylabel("Price")
    plt.title(stock)
    plt.legend()
    plt.subplots_adjust(left=0.09,bottom=0.20,right=0.94,top=0.90,wspace=0.2,hspace=0)
    #plt.show()
    #savefig('base.png')

#@app.route("/api/aurora/getgraph",methods=['GET','POST'])
#def getGraph():
#    stock = request.args.get('stockname')
#    graph_data(stock)                                                         
    


# In[ ]:


#
# from test_helper import Test
# import os.path
# from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating
# model = 0
# stockDict = {0:'YHOO', 1:'UNFI', 2:'FDX', 3:'NMBL', 4:'OVAS', 5:'VZ', 6:'BEAT', 7:'NVAX', 8:'SO', 9:'RHT', 10:'VDSI', 11:'BMY', 12:'SPLK', 13:'CELG', 14:'QIHU', 15:'VOD', 16:'IGTE', 17:'ALXN', 18:'SCCO', 19:'GE', 20:'MRVL', 21:'CASY', 22:'TWTR', 23:'PYPL', 24:'FV', 25:'DUK', 26:'CNX', 27:'AU', 28:'HOLX', 29:'CTAS'}
# transformedList = []
# def myMapingFunction(x):
#     y = x.encode('utf8').split(",")
#     return y[1:41]
#
# def buildModel():
#     global model
#     rootDir = os.path.join('data')
#     inputFilePath = os.path.join('stock.csv')
#     stockFileName = os.path.join(rootDir,inputFilePath)
#
#     numPartitions = 2
#
#     rawData = sc.textFile(stockFileName,numPartitions)
#
#     newRawData = rawData.map(myMapingFunction)
#
#
#
#     likingList = newRawData.collect()
#     memid = 1
#     while memid < 24000:
#         i = 0
#         global transformedList
#         while i < 30:
#             if(float(likingList[memid][i])==99):
#                 transformedList.append((memid,i,0.0))
#             else:
#                 transformedList.append((memid,i,int(float(likingList[memid][i]))))
#
#             i = i + 1
#         memid = memid + 1
#
#     transData = sc.parallelize(transformedList)
#
#     trainingDataSet, testDataSet = transData.randomSplit([8, 2], 17)
#
#     # Build the recommendation model using Alternating Least Squares
#     rank = 5
#     numIterations = 5
#     model = ALS.train(trainingDataSet, rank, numIterations)
#
#     #EXTRACT ONLY (MEMBERID,STOCKID)
#     #testDataSetModified = testDataSet.map(lambda p:(p[0],p[1]))
#     #PREDICT
#     #predictedData = model.predictAll(testDataSetModified).map(lambda r: ((r[0], r[1]), r[2]))
#
#     #ratingsAndPredictions = transData.map(lambda r: ((r[0], r[1]), r[2])).join(predictedData)
#     #MSE = ratingsAndPredictions.map(lambda r: (r[1][0] - r[1][1])**2).mean()
#     #print("Root Mean Squared Error = " + str(MSE**0.5))
#
#
#
#
# @app.route("/api/aurora/recommend",methods=['GET','POST'])
# def getPredictions():
#     y = 0
#     tempList = [] #PREDICTED STOCK NUMBERS
#     #print "stkno"+"\t"+ "howmuch"
#     while y<30:
#         temp = (model.predict(335,y))
#         if temp > 0:
#             tempList.append(int(y))
#             #print str(y)+"\t"+str(temp)sto
#         y = y+1
#
#     finalList = [] #PREDICTED STOCK NAMES
#     for temp in tempList:
#         finalList.append(stockDict[temp])
#     tempTime = time.time()
#     x = [] #STOCK PRICES
#     for s in finalList:
#         x.append(stockPrice(s))
#     print "Stock Price time"
#     print time.time() - tempTime
#     i=0
#     recommend = ''
#     while i<len(x):
#         recommend+=str(finalList[i])
#         recommend+=','
#         recommend+=str(x[i])
#         recommend+=','
#         i+=1
#
#
#     return recommend
#
#
# #buildModel()
# #model.save(sc, "modelRecEng")
#
# # Trying to load saved model and work with it
# model = MatrixFactorizationModel.load(sc, "modelRecEng")
#

# In[18]:

# start_time = time.time()
# x = getPredictions(335)
# print x
# print time.time() - start_time


# In[ ]:

if __name__ == "__main__":
    app.run()


# In[39]:

# start_time = time.time()
#
# for i in range(30):
#     print model.predict(335,i)
# print time.time() - start_time


# In[26]:




