"""
Lakota Dolce
Project 1
October 8, 2024
Dr. Debendra
"""
#Libraries needed
import numpy as np
import matplotlib.pyplot as plt
import math
#Classes
"""
Class Person: Params(float Weight, string Gender, float FAC)
Attributes:
    float Weight
    float FluidVolume
    string Gender
    float FAC
Functions:
getters / setters for attributes
ToString
"""
class Person:
    #Constructor
    def __init__ (self, WeightIn, GenderIn):
        #Attributes
        self._Weight = WeightIn
        self._Gender = GenderIn
        self._FluidVolume = self.setFluidVolume()
        self._FAC = self.setFAC(0.00)
        
    #Getters
    def getWeight (self):
        return self._Weight
    
    def getFluidVolume (self):
        return self._FluidVolume
    
    def getGender (self):
        return self._Gender
    
    def getFAC(self):
        return self._FAC
    
    #Setters
    def setWeight(self, newWeight):
        self._Weight = round(newWeight, 2)
        return round(newWeight,2)

    def setFluidVolume(self):
        volume = 0
        if self.getGender() == "f":
            #Calculate
            volume = (self.getWeight() * .65)
        if self.getGender() == "m":
            #Calculate
            volume = (self.getWeight() * .68)
        self._FluidVolume = volume
        return volume

    def setGender (self, newGender):
        self._Gender = newGender
        self.setFluidVolume()
        return newGender
    
    def setFAC (self, newFAC):
        self._FAC = newFAC
        return newFAC
        
    
    #Supplemental Functions

    """
    function EliminationRate: determines the elimination of alcohol over time in the fluid
    Param -> int time - holds the time the alcohol was newFAC over in hours
    *Note* Average person eliminates 12g alcohol /hr
    Return -> average intake
    """
    def EliminationRate(self, step):
        #previous FAC - FAC lost (~12g/hr)
        newFAC = self.getFAC() - (12 / self.getFluidVolume() * step)
        newFAC = round(newFAC,6)
        self.setFAC(newFAC)
        #Return the calculated elimination rate
        return newFAC
    
    """
    function FACCalculator: Calculate the fluid alcohol content
    Param -> float intake - Alcohol intake
    Param -> person Person - person object containing info on person
    *Note* Legal driving limit in SC is .08% FAC (.08g /100ml)
    *Note* 4g/ml Alcohol results in a coma
    *Note* 4.5-5g/ml Alcohol results in death
    Return -> FAC of person
    """
    def FACCalculator (self, intake):
        #Calculate gram of alcohol / Fluid volume
        FAC = round(self.getFAC() + (intake / self.getFluidVolume()),6)
        #Set new FAC
        self.setFAC(FAC)
        return FAC

    #ToString
    def __str__ (self):
        return f"""Person ({self.getGender()})->
Weight: {self.getWeight()}kg 
Body Fluid Volume: {self.getFluidVolume()}ml
Fluid Alcohol Content: {round(self.getFAC(), 3)}g/ml
"""


#Main
"""
function main: Used to organize and call needed functions
Params -> None
Return -> int for success or fail
"""
def main():
    #initialize variables
    weight1 = 70
    weight2 = 130
    gender1 = "m"
    gender2 = "f"
    units1 = "kg"
    units2 = "lbs"

    #Convert to needed units
    weight1, units1 = weightConversion(weight1, units1)
    weight2, units2 = weightConversion(weight2, units2)

    #Create person object and calculate the fluid Volume
    personM1 = Person(weight1, gender1)
    personF1 = Person(weight2, gender2)

    #Call function for question 1
    questionOne(personM1)

    #Call function for question 2
    questionTwo(personM1)

    #Call function for question 3
    questionThree(personM1)


    
#Functions
"""
function weightConversion: Converts units from pounds to kg
Param -> int weight - stores weight of person
Param -> string units - stores the units of measurement
Return -> weight, units after conversion to kgs
"""
def weightConversion(weight, units):
    if units == "lbs":
        #Convert pound to kilograms
        weight = weight / 2.2046
        units = "kg"
    #Keep kg the same
    if units == "kg":
        weight = weight
    #Round to 2 decimals
    return round(weight, 2), units

