import numpy as np
import matplotlib.pyplot as pl

x=np.array([1,2,3,4,5,6,7,8,9,10])
y=np.array([2,4,6,8,10,12,14,16,18,20])
pl.plot(x,y)

z=np.array([0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0])
pl.plot(x,z)


pl.show()