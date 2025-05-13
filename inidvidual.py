import random


class Individual:
    def __init__(self, moves, fitness=-1, reached_goal=False, col=0, row=3, prevCol=0):
        self.moves = moves
        self.fitness = fitness
        self.reached_goal = reached_goal
        self.col = col
        self.row = row
        self.prevCol = prevCol

    def setPos(self, state):
        self.col = state % 12
        self.row = state // 12