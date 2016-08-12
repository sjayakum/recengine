
# coding: utf-8

# In[1]:

from test_helper import Test
import os.path

def myMapingFunction(x):
    y = x.encode('utf8').split(",")
    return y[1:41]

rootDir = os.path.join('data')
inputFilePath = os.path.join('stock.csv')
stockFileName = os.path.join(rootDir,inputFilePath)

numPartitions = 2

rawData = sc.textFile(stockFileName,numPartitions)

totalPoints = rawData.count()
print totalPoints


sampleData = rawData.take(5)
#print sampleData

newRawData = rawData.map(myMapingFunction)

print len(newRawData.take(1)[0])


print newRawData.take(5)


# In[2]:

#TRANSFORM THE DATA

transformedList = []

likingList = newRawData.collect()
memid = 1
while memid < 24000:
    i = 0
    global transformedList
    while i < 40:
        if(float(likingList[memid][i])==99):
            transformedList.append((memid,i,0.0))
        else:
            transformedList.append((memid,i,int(float(likingList[memid][i]))))
                     
        i = i + 1
    memid = memid + 1
    
print transformedList[0:40]


# In[4]:

transData = sc.parallelize(transformedList)


print transData
print transData.count()
print transData.take(2)


# In[6]:

#BUILDING THE MODEL


from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating


trainingDataSet, testDataSet = transData.randomSplit([8, 2], 17)

# Build the recommendation model using Alternating Least Squares
rank = 5
numIterations = 5
model = ALS.train(trainingDataSet, rank, numIterations)


# In[38]:

# Evaluate the model on training data

#EXTRACT ONLY (MEMBERID,STOCKID)
testDataSetModified = testDataSet.map(lambda p:(p[0],p[1]))
#PREDICT
predictedData = model.predictAll(testDataSetModified).map(lambda r: ((r[0], r[1]), r[2]))

ratingsAndPredictions = transData.map(lambda r: ((r[0], r[1]), r[2])).join(predictedData)
MSE = ratingsAndPredictions.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Root Mean Squared Error = " + str(MSE**0.5))



# In[64]:

### print newRawData.take(30)[25][7]

print newRawData.take(30)[25]

plotActualData = []
loopThroughData = newRawData.take(40)[30]
for x in loopThroughData:
    if float(x) == 99:
        plotActualData.append(0)
    else:
        plotActualData.append(int(float(x)))

plotPredictedData = []

k = 0
while (k<40):
    plotPredictedData.append(int(model.predict(30,k)))
    k = k + 1

import matplotlib.pyplot as plt



plt.plot(range(40),plotActualData,label='actual')
plt.plot(range(40),plotPredictedData,label='predicted')
plt.show()





# In[65]:


print plotActualData[23]
print plotPredictedData[23]


# In[76]:


y = 0
print "stkno"+"\t"+ "howmuch"
while y<40:
    temp = int(model.predict(23,y))
    if temp > 0:
        print str(y)+"\t"+str(temp)
    y = y+1


# In[4]:

print rawData.take(2)


# In[7]:

from test_helper import Test
import os.path
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

transformedList = []
transData = 0
newRawData = 0
model = 0


def myMapingFunction(x):
    y = x.encode('utf8').split(",")
    return y[1:41]

def LoadData():
    global newRawData
    rootDir = os.path.join('data')
    inputFilePath = os.path.join('stock.csv')
    stockFileName = os.path.join(rootDir,inputFilePath)
    numPartitions = 2
    rawData = sc.textFile(stockFileName,numPartitions)

    totalPoints = rawData.count()
    print totalPoints

    #sampleData = rawData.take(5)
    #print sampleData

    newRawData = rawData.map(myMapingFunction)

    #print len(newRawData.take(1)[0])
    #print newRawData.take(5)

def ReduceAndTransfromData():
        #TRANSFORM THE DATA
    global transData

    likingList = newRawData.collect()
    memid = 1
    while memid < 24000:
        i = 0
        global transformedList
        while i < 40:
            if(float(likingList[memid][i])==99):
                transformedList.append((memid,i,0.0))
            else:
                transformedList.append((memid,i,int(float(likingList[memid][i]))))

            i = i + 1
        memid = memid + 1

    #print transformedList[0:40]

    transData = sc.parallelize(transformedList)


    #print transData
    #print transData.count()
    #print transData.take(2)



#BUILDING THE MODEL



def makeModel():
    global model
    global transData
    trainingDataSet, testDataSet = transData.randomSplit([8, 2], 17)

    # Build the recommendation model using Alternating Least Squares
    rank = 5
    numIterations = 5
    model = ALS.train(trainingDataSet, rank, numIterations)




    # Evaluate the model on training data

    #EXTRACT ONLY (MEMBERID,STOCKID)
    testDataSetModified = testDataSet.map(lambda p:(p[0],p[1]))
    #PREDICT
    predictedData = model.predictAll(testDataSetModified).map(lambda r: ((r[0], r[1]), r[2]))

    ratingsAndPredictions = transData.map(lambda r: ((r[0], r[1]), r[2])).join(predictedData)
    MSE = ratingsAndPredictions.map(lambda r: (r[1][0] - r[1][1])**2).mean()
    print("Root Mean Squared Error = " + str(MSE**0.5))

def getPredictions(memid):
    y = 0
    tempList = []
    print "stkno"+"\t"+ "howmuch"
    while y<40:
        temp = int(model.predict(23,y))
        if temp > 0:
            tempList.append(temp)
            print str(y)+"\t"+str(temp)
        y = y+1
    return tempList


def getRecommendation(memid):
    getPredictions(memid)

def makeModelReady():
    LoadData()
    ReduceAndTransfromData()
    makeModel()

makeModelReady()
getRecommendation(30)


# In[8]:

getRecommendation(29)


# In[ ]:


### print newRawData.take(30)[25][7]

print newRawData.take(30)[25]

plotActualData = []
loopThroughData = newRawData.take(40)[30]
for x in loopThroughData:
    if float(x) == 99:
        plotActualData.append(0)
    else:
        plotActualData.append(int(float(x)))

plotPredictedData = []

k = 0
while (k<40):
    plotPredictedData.append(int(model.predict(30,k)))
    k = k + 1

import matplotlib.pyplot as plt



plt.plot(range(40),plotActualData,label='actual')
plt.plot(range(40),plotPredictedData,label='predicted')
plt.show()



print plotActualData[23]
print plotPredictedData[23]



