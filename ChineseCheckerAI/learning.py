from collections import defaultdict
import random, math, sys
import numpy as np
import matplotlib.pyplot as plt


class TDLearningAlgorithm():
    def __init__(self, game, featureExtractor, discount=1, explorationProb=0.1):
        self.game = game
        self.discount = discount
        self.featureExtractor = featureExtractor
        self.explorationProb = explorationProb
        self.weights = defaultdict(float)
        self.numIters = 0

    def getV(self, state):
        score = 0
        for f, v in self.featureExtractor(state):
            score += self.weights[f] * v
        return score

    def getAction(self, state):
        self.numIters += 1
        action_list = self.game.actions(state)
        if not action_list:  # stuck
            return None

        if random.random() < self.explorationProb:
            return random.choice(action_list)
        else:
            player = state[0]
            v_list = [self.getV(self.game.succ(state, action)) for action in action_list]
            if player == 1:
                max_v = max(v_list)
                max_actions = [action_list[i] for i in range(len(action_list)) if v_list[i] == max_v]
                return random.choice(max_actions)
            else:
                min_v = min(v_list)
                min_actions = [action_list[i] for i in range(len(action_list)) if v_list[i] == min_v]
                return random.choice(min_actions)

    def getStepSize(self):
        return 1.0 / self.numIters

    def incorporateFeedback(self, state, reward, newState):
        # print 'step size now:', self.getStepSize()
        residual = self.getV(state) - (reward + self.discount * self.getV(newState))
        for f, v in self.featureExtractor(state):
            self.weights[f] -= self.getStepSize() * residual * v


def simulate(game, rl, numTrials=100, maxIterations=200, verbose=False):
    utility_list = []
    weight_update_history = defaultdict(list)
    for trial in range(numTrials):
        state = game.startState()
        totalDiscount = 1
        iter = 0
        while iter < maxIterations and not game.isEnd(state):
            action = rl.getAction(state)
            if action is None:
                print 'stuck!'
                break
            new_state = game.succ(state, action)
            if game.isEnd(new_state):
                reward = game.utility(new_state)
            else:
                reward = 0
            rl.incorporateFeedback(state, reward, new_state)
            totalDiscount *= rl.discount
            state = new_state
            iter += 1
        if verbose:
            if game.isEnd(state):
                print "Trial %d (final utility = %s)" % (trial + 1, game.utility(state))
                utility_list.append(game.utility(state))
            else:
                print "Trial %d (final utility = %s)" % (trial + 1, 0)
                utility_list.append(0)
            print 'weights after trial:', trial+1
            for feature in rl.weights:
                weight_update_history[feature].append(rl.weights[feature])
                print feature, rl.weights[feature]
    format_list = ['r--', 'b--', 'g--', 'c--', 'm--', 'y--', 'k--']
    for i in range(0, len(rl.weights.keys())):
        plt.plot(range(1, numTrials + 1), weight_update_history[rl.weights.keys()[i]], format_list[i])
    return utility_list


def averageVerticalDistanceToGoalVertex(player):
    def averageVerticalDistanceToGoalVertexOnePlayer(state):
        board = state[1]
        size = board.size
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        if player == 1:
            score = sum([pos[0] - 1 for pos in player_piece_pos_list]) * 1.0 / len(player_piece_pos_list)
        else:
            score = sum([2 * size - 1 - pos[0] for pos in player_piece_pos_list]) * 1.0 / len(player_piece_pos_list)
        return 'avg vertical dist ' + str(player), score

    return averageVerticalDistanceToGoalVertexOnePlayer


def diffOfAvgVerDistToGoalVertex(state):
    board = state[1]
    size = board.size
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    dist1 = sum([pos[0] - 1 for pos in player_piece_pos_list1]) * 1.0 / len(player_piece_pos_list1)
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    dist2 = sum([2 * size - 1 - pos[0] for pos in player_piece_pos_list2]) * 1.0 / len(player_piece_pos_list2)
    return 'diff of avg vertical dist', dist1 - dist2


def verticalVariance(player):
    def verticalVarianceOnePlayer(state):
        board = state[1]
        player_piece_row_list = [pos[0] for pos in board.getPlayerPiecePositions(player)]
        var = np.var(player_piece_row_list)
        return 'vertical var ' + str(player), var

    return verticalVarianceOnePlayer


def intercept(state):
    return 'intercept', 1.0


def getFeatureExtractor(featureFunctionList):
    def featureExtractor(state):
        features = []
        for f in featureFunctionList:
            features.append(f(state))
        return features

    return featureExtractor


def getEvalFunctionViaTDlearning(game, featureExtractorFunction, num_trials=100):
    tdLearningAgent = TDLearningAlgorithm(game, featureExtractorFunction)
    simulate(game, tdLearningAgent, verbose=True, numTrials=num_trials)

    def resultEvalFunction(state):
        weights = tdLearningAgent.weights
        eval_score = 0
        for f, v in featureExtractorFunction(state):
            eval_score += weights[f] * v
        return eval_score

    return resultEvalFunction
