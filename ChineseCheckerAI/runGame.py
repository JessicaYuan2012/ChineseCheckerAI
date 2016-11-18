from agent import *
from game import SimplifiedChineseChecker
import datetime

def runGame(ccgame, agents):
    state = ccgame.startState()
    max_iter = 100  # deal with some stuck situations
    iter = 0
    start = datetime.datetime.now()
    while (not ccgame.isEnd(state)) and iter < max_iter:
        iter += 1
        # print 'current board:'
        # state[1].printBoard()
        player = ccgame.player(state)
        agent = agents[player]
        action = agent.getAction(state)
        # print 'player', str(player), 'takes action', str(action)
        state = ccgame.succ(state, action)
    print 'final board:'
    state[1].printBoard()
    end = datetime.datetime.now()
    print 'time spent:', end-start
    if ccgame.isEnd(state):
        # print ccgame.utility(state)
        return (state[1].isEnd()[1], ccgame.utility(state)) # return (winner, utility)
    else: # stuck situation
        print 'stuck!'
        return (0, 0)

def simulateMultipleGames(agents_dict, simulation_times, ccgame):
    win_times = 0
    stuck_times = 0
    utility_sum = 0
    # 1: agent, 2: opp
    agent1 = agents_dict[1](ccgame)
    agent2 = agents_dict[2](ccgame)
    agents = {1: agent1, 2: agent2}
    for i in range(simulation_times):
        run_result = runGame(ccgame, agents)
        if run_result[0] == 1:
            win_times += 1
        elif run_result[0] == 0:
            stuck_times += 1
        utility_sum += run_result[1]
        print 'game', i+1, 'finished'
    print 'In', simulation_times, 'simulations:'
    print 'winning times:', win_times
    print 'winning rate:', win_times * 1.0 / simulation_times
    print 'stuck times:', stuck_times
    # print 'average utility', utility_sum * 1.0 / simulation_times

if __name__ == '__main__':
    ccgame = SimplifiedChineseChecker(5, 3)
    #runGame(ccgame, {1:SimpleGreedyAgent(ccgame), 2:RandomAgent(ccgame)})
    simulateMultipleGames({1: SimpleGreedyAgent , 2: MiniMaxAlphaBetaAgent}, 25, ccgame)


