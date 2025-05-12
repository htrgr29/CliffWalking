import random

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
env = gym.make("CliffWalking-v0", render_mode="human")

#variable declaration
POPULATION_SIZE = 150
MOVES_QUANTITY = 18
WIDTH = 12

random.seed(0)
state, info = env.reset()
env.render()

#function for getting random dir
def getRandomDir():
    random.choice(list(Dir))

#function for calculating fitness
def calculateFitness(row, col, movesCount):
    rowDifference = 3 - row
    colDifference = 12 - col
    return 50 - rowDifference - colDifference - movesCount

#create initial population
population = [Individual([random.randint(0, 3) for _ in range(MOVES_QUANTITY)], -1, False) for _ in range(POPULATION_SIZE)]

iterator = -1
movesCount = 0

row = 3
col = 0

for individual in population:
    iterator += 1
    print(str(iterator) + ": ", end="")
    for move in individual.moves:
        movesCount += 1
        state, *_ = env.step(move)
        row = state // WIDTH
        col = state % WIDTH
        print(str(move) + ", ", end="")
    print()
    individual.fitness = calculateFitness(row, col, movesCount)
    print("fitness:" + str(individual.fitness))
    env.reset()
    movesCount = 0