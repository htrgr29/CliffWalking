import os
import random
import sys
import time
import json

import gymnasium as gym
from enum import IntEnum

import numpy as np

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
MOVES_QUANTITY = 21
WIDTH = 12
FILENAME = 'data.json'
SEED = 0

rng = np.random.default_rng(seed = SEED)
state, info = env.reset()
env.render()

#function for getting random dir
def getRandomDir():
    rng.integers(0, 4)

#function for getting random moves sequence
def genRandMovesSequence():
    return rng.integers(0, 4, size = MOVES_QUANTITY).tolist()

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
        parent1: Individual = rng.choice(probabilityArray)
        parent2 = rng.choice(probabilityArray)
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
        for index, currentMove in enumerate(i.moves):
            if rng.random() < 0.05:
                possibleMoves = [m for m in range(4) if m != currentMove]
                i.moves[index] = rng.choice(possibleMoves)

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

#function for displaying invidual's move sequence
def showMoves(i: Individual):
    env1 = gym.make("CliffWalking-v0", render_mode="human")
    _, info1 = env1.reset()
    for move1 in i.moves:
        state1, *_ = env1.step(move1)
    time.sleep(2)
    env1.close()

#function for appending data to .json file
def saveToJSON(i: Individual, pp: int):
    new_data = {
        "population": pp,
        "best fitness": i.fitness,
        "move combination": i.moves,
    }
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_data)
    with open(FILENAME, "w") as f:
        json.dump(data, f)

    print("Saved to " + FILENAME)

#function to remove old data.json file
def removeOldDataFile():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

#create initial population
population = [Individual(genRandMovesSequence()) for _ in range(POPULATION_SIZE)]

#clear old data file
removeOldDataFile()

#set up main loop variables
reachedGoal = False
populationId = -1

while not reachedGoal:
    populationId += 1
    bestIndividual = population[0]
    iterator = -1
    for individual in population:
        iterator += 1
        for move in individual.moves:
            state, *_ = env.step(move)
            individual.setPos(state)
            if didFall(individual):
                individual.fitness = 0
                break
            individual.prevCol = individual.col

        env.reset()
        if individual.fitness == 0:
            continue
        individual.fitness = calculateFitness(individual)
        if individual.fitness == 20:
            reachedGoal = True
            saveToJSON(individual, populationId)
            print("individual has won!")
            time.sleep(2)
            showMoves(individual)
            sys.exit()
        if individual.fitness > bestIndividual.fitness:
            bestIndividual = individual

    np = crossover(population)
    population = np
    mutate(population)
    saveToJSON(bestIndividual, populationId)