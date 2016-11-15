import random, re

class Agent(object):
    def __init__(self, game):
        self.game = game
    def getAction(self, state):
        raise Exception("Not implemented yet")

class HumanAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        print 'legal actions are:', legal_actions
        while True:
            print 'enter your action:'
            num_list = map(int, re.findall(r'\d+', raw_input()))
            if len(num_list) != 4:
                print 'illegal action!'
                continue
            action = ((num_list[0], num_list[1]), (num_list[2], num_list[3]))
            if action in legal_actions:
                break
            else:
                print 'illegal action!'
        return action

class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
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
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        return random.choice(legal_actions)
