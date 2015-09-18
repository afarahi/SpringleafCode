import numpy as np
import numpy.random as npr
import pyfits
import os


def generateSampleData():
   npr.seed(1)

   from model import selectionFunctionClass
   sf = selectionFunctionClass()

   print( "TEST IS DONE" )

   h = pyfits.open('sample/XCAT_Aardvark_1.0_100.fit')[1].data
 
   Tobs = [];  Lxobs = []; Z = []; M500 = []
   Tobs_err = []; Lxobs_err = []

   print max(h['RA']), min(h['RA'])
   print max(h['DEC']), min(h['DEC'])

   counter = 0
   for i in range(len(h)):
      if sf.selectionFunction(h['Lx'][i], h['T'][i], h['Z'][i]) > npr.random() :
         counter += 1
         print counter, h['M500'][i], h['T'][i], h['Lx'][i], h['Z'][i]
         Tobs.append(h['T'][i])
         Lxobs.append(h['Lx'][i])
         Z.append(h['Z'][i])
         M500.append(h['M500'][i])

   fdir = './sample/observationTest.fit'
   print "Removing old halo catalog (if exist) :", fdir
   os.system('rm %s'%fdir)
   print "Saving new halo catalog :", fdir

   hdr =  pyfits.Header()      
   PrimaryHDUList = np.arange(1)
   # HALOS INFO
   T = np.array(Tobs)
   Lx= np.array(Lxobs)
   Z = np.array(Z)
   M500 = np.array(M500)
   col1 = pyfits.Column(name='Z', format='E', array=Z)
   col2 = pyfits.Column(name='lgT', unit='keV', format='E', array=T)
   col3 = pyfits.Column(name='lgLx', unit='1e44 ergs/s', format='E', array=Lx)
   col4 = pyfits.Column(name='M500', unit='Msun/h', format='E', array=M500)
   cols = pyfits.ColDefs([col1, col2, col3, col4])
 
   hdu = pyfits.PrimaryHDU(data=PrimaryHDUList,header=hdr)
   tbhdu_halo = pyfits.BinTableHDU.from_columns(cols)
   thdulist = pyfits.HDUList([hdu, tbhdu_halo]) 
   thdulist.writeto(fdir)

   print "DONE"
   
   #import matplotlib.pylab as plt
   #plt.hist(Z, bins= 12, range=(0.0,1.2) )
   #plt.xlabel('Z'); plt.ylabel('N')
   #plt.savefig('z-dist.png')


