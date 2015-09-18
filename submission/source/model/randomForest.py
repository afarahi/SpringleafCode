from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

class randomForest:

   def __init__(self,predictorsLabel,targetLabel='target',n_estimators=5):
      self.predictorsLabel = predictorsLabel
      self.targetLabel = targetLabel
      self.RFC = RandomForestClassifier(n_estimators)

   def training(self,trainingData,n_estimators=5):
      target = trainingData[self.targetLabel]
      train = pd.DataFrame(trainingData, columns=self.predictorsLabel)
      train = train.replace(np.nan,-1.0) 
      self.RFC.fit(train,target)
 
   def prediction(self,predictionData):
      test = pd.DataFrame(predictionData, columns=self.predictorsLabel)
      test = test.replace(np.nan,-1.0) 
      predTarget = self.RFC.predict(test)
      pred = pd.DataFrame(np.array([test['ID'],predTarget]).T,\
                          columns=["ID","target"])
      return pred



