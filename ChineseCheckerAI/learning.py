from collections import defaultdict
import random, math, sys
import numpy as np
import matplotlib.pyplot as plt


class TDLearningAlgorithm():
    def __init__(self, game, featureExtractor, discount=1, explorationProb=0.15):
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
            print 'weights after trial:', trial + 1
        print 'Trial %d' % (trial + 1)
        for feature in rl.weights:
            weight_update_history[feature].append(rl.weights[feature])
            if verbose:
                print feature, rl.weights[feature]

    fig, ax = plt.subplots()
    format_list = ['r--', 'b--', 'g--', 'c--', 'm--', 'y--', 'k--']
    for i in range(0, len(rl.weights.keys())):
        ax.plot(range(1, numTrials + 1), weight_update_history[rl.weights.keys()[i]],
                format_list[i], label=rl.weights.keys()[i])
    legend = ax.legend(loc='upper center', shadow=True)
    plt.ylabel('weight value')
    plt.xlabel('# iteration')
    return utility_list


def getFeatureExtractor(featureFunctionList):
    def featureExtractor(state):
        features = []
        for f in featureFunctionList:
            features.append(f(state))
        return features

    return featureExtractor


def getEvalFunctionViaTDlearning(game, featureExtractorFunction, num_trials=100):
    tdLearningAgent = TDLearningAlgorithm(game, featureExtractorFunction)
    simulate(game, tdLearningAgent, verbose=False, numTrials=num_trials)

    for f in tdLearningAgent.weights:
        print 'feature:', f, '; weight:', tdLearningAgent.weights[f]

    def resultEvalFunction(state):
        weights = tdLearningAgent.weights
        eval_score = 0
        for f, v in featureExtractorFunction(state):
            eval_score += weights[f] * v
        return eval_score

    return resultEvalFunction


def getEvalFunctionGivenWeights(feature_weight_dict):
    def resultEvalFunction(state):
        eval_score = 0
        for func, weight in feature_weight_dict.items():
            eval_score += weight * func(state)[1]
        return eval_score

    return resultEvalFunction
