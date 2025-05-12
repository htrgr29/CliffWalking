import random

import gymnasium as gym
from enum import IntEnum
from inidvidual import Individual

class Dir(IntEnum):
    UP = 0
    DOWN = 2
    LEFT = 3
    RIGHT = 1

env = gym.make("CliffWalking-v0", render_mode="human")
observation, info = env.reset()
env.render()

#function for getting random dir
def getRandomDir():
    random.choice(list(Dir))

#create initial population
population = [Individual([random.randint(0, 3) for _ in range(18)], 0, False) for _ in range(150)]

iterator = -1

for i in population:
    iterator += 1
    print()
    print(str(iterator) + ": ", end="")
    for j in i.moves:
        print(str(j) + ", ", end="")

env.step(Dir.UP)
env.step(Dir.RIGHT)

env.action_space.seed(0)