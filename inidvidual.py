import random


class Individual:
    def __init__(self, moves, fitness, reached_goal):
        self.moves = moves
        self.fitness = fitness
        self.reached_goal = reached_goal