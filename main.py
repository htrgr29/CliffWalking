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
POPULATION_SIZE = 100
MOVES_QUANTITY = 18
WIDTH = 12

random.seed(0)
state, info = env.reset()
env.render()

#function for getting random dir
def getRandomDir():
    random.choice(list(Dir))

#function for calculating fitness
def calculateFitness(row, col):
    rowDifference = 3 - row
    colDifference = 12 - col
    return 50 - rowDifference - colDifference

#create initial population
population = [Individual([random.randint(0, 3) for _ in range(MOVES_QUANTITY)], -1, False) for _ in range(POPULATION_SIZE)]

iterator = -1
row = 3
col = 0

for individual in population:
    iterator += 1
    print(str(iterator) + ": ", end="")
    prevCol = 0
    for move in individual.moves:
        state, *_ = env.step(move)
        row = state // WIDTH
        col = state % WIDTH
        print(str(move) + ", ", end="")
        if prevCol != 0 and col == 0 and row == 3:
            individual.fitness = 0
            break
        prevCol = col
    print()
    env.reset()
    if individual.fitness == 0:
        print("individual has fallen")
        continue
    individual.fitness = calculateFitness(row, col)
    print("fitness:" + str(individual.fitness))