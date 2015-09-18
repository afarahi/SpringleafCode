#Supper Parameters
tSlopeYX = 1.35; tSlopeZX = 1.29
tSigYX  = 0.2; tSigZX = 0.35
tIntYX  = -0.5;  tIntZX = -0.8
xObsSig = 0.2;   yObsSig = 0.2; zObsSig = 0.00001
rYZ = 0.0

beta1 = -0.5; beta2 = 0.7

cutOnY = True; cutOnZ = False

ndata = 40000; xmin = -8.0; xmax = 500.0
yCutmin = -2.#-.5 #7.5 #tIntYX + tSlopeYX*xmin + 3.5*tSigYX
yCutmax = tIntYX + tSlopeYX*xmax - 3.5*tSigYX
zCutmin = tIntZX + tSlopeZX*xmin + 3.5*tSigZX
zCutmax = tIntZX + tSlopeZX*xmax - 3.5*tSigZX

if (beta2 <= 0.):
   print "Warrning: the code is not working for beta2 <= 0"; exit(1) 

