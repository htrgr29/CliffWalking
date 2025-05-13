import random
import sys

import gymnasium as gym
from enum import IntEnum
from inidvidual import Individual

#enum for directions
class Dir(IntEnum):
    UP = 0
    DOWN = 2
    LEFT = 3
    RIGHT = 1

#init gymnasium CliffWalking
env = gym.make("CliffWalking-v0", render_mode=None)

#variable declaration
POPULATION_SIZE = 100
MOVES_QUANTITY = 18
WIDTH = 12

random.seed(0)
state, info = env.reset()
env.render()

#function for getting random dir
def getRandomDir():
    random.choice(list(Dir))

#function for getting random moves sequence
def genRandMovesSequence():
    return [random.randint(0, 3) for _ in range(MOVES_QUANTITY)]

#function for checking if the individual has fallen
def didFall(i: Individual):
    if i.prevCol != 0 and i.col == 0 and i.row == 3:
        return True
    else:
        return False

#function for printing individual's move sequence
def printMoves(i: Individual):
    for m in i.moves:
        print(str(m) + ", ", end="")

#function for calculating fitness
def calculateFitness(i: Individual):
    rowDifference = 3 - i.row
    colDifference = 11 - i.col
    return 20 - rowDifference - colDifference

#function for crossover
def crossover(p:list[Individual]):
    probabilityArray = rouletteSelArray(p)
    newPopulation: list[Individual] = []
    bestIndividualCount = round(POPULATION_SIZE * 0.05)
    for i in range(POPULATION_SIZE - bestIndividualCount):
        parent1: Individual = random.choice(probabilityArray)
        parent2 = random.choice(probabilityArray)
        childMoves: list[int] = []
        for m in range(MOVES_QUANTITY):
            if m < MOVES_QUANTITY/2:
                childMoves.append(parent1.moves[m])
            else:
                childMoves.append(parent2.moves[m])
        child = Individual(childMoves)
        newPopulation.append(child)

    bestIndividuals = findBestIndividuals(p)
    newPopulation.extend(bestIndividuals)

    return newPopulation

#function for finding best 5% of population
def findBestIndividuals(p: list[Individual]):
    sortedPopulation = sorted(p, key=lambda i: i.fitness, reverse=True)
    topCount = int(POPULATION_SIZE * 0.05)

    return sortedPopulation[:topCount]

#function for mutation
def mutate(p: list[Individual]):
    for i in p:
        for index, _ in enumerate(i.moves):
            if random.random() < 0.05:
                i.moves[index] = random.randint(0, 3)

#function for creating array for roulette selection
def rouletteSelArray(p:list[Individual]):
    probabilityArray: list[Individual] = []
    index = 0
    for i in p:
        for j in range(i.fitness):
            probabilityArray.append(i)
            # print(str(index) + ", ", end="")
        index += 1
    return probabilityArray

#create initial population
population = [Individual(genRandMovesSequence()) for _ in range(POPULATION_SIZE)]

reachedGoal = False
populationId = -1

while not reachedGoal:
    populationId += 1
    bestFitness = 0
    iterator = -1
    for individual in population:
        iterator += 1
        # print(str(iterator) + ": ", end="")
        for move in individual.moves:
            state, *_ = env.step(move)
            individual.setPos(state)
            # print(str(move) + ", ", end="")
            if didFall(individual):
                individual.fitness = 0
                break
            individual.prevCol = individual.col

        # print()
        env.reset()
        if individual.fitness == 0:
            # print("individual has fallen")
            continue
        individual.fitness = calculateFitness(individual)
        if individual.fitness == 20:
            reachedGoal = True
            print("individual has won! his steps:")
            for move in individual.moves:
                print(str(move) + ", ", end="")
        if individual.fitness > bestFitness:
            bestFitness = individual.fitness
        #print("fitness:" + str(individual.fitness))

    np = crossover(population)
    population = np
    mutate(population)
    print("population: ", populationId, "best fitness: ", bestFitness)