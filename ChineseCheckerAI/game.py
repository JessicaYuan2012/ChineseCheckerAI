from board import SimplifiedBoard


class SimplifiedChineseChecker(object):
    def __init__(self, size, piece_rows):
        self.board = SimplifiedBoard(size, piece_rows)

    def startState(self):
        # state is in format (player, current board object)
        # player is 1 (agent), 2 (opp)
        return (1, self.board)

    def isEnd(self, state):
        return state[1].isEnd()[0]

    def stepsToGo(self, state, player):
        # at end state, minimum steps player need to take to reach the target triangle
        return 0
        # raise Exception("Not implemented yet")

    def utility(self, state):
        end_info = state[1].isEnd()
        assert end_info[0]
        if end_info[1] == 0:
            return 0  # tie
        else:
            steps = self.stepsToGo(state, 3-end_info[1])
            if end_info[1] == 1:
                return steps
            else:
                return -steps

    def actions(self, state):
        action_list = []
        player = state[0]
        player_piece_pos_list = self.board.getPlayerPiecePositions(player)

        # check moves
        for pos in player_piece_pos_list:
            for adj_pos in self.board.adjacentPositions(pos):
                if self.board.isEmptyPosition(adj_pos):
                    action_list.append((pos, adj_pos))

        # check hops
        for pos in player_piece_pos_list:
            for new_pos in self.board.getAllHopPositions(pos):
                if (pos, new_pos) not in action_list:
                    action_list.append((pos, new_pos))
        return action_list

    def player(self, state):
        return state[0]

    def succ(self, state, action):
        player = state[0]
        board = state[1]
        assert board.board_status[action[0]] == player
        assert board.board_status[action[1]] == 0
        board.board_status[action[1]] = player
        board.board_status[action[0]] = 0
        return (3 - player, board)
