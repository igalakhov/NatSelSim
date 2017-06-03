#Ivan doesn't know how to write modules, so Ill write the whole thing in one file

#imports
import random as r
import operator as op
import numpy as n
import math as m

#settings

start_organisms = 1000 #how many organisms with start with

start_food = 20 #how much food we start with. Food increases linearlly

delta_food = 1 #by how much food increases each generation

reprSuccess = 2.1 #reproductive success of the organisms, the population will increase when its more than 2, and decrease when its less than two

breedRate = 0.01 #this is the average that will setup the bell curve. If its equal to 0.01, this means that around 1% of all breeding will be outside of either the parent values (if Ivan did his math correctly)

maxGenerations = 10 #total generations we will run the program for

#globals you shouldn't touch
organisms = []
food = start_food

#classes

class primCons: #organism one, the one that is being predated and evolves

    def __init__(self, size):
        self.size = size

    def sayName(self):
        pass

class predator: #this is the predator, the one that feeds on the primary consumer

    def __init__(self):
        pass

    def testFunc(self):
        pass

#functions
def prepareSim(): #this function prepares the simulation
    for i in range(start_organisms):
        curOrganism = primCons(n.random.randint(0, 10))
        organisms.append(curOrganism)

def breedSpecific(org1, org2): #this function breeds two specific organisms and returns an array of new organisms
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

    orgCop = organisms

    nextGeneration = []

    split1 = [] #"males" - although we don't really care
    split2 = [] #"females" - again, irrelevant

    #find the split, and see if we should pop
    split = m.floor(len(orgCop)/2)

    #divide our current generation into two random parts
    if(len(orgCop) % 2 == 1):
        orgCop.sort(key=lambda x: x.size, reverse=True)
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
def main():
    global organisms
    #prepare the simulation
    prepareSim()

    #do the set amount of generations
    for i in range(maxGenerations):
        organisms  = breedOrganisms()
        print(len(organisms))



main()