
def mainPipeline():

    import sys; import numpy as np
 
    print( "READY" )
    
    try: stepNum = int(sys.argv[1])
    except IndexError: sys.exit(-1)

    # Monte Carlo simulation
    if stepNum == 1:
       # ARYA's pipeline
       from manipulateData import readData
       from model import randomForest
       train = readData('train.csv')
       train.read_data()
       test = readData('test.csv',training=False)
       test.read_data()

       for i in range(10):
          print i
          rf = randomForest(train.numLabels,'target',n_estimators=(10+i))
          rf.training(train.data)
          predData = rf.prediction(test.data)
          np.savetxt('./submission/submission_a_%i.csv'%i,\
                     predData, delimiter=',', \
                     fmt='%d,%0.2f', header='ID,target')       
          del rf
    elif stepNum == 2:
       pass
    elif stepNum == 3:
       print( "TEST IS DONE" )
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
 
