import numpy as np
import matplotlib.pyplot as plt
import math

"""
Lakota Dolce
Lab 2
"""
#Title and label variables
title = "Charge of a Capacitor over Time"
horizontal="Time (t)"
vertical = "Charge (q)"
gridTF = True
fsize = 20 #Font size
lwidth = 1; #line width
lstyle = "solid" #line style
lcolor = "black" #line color
llabel = "Charge as a Function over Time" 
start = 0
stop = .5
accuracy = 100

#Function
t = np.linspace(start,stop, accuracy) #(start, stop, # of points)
ft = 10*(np.exp(-(50*t)/(2*5)))*(np.cos(math.sqrt((1/(5*(10**-4)))-(50/(2*5))**2) * t))
#Note
# x = np.arange(start,stop,accuracy) #(start, stop, gap)
#e^x = np.exp(x) e^(2x) = np.exp(2*x)
#cos() = np.cos() sin() = np.sin()


#Plotting
plt.plot(t,ft, linestyle = lstyle, linewidth = lwidth, label = llabel, color = lcolor)
plt.title(title,fontsize = fsize)   
plt.xlabel(horizontal)
plt.ylabel(vertical)
plt.legend() 
plt.grid(gridTF)
plt.show()