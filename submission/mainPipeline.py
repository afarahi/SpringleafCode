
def mainPipeline():

    import sys; import numpy as np
    import numpy.random as npr 
    npr.seed(100)

    print( "READY" )
    
    try: stepNum = int(sys.argv[1])
    except IndexError: sys.exit(-1)

    # Monte Carlo simulation
    if stepNum == 1:
       # Primary pipeline
       from manipulateData import readData
       from model import randomForest
       train = readData('train.csv')
       train.read_data()
       test = readData('test.csv',training=False)
       test.read_data()

       #for i in range(10):
       #print i
       rf = randomForest(train.numLabels,'target',n_estimators=25)
       rf.training(train.data)
       predData = rf.prediction(test.data)
       np.savetxt('./submission/submission_a_20.csv',\
                     predData, delimiter=',', \
                     fmt='%d,%0.2f', header='ID,target')       
       del rf

    elif stepNum == 2:
       # Cross validation
       from manipulateData import readData
       from model import randomForest, extraTrees, adaBoost
       from crossValidation import calcROC
 
       data = readData('train.csv')
       data.read_data()
       labels = data.numLabels
       # divide training set into test and training set for cross validation
       test = data.data[data.data['ID'] < 100000]
       train = data.data[data.data['ID'] > 100000]
       del data
       print test;  print train

       for i in range(20):
          print "Nnmber of estomators:", 10+5*i
          print " Random Forest Classifier:  ",
          rfc = randomForest(labels,'target',n_estimators=10+5*i)
          rfc.training(train)
          predData = rfc.prediction(test)
          calcROC(predData['target'],test['target'])

          print " Extra Trees Classifier:  ",
          etc = extraTrees(labels,'target',n_estimators=10+5*i)
          etc.training(train)
          predData = etc.prediction(test)
          calcROC(predData['target'],test['target'])

          print " Ada Boost Classifier:  ",
          abc = adaBoost(labels,'target',n_estimators=10+5*i)
          abc.training(train)
          predData = abc.prediction(test)
          calcROC(predData['target'],test['target'])

    elif stepNum == 3:

       # Ensembe pipeline
       # Idea 
       #   1. Make prediction
       #   2. Average out predictions

       from manipulateData import readData
       from model import randomForest, extraTrees, adaBoost
       train = readData('train.csv')
       train.read_data()
       test = readData('test.csv',training=False)
       test.read_data()

       prediction1 = np.zeros(test.data.shape[0])
       prediction2 = np.zeros(test.data.shape[0])

       for i in range(3):
          n_estimators = npr.random_integers(30,100)
          print "Number of estimators : ", n_estimators

          rfc = randomForest(train.numLabels,'target',n_estimators=n_estimators)
          rfc.training(train.data)
          predData = rfc.prediction(test.data)
          prediction1 += predData['target']

          etc = extraTrees(train.numLabels,'target',n_estimators=n_estimators)
          etc.training(train.data)
          predData = etc.prediction(test.data)
          prediction2 += predData['target']

          del rfc, etc


       prediction1 /= 3.
       prediction2 /= 3.
       np.savetxt('./submission/submission_a_rf_test.csv',\
                     np.array([predData['ID'],prediction1]).T, delimiter=',', \
                     fmt='%d,%0.2f', header='ID,target', comments='')       
       np.savetxt('./submission/submission_a_et_test.csv',\
                     np.array([predData['ID'],prediction2]).T, delimiter=',', \
                     fmt='%d,%0.2f', header='ID,target', comments='')       

    elif stepNum == 4:
       print( "DONE" )


    # Complete pipeline
    ##################################################################
    #@@@@ STEP 1 [Reading Halos and clusters (1-file at a time)]
    ##################################################################
    #@@@@ STEP 2 [Sorting Halos and clusters]
    ##################################################################
    #@@@@ STEP 3 [Filtering Halos and/or clsters (optional)]
    ##################################################################
    #@@@@ STEP 4 [Matching excersice]
    ##################################################################
    #@@@@ STEP 5 [Primery analysis and making matching output]
    ##################################################################
    #@@@@ STEP 6 [Reading outputs and Stacking]
    ##################################################################
    #@@@@ STEP 7 [Plotting (need to be modified based on stacked version)] 
 
