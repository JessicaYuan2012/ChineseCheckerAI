from agent import *
from game import SimplifiedChineseChecker

def runGame(ccgame, agents):
    state = ccgame.startState()
    while not ccgame.isEnd(state):
        # print 'current board:'
        # state[1].printBoard()
        player = ccgame.player(state)
        agent = agents[player]
        action = agent.getAction(state)
        # print 'player', str(player), 'takes action', str(action)
        state = ccgame.succ(state, action)
    print 'final board:'
    state[1].printBoard()
    return state[1].isEnd()[1] # return the winner

if __name__ == '__main__':
    simulation_times = 500
    win_times = 0
    for i in range(simulation_times):
        ccgame = SimplifiedChineseChecker(4, 2)
        agent1 = SimpleGreedyAgent(ccgame)
        agent2 = RandomAgent(ccgame)
        # 1: agent, 2: opp
        agents = {1: agent1, 2: agent2}

        if runGame(ccgame, agents) == 1:
            win_times += 1
        print 'game', i, 'finished'
    print 'winning rate:', win_times*1.0/simulation_times


