from scipy import integrate

def f(x, y, z):  return x*y*z

print(integrate.tplquad(f, 0, 1,\
                     lambda x:0, lambda x:1,\
                     lambda x,y:0, lambda x,y:1 ))
#(0.010416666666666668, 4.101620128472366e-16)
print(integrate.nquad(f, [[0.0,1.0],[0.0,1],[0,1]] ))

