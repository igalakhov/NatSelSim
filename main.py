#Ivan doesn't know how to write modules, so Ill write the whole thing in one file

#imports
import random as r
import numpy as n
import math as m
import mpmath as np
#settings

start_organisms = 1000 #how many organisms with start with


start_food = 1000 #how much food we start with. Food increases linearlly

delta_food = 100 #by how much food increases each generation

reprSuccess = 2 #startingreproductive success of the organisms, the population will increase when its more than 2, and decrease when its less than two

breedRate = 0.1 #this is the average that will setup the bell curve. If its equal to 0.01, this means that around 1% of all breeding will be outside of either the parent values (if Ivan did his math correctly)

maxGenerations = 100 #total generations we will run the program for

succChange = 0.5 #by how much success will change, the higher this number us, the more the population will be affected by food

encounters = 5 #number of times each organism will encounter a predator per generation in this simulation

bestSize = 10 #size that the predator is best at eating

startSize = 10 #middle of the bell curve of starting size

deviation = 2.5 #deviation of predator bell curve

bestSuccess = 0.1 #the best sucess a predator can have at eating its prey, high values will bacically crash the simulation so I don't reccomend trying those

#globals you shouldn't touch
organisms = []
food = start_food
curCycle = 0
populationOutput = open("output/populations.txt", "w+")
selectionOutput = open("output/selection.txt", "w+")
populationOutput.truncate()
selectionOutput.truncate()
populationOutput.write("Generation, Population, Food \n")
selectionOutput.write("Generation, Average size \n")

#classes

class primCons: #organism one, the one that is being predated and evolves

    def __init__(self, size):
        self.size = size
        self.fitness = 0

    def sayName(self):
        pass

def prepareSim(): #this function prepares the simulation
    for i in range(start_organisms):
        curOrganism = primCons(10 + n.random.normal())
        organisms.append(curOrganism)

def breedSpecific(org1, org2): #this function breeds two specific organisms and returns an array of new organisms
    global reprSuccess, breedRate

    output = []

    size1 = org1.size
    size2 = org2.size

    probabilities = [1] * m.floor(reprSuccess)

    if(reprSuccess % 1 != 0):
        probabilities.append(reprSuccess % 1)

    avg = (size1 + size2)/2

    #we will arange the bell curve such that there is a 1% chance of getting a value higher or lower

    stDiv = (((1 + (breedRate * 2)) * abs(size1 - size2)) * 0.997)/6



    for p in probabilities:
        if(r.random() < p):
            output.append(primCons(avg + n.random.normal(0, stDiv) + r.random()/100))

    return output

def breedOrganisms(): #this function breeds the organisms
    global organisms

    orgCop = organisms

    nextGeneration = []

    split1 = [] #"males" - although we don't really care
    split2 = [] #"females" - again, irrelevant

    #find the split, and see if we should pop
    split = m.floor(len(orgCop)/2)

    #divide our current generation into two random parts
    if(len(orgCop) % 2 == 1):
        orgCop.sort(key=lambda x: (x.size, x.fitness), reverse=True)
        orgCop.pop()

    n.random.shuffle(orgCop)
    split1 = orgCop[0 : split]
    split2 = orgCop[split:]

    split1.sort(key=lambda x: x.size, reverse = True)
    split2.sort(key=lambda x: x.size, reverse = True)

    #now we have 2 splits, so we will breed these an
    for i in range(len(split1)):
        addition = breedSpecific(split1[i], split2[i])
        nextGeneration += addition

    return nextGeneration
#main
def doFood(): #this function will get the food for the next generation
    global food, delta_food
    return food + delta_food
def doRepSucc(): #this funciton give us a new, updated reproductive success
    global food, organisms, reprSuccess, succChange
    curPopulation = len(organisms)
    ratio = food/curPopulation

    if(ratio < 1):
        output = reprSuccess * m.tan(((ratio - 1)*m.pi)/4)
        #print(output)
        return reprSuccess + output*succChange*3
    else:
        slop = reprSuccess * m.pow(np.sec(m.pi/-4), 2) * (m.pi/4)
        output = slop * (ratio - 2) + reprSuccess
        #print(output)
        return reprSuccess + output*succChange
def doEncounters():
    global encounters, organisms
    for i in range(encounters):
        toDelete = [] #indexes we will delete
        for j in range(len(organisms)):
            curSize = organisms[j].size
            prob = doBellCurve(curSize)
            if(r.random() < prob):
                toDelete.append(j)
            else:
                organisms[j].fitness += 1

        organisms = removeIndexes(organisms, toDelete)

def doBellCurve(size):
    global bestSize, deviation
    part1 = (1/(deviation*pow((2*m.pi),0.5)))
    part2 = pow(m.e,(-1*(pow((size - bestSize), 2)/(2*pow(deviation, 2)))))
    output = part1*part2*deviation

    output /= 0.39894228040143276

    output *= bestSuccess

    return output

def doGeneration(): #calls multiple functions in order so I don't have to do everything in the main loop
    global organisms, food, reprSuccess, curCycle
    doEncounters()
    organisms = breedOrganisms()
    food = doFood()
    reprSuccess = doRepSucc()
    curCycle += 1
def logData(): #logs the data to the output folder
    global populationOutput
    populationOutput.write(str(curCycle) + ", " + str(len(organisms)) + ", " + str(food) + "\n")
    values = []
    for i in organisms:
        values.append(i.size)
    selectionOutput.write(str(curCycle) + ", " + str(mean(values)) + "\n")

def removeIndexes(inPut, toRemove):
    copy = inPut
    toRemove.sort()
    for i in reversed(toRemove):
        del copy[i]
    return copy
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def main():
    global organisms
    #prepare the simulation
    prepareSim()
    #do the set amount of generations
    for i in range(maxGenerations):
        doGeneration()
        logData()


if __name__ == "__main__": #so we don't get bamboozled by a module
    main()
    pass
