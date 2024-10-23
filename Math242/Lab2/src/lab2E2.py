import numpy as np
import matplotlib.pyplot as plt
import math

"""
Lakota Dolce
Lab 2
"""
#Title and label variables
title = "Comparing Functions"
horizontal="X"
vertical = "Y"
gridTF = True
fsize = 20 #Font size
lwidth = 1; #line width
lstyle = "solid" #line style
lstyle2 = "dashed" #line style
lstyle3 = "dotted" #line style
lcolor = "red" #line color
lcolor2 = "green" #line color
lcolor3 = "blue" #line color
llabel = "e^(x)" 
llabel2 = "-e^(-x)"
llabel3 = "e^(-x) * cos(6x)"  
start = 0
stop = 5
accuracy = 100

#Function
x = np.linspace(start,stop, accuracy) #(start, stop, # of points)
y = np.exp(-x)
y2 = -np.exp(-x)
y3 = np.exp(-x) * np.cos(6*x)
#Note
# x = np.arange(start,stop,accuracy) #(start, stop, gap)
#e^x = np.exp(x) e^(2x) = np.exp(2*x)
#cos() = np.cos() sin() = np.sin()


#Plotting
plt.plot(x,y, linestyle = lstyle, linewidth = lwidth, label = llabel, color = lcolor)
plt.plot(x,y2, linestyle = lstyle2, linewidth = lwidth, label = llabel2, color = lcolor2)
plt.plot(x,y3, linestyle = lstyle3, linewidth = lwidth, label = llabel3, color = lcolor3)
plt.title(title,fontsize = fsize)   
plt.xlabel(horizontal)
plt.ylabel(vertical)
plt.legend() 
plt.grid(gridTF)
plt.show()