"""
function Graphing: Graphs the points over time for the problem
Param -> npArray pointsY - stores Y values
Param -> npArray pointsX - stores X values
Return -> None
"""
def Graphing(pointsX, pointsY):
    #Title and label variables
    title = "Fluid Alcohol Content over time (t)"
    horizontal="Time"
    vertical = "Alcohol Content"
    gridTF = True
    fsize = 20 #Font size
    lwidth = 1; #line width
    lstyle = "solid" #line style
    lcolor = "" #line color
    llabel = "Alcohol Content" 
    start = 0
    stop = .5
    accuracy = 100

    #Plotting
    plt.plot(pointsX, pointsY, linestyle = lstyle, linewidth = lwidth, label = llabel)
    plt.title(title,fontsize = fsize)   
    plt.xlabel(horizontal)
    plt.ylabel(vertical)
    plt.axhline(y=0.08, color='green', linestyle='--', label='Legal Driving Limit')
    plt.axhline(y=4.0, color='orange', linestyle='--', label='Coma')
    plt.axhline(y=4.5, color='red', linestyle='--', label='Death')
    plt.legend() 
    plt.grid(gridTF)
    plt.show()

#Questions Coding
def questionOne(person):
    """
    Question 1
    Assume your hypothetical person arrives at a party and instantaneously downs a six-pack of
    beer. Graph alcohol concentration as a function of time.
    """
    #Initialize
    pointsY = []
    pointsX = []
    time = 0
    step = .25

    #Regular beer is 13.6g of alcohol
    #drinks 6 instantaneosly
    intake = 6 * 13.6

    #Calculate the initial FAC
    person.FACCalculator(intake)

    #Calculate the elimination of alcohol over time (hrs)
    while (round(person.getFAC(), 3) > 0):
         #Add points to array
        if (round(time , 6) != 0):
            pointsY.append(person.EliminationRate(step))
        if (time == 0):
            pointsY.append(person.getFAC())
        pointsX.append(time)
        time += step
        #Check if an error occurred
        if (time > math.ceil((6*13.6)/12)+ 1 ):
            print("An error occurred (Exceeded expected time to eliminate alcohol consuption)")
            break

    #Graph the FAC over time
    Graphing(np.array(pointsX), np.array(pointsY))

def questionTwo(person):
    """
    Question 2
    Construct a more realistic manner of consuming six beers. One of many cases could be that
    the hypothetical person drinks drinks two beer cans and waits for 10 minutes, drinks another
    set etc.
    """
    #Initialize
    pointsY = []
    pointsX = []
    beerCounter = 2
    time = 0
    step = .25
    #drinks 2 beers imediately
    intake = 2 * 13.6

    #Calculate the initial FAC
    person.FACCalculator(intake)

    #Calculate the elimination of alcohol over time (hrs)
    while (round(person.getFAC(), 3) > 0):
        # drinks 1 beer after every 15 minutes
        if(beerCounter < 6 and (time %.25) == 0):
            person.FACCalculator(13.6)
            beerCounter += 1
    
        #Add points to array
        if (time != 0 ):
            pointsY.append(person.EliminationRate(step))
        if (time == 0):
            pointsY.append(person.getFAC())
        pointsX.append(time)
        #increase time by 15 minutes after initial drinks
        time += step
        #Check if an error occurred
        if (time > math.ceil((6*13.6)/12) + 1):
            print("An error occurred (Exceeded expected time to eliminate alcohol consuption)")
            break

    #Graph the FAC over time
    Graphing(np.array(pointsX), np.array(pointsY))

def questionThree(person):
    """
    Question 3
    Try some other alcohol input functions. Here is one idea: the hypothetical person drinks 2
    beers, and after 15 minutes he drinks 3 oz of 100-proof vodka. After 20 minutes drinks more
    (pick something realistic).
    """
    #Initialize
    pointsY = []
    pointsX = []
    time = 0
    step = .05
    beerCounter = 2
    #Drinks 2 beer immediately
    intake = 2 * 13.6

    #Calculate the initial FAC
    person.FACCalculator(intake)

    #Calculate the elimination of alcohol over time (hrs)
    while (round(person.getFAC(), 3) > 0):
        # drinks double shot (3oz 100 proof vodka) after 15 minutes
        if (time == .25):
            person.FACCalculator((2 * 16.7))
        if (time > .25 and beerCounter < 6): 
            #drinks a beer every ~20 minutes after shots
            if ((time % .3) == 0):   
                #drinks a beer every 15 minutes after until they have drank 6
                person.FACCalculator(13.6)
        #Add points to array
        if (time != 0 ):
            pointsY.append(person.EliminationRate(step))
        if (time == 0):
            pointsY.append(person.getFAC())
        pointsX.append(time)
        #increase time by 3 minutes after initial drinks
        time += step
        #Check if an error occurred
        if (time > (math.ceil(6*13.6 + 2*16.7)/12)+ 1):
            print("An error occurred (Exceeded expected time to eliminate alcohol consuption)")
            break

    #Graph the FAC over time
    Graphing(np.array(pointsX), np.array(pointsY))

#Begin the program
main()