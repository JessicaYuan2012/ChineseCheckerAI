from agent import *
from game import SimplifiedChineseChecker
from learning import *
from features import *
import datetime


def runGame(ccgame, agents):
    state = ccgame.startState()
    max_iter = 200  # deal with some stuck situations
    iter = 0
    start = datetime.datetime.now()
    while (not ccgame.isEnd(state)) and iter < max_iter:
        iter += 1
        # print 'current board:'
        # state[1].printBoard()
        player = ccgame.player(state)
        agent = agents[player]
        action = agent.getAction(state)
        if action is None:
            break
        # print 'player', str(player), 'takes action', str(action)
        state = ccgame.succ(state, action)
    print '# of rounds:', iter
    print 'final board:'
    state[1].printBoard()
    end = datetime.datetime.now()
    print 'time spent:', end - start
    if ccgame.isEnd(state):
        # print ccgame.utility(state)
        return (state[1].isEnd()[1], ccgame.utility(state))  # return (winner, utility)
    else:  # stuck situation
        print 'stuck!'
        return (0, 0)


def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times = 0
    stuck_times = 0
    utility_sum = 0
    for i in range(simulation_times):
        run_result = runGame(ccgame, agents_dict)
        if run_result[0] == 1:
            win_times += 1
        elif run_result[0] == 0:
            stuck_times += 1
        utility_sum += run_result[1]
        print 'game', i + 1, 'finished'
        print 'utility:', run_result[1]
    print 'In', simulation_times, 'simulations:'
    print 'winning times:', win_times
    print 'stuck times:', stuck_times
    print 'winning rate:', win_times * 1.0 / (simulation_times - stuck_times)
    print 'average utility', utility_sum * 1.0 / simulation_times


if __name__ == '__main__':
    ccgame = SimplifiedChineseChecker(5, 3)
    # 0. human agent
    humanAgent = HumanAgent(ccgame)
    # 1. baseline - simple greedy agent
    simpleGreedyAgent = SimpleGreedyAgent(ccgame)
    # 2. minimax agent with naive evaluation function
    # minimaxAgent = MiniMaxAlphaBetaAgent(ccgame, depth=2)

    # 3. minimax agent with different evaluation function learned via TD-learning
    # td-agent 1 (2 features)
    # featureFuctionList1 = [diffOfAvgVerDistToGoalVertex, diffOfAvgSquaredVerDistToGoalVertex]
    # featureExtractor1 = getFeatureExtractor(featureFuctionList1)
    # evalFunction1 = getEvalFunctionViaTDlearning(ccgame, featureExtractor1, num_trials=1000)
    # tdAgent1 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction1)
    feature_weight_dict1 = {diffOfAvgSquaredVerDistToGoalVertex: 0.00328899184996,
                            diffOfAvgVerDistToGoalVertex: 0.0238213005841}
    evalFunction1 = getEvalFunctionGivenWeights(feature_weight_dict1)
    tdAgent1 = MiniMaxAlphaBetaAgent(ccgame, depth=3, evalFunction=evalFunction1, timing=True)
    minimaxAgent = MiniMaxAgent(ccgame, depth=3, evalFunction=evalFunction1, timing=True)

    # td-agent 2 (3 features)
    # featureFuctionList2 = [diffOfAvgVerDistToGoalVertex, diffOfAvgSquaredVerDistToGoalVertex,
    #                        diffOfAvgMaxVerticalAdvance]
    # featureExtractor2 = getFeatureExtractor(featureFuctionList2)
    # evalFunction2 = getEvalFunctionViaTDlearning(ccgame, featureExtractor2, num_trials=1000)
    # tdAgent2 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction2)

    feature_weight_dict2 = {diffOfAvgMaxVerticalAdvance: -5.92186496368e-05,
                            diffOfAvgSquaredVerDistToGoalVertex: 0.00441843679602,
                            diffOfAvgVerDistToGoalVertex: 0.0145534806826}
    evalFunction2 = getEvalFunctionGivenWeights(feature_weight_dict2)
    tdAgent2 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction2)

    # td-agent 3 (4 features)
    # featureFuctionList3 = [diffOfAvgVerDistToGoalVertex, diffOfAvgSquaredVerDistToGoalVertex,
    #                        diffOfAvgMaxVerticalAdvance, intercept]
    # featureExtractor3 = getFeatureExtractor(featureFuctionList3)
    # evalFunction3 = getEvalFunctionViaTDlearning(ccgame, featureExtractor3, num_trials=1000)
    # tdAgent3 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction3)

    feature_weight_dict3 = {intercept: 0.0308445738283,
                            diffOfAvgMaxVerticalAdvance: -3.8784725201e-05,
                            diffOfAvgSquaredVerDistToGoalVertex: 0.0053661434185,
                            diffOfAvgVerDistToGoalVertex: 0.0134529315166}
    evalFunction3 = getEvalFunctionGivenWeights(feature_weight_dict3)
    tdAgent3 = MiniMaxAlphaBetaAgent(ccgame, depth=2, evalFunction=evalFunction3, timing=True)

    simulateMultipleGames({1: minimaxAgent, 2: tdAgent1}, 2, ccgame)
    print 'average time to get an action:', minimaxAgent.total_exec_time/minimaxAgent.num_exec
    print 'average time to get an action:', tdAgent1.total_exec_time/tdAgent1.num_exec


    # plt.show()
