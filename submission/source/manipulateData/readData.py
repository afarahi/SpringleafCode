import pandas as pd
import numpy as np
import sys

class readData:

   def __init__(self,fname='None',training=True):
      fdir = './inputData/'
      self.fname = fdir + fname
      self.training = training
      print "Initaializaed"

   def read_data(self,numRows=10):
      self.data = pd.read_csv(self.fname)
      self.labels = self.data.axes[1]
      self.floatLabels = self.data.select_dtypes(include=['float']).axes[1]
      self.intLabels = self.data.select_dtypes(include=['int']).axes[1]
      self.numLabels = self.data.select_dtypes(include=['int','float']).axes[1]
      if (self.training):
         maskOne  = self.data['target'] == 1
         maskZero = self.data['target'] == 0
         self.data1 = self.data[maskOne] 
         self.data0 = self.data[maskZero] 
        
   def missingData(self,label,value):
      self.data1[label].replace(value,np.nan) 
      self.data0[label].replace(value,np.nan) 

   def printData(self,numRows=10):
       print "OK"

   def generateHistograms(self):
      import matplotlib.pylab as plt
      for labe in self.labels[1:]:
         for labe2 in self.labels[1:]:
 
            print labe,labe2
            try:
               plt.figure()
               plt.clf()
               plt.plot(np.log10(self.data0[labe]+1.0),\
                        np.log10(self.data0[labe2]+1.0),\
                        'r.',alpha=0.2)
               plt.plot(np.log10(self.data1[labe]+1.0),\
                        np.log10(self.data1[labe2]+1.0),\
                        'b.',alpha=0.2)
               plt.xlabel(labe)
               plt.ylabel(labe2)
               plt.savefig('./plots/'+labe+'_'+labe2+'.png')
               plt.close()
            except: pass
