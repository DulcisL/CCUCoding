from math import *

#Set the zero
zero = 100
#Set range
r = 1000
#Set Coefficient
c = .451
#Set initial velocity (fps to m/s)
Vo = 2510 * 3.281
#Set line of sight (inches to m/s)
los = 1.5 / 39.37
#Set gravity
g = 9.8
#Set air pressure
p = 1.225
#Set mass / (convert to kg)
m = 185 / 15430
#set bullet area (.308)
Ab = 4.8 * 10**-5

#Calculate the adjacent (hypotenuse)
H = sqrt(zero**2 - los**2)

#Calculate Velocity in x and y direction
Vx = Vo * cos(zero/H)
Vy = Vo * sin(los/H)

#time step 
t = .001
x = 0
y = 0
dt = 0

while x <= r:
    #Calculate drag
    Fd = .5 * p * c * Ab * Vx **2

    #Calculate acceleration
    Ax = -Fd/m
    Ay = -g - Fd/m

    #update velocity
    Vx += Ax * t
    Vy+= Ay * t

    #update Position
    x += Vx * t
    y += Vy * t

    dt += t

drop = round(((((Vy * t) - ((1/2) * g * t**2)) - ((c * p * Ab * Vy**2 * t**2) / 2)))* 39.37, 1)
print(dt)
print(round(y * 39.37, 1))
print(drop)