from board import SimplifiedBoard
import copy

class SimplifiedChineseChecker(object):
    def __init__(self, size, piece_rows):
        self.size = size
        self.piece_rows = piece_rows

    def startState(self):
        # state is in format (player, current board object)
        # player is 1 (agent), 2 (opp)
        return (1, SimplifiedBoard(self.size, self.piece_rows))

    def isEnd(self, state):
        return state[1].isEnd()[0]

    def stepsToGo(self, state, player):
        # at end state, minimum steps player need to take to reach the target triangle
        # not efficient enough when far from destination
        visited = set([])
        frontier = [state]
        remain_steps = 0
        while True:
            remain_steps += 1
            new_frontier = []
            for new_state in frontier:
                new_state = (player, new_state[1])
                for action in self.actions(new_state):
                    if player == 2 and action[0][0] > action[1][0]:
                        continue
                    if player == 1 and action[0][0] < action[1][0]:
                        continue
                    succ = (player, self.succ(new_state, action)[1])
                    if succ[1].ifPlayerWin(player):
                        return remain_steps
                    if succ not in visited:
                        visited.add(succ)
                        new_frontier.append(succ)
                    else:
                        continue
            frontier = new_frontier

    def utility(self, state):
        end_info = state[1].isEnd()
        assert end_info[0]
        # steps = self.stepsToGo(state, 3-end_info[1])
        if end_info[1] == 1:
            return 1
        else:
            return -1

    def actions(self, state):
        # return possible actions current player can take in a list [(old_pos), (new_pos)]
        action_list = []
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)

        # check moves
        for pos in player_piece_pos_list:
            for adj_pos in board.adjacentPositions(pos):
                if board.isEmptyPosition(adj_pos):
                    action_list.append((pos, adj_pos))

        # check hops
        for pos in player_piece_pos_list:
            for new_pos in board.getAllHopPositions(pos):
                if (pos, new_pos) not in action_list:
                    action_list.append((pos, new_pos))
        return action_list

    def player(self, state):
        return state[0]

    def succ(self, state, action):
        player = state[0]
        board = copy.deepcopy(state[1])
        assert board.board_status[action[0]] == player
        assert board.board_status[action[1]] == 0
        board.board_status[action[1]] = player
        board.board_status[action[0]] = 0
        return (3 - player, board)
