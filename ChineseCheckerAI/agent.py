import random

class Agent(object):
    def getAction(self, state):
        raise Exception("Not implemented yet")

class SimpleGreedyAgent(Agent):
    def __init__(self, game):
        self.game = game
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if action[1][0] - action[0][0] == max_vertical_advance_one_step]
        return random.choice(max_actions)

class RandomAgent(Agent):
    def __init__(self, game):
        self.game = game
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        return random.choice(legal_actions)
