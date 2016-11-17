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

class MiniMaxAgent(Agent):
    # Minimax agent
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        player = self.game.player(state)
        global mainplayer
        mainplayer = player
        global oppplayer
        oppplayer= 3 - mainplayer

        depth = 1

        score = [self.Vmaxmin(self.game.succ(state, action), depth, player) for action in legal_actions]
        max_score = max(score)
        max_actions = [legal_actions[index] for index in range(len(score)) if score[index] == max_score]
        return random.choice(max_actions)

    #Define function Vmaxmin(s, d, agentnum) to compute the score
    def Vmaxmin(self, CurrentGameState, d, agentnum):

      #IsEnd(s)
      if self.game.isEnd(CurrentGameState):
        if CurrentGameState[1].isEnd()[1] == mainplayer:
            return float('inf')   #if main player wins
        else:
            return -float('inf')

      # depth d = 0
      elif d == 0:
        return self.evaluationFunction(CurrentGameState)

      #check the depth make recursion
      agentnum += 1
      if agentnum == 3: # go back to the agent 1
        agentnum = 1
      if agentnum == oppplayer: # reach the opponent in a depth level
        d -= 1

      #print 'agentnum = %i' %agentnum
      #print 'depth = %i' %d

      #Get the legal moves, (next agent)
      legal_actions = self.game.actions(CurrentGameState)
      Allscore = [self.Vmaxmin(self.game.succ(CurrentGameState, action), d, agentnum) for action in legal_actions]
      if agentnum == mainplayer:
        return max(Allscore)
      else:
        return min(Allscore)

    def evaluationFunction(self, currentGameState):
        size = self.game.size
        #piece_rows = self.game.piece_rows
        #player = currentGameState[0]
        board = currentGameState[1]
        player_piece_pos_list1 = board.getPlayerPiecePositions(1)
        # The Evaluation function considers the sum of distances of each piece to the corner
        # With smaller distance, it is closer to win and the score is higher
        # For Player 1, it is the distance to (1,1), which is just (row - 1)
        p1score = sum([pos[0]-1 for pos in player_piece_pos_list1])

        # For Player 2, it is the distance to (2*size-1,1)
        player_piece_pos_list2 = board.getPlayerPiecePositions(2)
        p2score = sum([2*size - 1 - pos[0] for pos in player_piece_pos_list2])

        if mainplayer == 1:
            return p2score - p1score
        else:
            return p1score - p2score

# Minimax with alpha beta pruning
class MiniMaxAlphaBetaAgent(Agent):
    # Minimax agent
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        player = self.game.player(state)
        global mainplayer
        mainplayer = player
        global oppplayer
        oppplayer= 3 - mainplayer

        depth = 2

        alpha = -float('inf')    #The lower bound
        beta = float('inf')      #The upper bound
        score = []
        for action in legal_actions:
            NodeScore = self.Vmaxmin(self.game.succ(state, action), depth, player, alpha, beta)
            score.append(NodeScore)
            # if not overlap, break(which should not in this case since it compute the lower bound which should always overlap with beta = -inf)
            if not self.Overlap(NodeScore, alpha, beta, player):
              #print "break"
              break

        max_score = max(score)
        max_actions = [legal_actions[index] for index in range(len(score)) if score[index] == max_score]

        return random.choice(max_actions)

    def Overlap(self, num, alpha, beta, agentnum):
      # alpha: lower bound, the number needs to be >= alpha
      # beta: upper bound, the number needs to be <= beta
      # for agent = mainplayer, the interval is >= num
      # else,          the interval is <= num
      if agentnum == mainplayer:     #mainplayer which num is the temperary lower bound to test
        if num >= beta:     #Temperary lower bound num is higher than beta, which is the upper bound -> not overlap
          return 0
        else:
          return 1
      else:                #opponent which num is the temperary upper bound to test
        if num <= alpha:   #Temperary Upper bound num is lower than Alpha, which is the lower bound -> not overlap
          return 0
        else:
          return 1


    #Define function Vmaxmin(s, d, agentnum) to compute the score
    def Vmaxmin(self, CurrentGameState, d, agentnum, alpha, beta):

      #IsEnd(s)
      if self.game.isEnd(CurrentGameState):
        if CurrentGameState[1].isEnd()[1] == mainplayer:
            return float('inf')   #if main player wins
        else:
            return -float('inf')

      # depth d = 0
      elif d == 0:
        return self.evaluationFunction(CurrentGameState)

      #check the depth make recursion
      agentnum += 1
      if agentnum == 3: # go back to the agent 1
        agentnum = 1
      if agentnum == oppplayer: # reach the opponent in a depth level
        d -= 1

      #print 'agentnum = %i' %agentnum
      #print 'depth = %i' %d

      #Get the legal moves, (next agent)
      legal_actions = self.game.actions(CurrentGameState)

      Allscore = []
      for action in legal_actions:
        NodeScore = self.Vmaxmin(self.game.succ(CurrentGameState, action), d, agentnum, alpha, beta)
        Allscore.append(NodeScore)
        # if not overlap, break(which should not in this case since it compute the lower bound which should always overlap with beta = -inf)
        if not self.Overlap(NodeScore, alpha, beta, agentnum):
          #print "break"
          break
        if agentnum == mainplayer:
          if NodeScore > alpha: # compare with alpha for mainplayer
            alpha = NodeScore
        else:
          if NodeScore < beta: # compare with bete for opponent
            beta = NodeScore

      if agentnum == mainplayer:
        return max(Allscore)
      else:
        return min(Allscore)

    def evaluationFunction(self, currentGameState):
        size = self.game.size
        #piece_rows = self.game.piece_rows
        #player = currentGameState[0]
        board = currentGameState[1]
        player_piece_pos_list1 = board.getPlayerPiecePositions(1)
        # The Evaluation function considers the sum of distances of each piece to the corner
        # With smaller distance, it is closer to win and the score is higher
        # For Player 1, it is the distance to (1,1), which is just (row - 1)
        p1score = sum([pos[0]-1 for pos in player_piece_pos_list1])

        # For Player 2, it is the distance to (2*size-1,1)
        player_piece_pos_list2 = board.getPlayerPiecePositions(2)
        p2score = sum([2*size - 1 - pos[0] for pos in player_piece_pos_list2])

        if mainplayer == 1:
            return p2score - p1score
        else:
            return p1score - p2score
