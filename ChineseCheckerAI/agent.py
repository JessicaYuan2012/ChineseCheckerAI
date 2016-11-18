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
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        return random.choice(max_actions)


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        return random.choice(legal_actions)


class MiniMaxAgent(Agent):
    # Minimax agent
    def getAction(self, state):
        depth = 1
        legal_actions = self.game.actions(state)
        player = self.game.player(state)
        score = [self.Vmaxmin(self.game.succ(state, action), depth) for action in legal_actions]
        if player == 1:
            max_score = max(score)
            max_actions = [legal_actions[index] for index in range(len(score)) if score[index] == max_score]
            return random.choice(max_actions)
        else:
            min_score = min(score)
            min_actions = [legal_actions[index] for index in range(len(score)) if score[index] == min_score]
            return random.choice(min_actions)

    # Define function Vmaxmin(s, d, agentnum) to compute the score
    def Vmaxmin(self, CurrentGameState, d):
        if self.game.isEnd(CurrentGameState):
            return self.evaluationFunction(CurrentGameState)
            # return self.game.utility(CurrentGameState)
        elif d == 0:
            return self.evaluationFunction(CurrentGameState)

        # Get the legal moves, (next agent)
        legal_actions = self.game.actions(CurrentGameState)
        agentnum = CurrentGameState[0]
        if agentnum == 1:
            Allscore = [self.Vmaxmin(self.game.succ(CurrentGameState, action), d) for action in legal_actions]
            return max(Allscore)
        else:
            Allscore = [self.Vmaxmin(self.game.succ(CurrentGameState, action), d-1) for action in legal_actions]
            return min(Allscore)

    def evaluationFunction(self, currentGameState):
        size = self.game.size
        board = currentGameState[1]
        # The Evaluation function considers the sum of distances of each piece to the corner
        # With smaller distance, it is closer to win and the score is higher
        # For Player 1, it is the distance to (1,1), which is just (row - 1)
        player_piece_pos_list1 = board.getPlayerPiecePositions(1)
        p1score = sum([pos[0] - 1 for pos in player_piece_pos_list1])
        # For Player 2, it is the distance to (2*size-1,1)
        player_piece_pos_list2 = board.getPlayerPiecePositions(2)
        p2score = sum([2 * size - 1 - pos[0] for pos in player_piece_pos_list2])
        return p2score - p1score


# Minimax with alpha beta pruning
class MiniMaxAlphaBetaAgent(Agent):
    # Minimax agent
    def getAction(self, state):
        depth = 1
        legal_actions = self.game.actions(state)
        player = self.game.player(state)
        alpha = -float('inf')
        beta = float('inf')
        score = [self.alphabeta(self.game.succ(state, action), depth, alpha, beta, 3-player) for action in legal_actions]
        if player == 1:
            max_score = max(score)
            max_actions = [legal_actions[index] for index in range(len(score)) if score[index] == max_score]
            return random.choice(max_actions)
        else:
            min_score = min(score)
            min_actions = [legal_actions[index] for index in range(len(score)) if score[index] == min_score]
            return random.choice(min_actions)

    def alphabeta(self, state, depth, alpha, beta, player):
        if self.game.isEnd(state):
            # return self.game.utility(state)
            return self.evaluationFunction(state)
        elif depth == 0:
            return self.evaluationFunction(state)

        if player == 1:
            v = float('-inf')
            legal_actions = self.game.actions(state)
            for action in legal_actions:
                succ = self.game.succ(state, action)
                v = max(v, self.alphabeta(succ, depth-1, alpha, beta, 3-player))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        else:
            v = float('inf')
            legal_actions = self.game.actions(state)
            for action in legal_actions:
                succ = self.game.succ(state, action)
                v = min(v, self.alphabeta(succ, depth-1, alpha, beta, 3-player))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return v

    def evaluationFunction(self, currentGameState):
        size = self.game.size
        board = currentGameState[1]
        # The Evaluation function considers the sum of distances of each piece to the corner
        # With smaller distance, it is closer to win and the score is higher
        # For Player 1, it is the distance to (1,1), which is just (row - 1)
        player_piece_pos_list1 = board.getPlayerPiecePositions(1)
        p1score = sum([pos[0] - 1 for pos in player_piece_pos_list1])
        # For Player 2, it is the distance to (2*size-1,1)
        player_piece_pos_list2 = board.getPlayerPiecePositions(2)
        p2score = sum([2 * size - 1 - pos[0] for pos in player_piece_pos_list2])
        return p2score - p1score