import numpy as np
import matplotlib.pyplot as plt
import math

"""
Lakota Dolce
Lab 2
"""
#Title and label variables
title = "Photodegredation of Aqueos Bromine"
horizontal="Concentration (c)"
vertical = "Time (t)"
gridTF = True
fsize = 20 #Font size
lwidth = 1; #line width
lstyle = "dotted" #line style
lcolor = "blue" #line color
llabel = "Concentration curve"
llabel2 = "Concentration Data"   
start = 10
stop = 70
accuracy = 100
gap = 10

#Function
#t = np.linspace(start,stop, accuracy) #(start, stop, # of points)
t = np.arange(start, stop, gap) #(start, stop, gap)
y = 4.84 * (np.exp(-.034*t))
y2 = [3.4, 2.6, 1.6, 1.3, 1, .5]

#Note
#e^x = np.exp(x), e^(2x) = np.exp(2*x)
#cos() = np.cos(), sin() = np.sin()


#Plotting
plt.plot(t,y, linestyle = lstyle, linewidth = lwidth, label = llabel, color = lcolor)
plt.plot(t,y2, "*")
plt.title(title,fontsize = fsize)   
plt.xlabel(horizontal)
plt.ylabel(vertical)
plt.legend() 
plt.grid(gridTF)
plt.show()