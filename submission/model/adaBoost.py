from sklearn.ensemble import AdaBoostClassifier
import pandas as pd
import numpy as np

class adaBoost:

   def __init__(self,predictorsLabel,targetLabel='target',n_estimators=5):
      self.predictorsLabel = predictorsLabel
      self.targetLabel = targetLabel
      self.ABC = AdaBoostClassifier(n_estimators=n_estimators)

   def training(self,trainingData,n_estimators=5):
      target = trainingData[self.targetLabel]
      train = pd.DataFrame(trainingData, columns=self.predictorsLabel)
      train = train.replace(np.nan,-1.0) 
      self.ABC.fit(train,target)
 
   def prediction(self,predictionData):
      test = pd.DataFrame(predictionData, columns=self.predictorsLabel)
      test = test.replace(np.nan,-1.0) 
      predTarget = self.ABC.predict(test)
      pred = pd.DataFrame(np.array([test['ID'],predTarget]).T,\
                          columns=["ID","target"])
      return pred



