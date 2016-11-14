class SimplifiedBoard(object):
    def __init__(self, size, piece_rows):
        assert piece_rows < size
        self.size = size
        self.piece_rows = piece_rows
        self.board_status = {}
        # player is 1 (agent), 2 (opp)
        # 1's pieces are at the bottom, and 2's are on the top at initialization
        for row in range(1, size+1):
            for col in range(1, row+1):
                if row <= piece_rows:
                    self.board_status[(row, col)] = 2
                else:
                    self.board_status[(row, col)] = 0
        for row in range(size+1, size*2):
            for col in range(1, size*2-row+1):
                if row < size*2 - piece_rows:
                    self.board_status[(row, col)] = 0
                else:
                    self.board_status[(row, col)] = 1

    def isEmptyPosition(self, pos):
        return self.board_status[pos] == 0

    def leftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if (row, col - 1) in self.board_status.keys():
            return (row, col-1)

    def rightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if (row, col + 1) in self.board_status.keys():
            return (row, col + 1)

    def upLeftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row <= self.size and (row-1, col-1) in self.board_status.keys():
            return (row-1, col-1)
        if row > self.size and (row-1, col) in self.board_status.keys():
            return (row-1, col)

    def upRightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row <= self.size and (row-1, col) in self.board_status.keys():
            return (row-1, col)
        if row > self.size and (row-1, col+1) in self.board_status.keys():
            return (row-1, col+1)

    def downLeftPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row < self.size and (row+1, col) in self.board_status.keys():
            return (row+1, col)
        if row >= self.size and (row+1, col-1) in self.board_status.keys():
            return (row+1, col-1)

    def downRightPosition(self, pos):
        row = pos[0]
        col = pos[1]
        if row < self.size and (row+1, col+1) in self.board_status.keys():
            return (row+1, col+1)
        if row >= self.size and (row+1, col) in self.board_status.keys():
            return (row+1, col)

    def adjacentPositions(self, pos):
        result = []
        result.append(self.leftPosition(pos))
        result.append(self.rightPosition(pos))
        result.append(self.upLeftPosition(pos))
        result.append(self.upRightPosition(pos))
        result.append(self.downLeftPosition(pos))
        result.append(self.downRightPosition(pos))
        return filter(lambda x: x is not None, result)

    def getPlayerPiecePositions(self, player):
        result1 = [(row, col) for row in range(1, self.size+1) for col in range(1, row+1) \
                   if self.board_status[(row,col)] == player]
        result2 = [(row, col) for row in range(self.size+1, self.size*2) for col in range(1, self.size*2-row+1)\
                   if self.board_status[(row, col)] == player]
        return result1 + result2

    def getOneDirectionHopPosition(self, pos, dir_func):
        hop_over_pos = dir_func(pos)
        count = 0
        while hop_over_pos is not None:
            if self.board_status[hop_over_pos] != 0:
                break
            hop_over_pos = dir_func(hop_over_pos)
            count += 1
        if hop_over_pos is not None:
            target_position = dir_func(hop_over_pos)
            while count > 0:
                if target_position is None or self.board_status[target_position] != 0:
                    break
                target_position = dir_func(target_position)
                count -= 1
            if count == 0 and target_position is not None and self.board_status[target_position] == 0:
                return target_position

    def getOneHopPositions(self, pos):
        result = []
        result.append(self.getOneDirectionHopPosition(pos, self.leftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.rightPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.upLeftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.upRightPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.downLeftPosition))
        result.append(self.getOneDirectionHopPosition(pos, self.downRightPosition))
        return filter(lambda x: x is not None, result)

    def getAllHopPositions(self, pos):
        result = self.getOneHopPositions(pos)
        start_index = 0
        while start_index < len(result):
            cur_size = len(result)
            for i in range(start_index, cur_size):
                for new_pos in self.getOneHopPositions(result[i]):
                    if new_pos not in result:
                        result.append(new_pos)
            start_index = cur_size
        return result

    def isEnd(self):
        player_1_reached = True
        for row in range(1, self.piece_rows+1):
            for col in range(1, row+1):
                if self.board_status[(row, col)] == 1:
                    continue
                else:
                    player_1_reached = False
                    break
            if not player_1_reached:
                break
        player_2_reached = True
        for row in range(self.size*2 - self.piece_rows, self.size*2):
            for col in range(1, self.size*2-row+1):
                if self.board_status[(row, col)] == 2:
                    continue
                else:
                    player_2_reached = False
                    break
            if not player_2_reached:
                break
        if player_1_reached and player_2_reached:
            return (True, 0) # tie
        if player_1_reached:
            return (True, 1) # player 1 wins
        if player_2_reached:
            return (True, 2) # player 2 wins
        return (False, None) # haven't reach the end

    def printBoard(self):
        for row in range(1, self.size+1):
            print ' ' * (self.size - row),
            for col in range(1, row+1):
                print str(self.board_status[(row, col)]),
            print '\n',
        for row in range(self.size+1, self.size*2):
            print ' ' * (row - self.size),
            for col in range(1, self.size*2-row+1):
                print str(self.board_status[(row, col)]),
            print '\n',

# simplified_board = SimplifiedBoard(5,0)
# simplified_board.board_status[(5, 2)] = 1
# simplified_board.board_status[(5, 3)] = 1
# simplified_board.board_status[(5, 4)] = 1
# simplified_board.board_status[(5, 5)] = 1
# simplified_board.board_status[(4, 3)] = 1
# simplified_board.board_status[(2, 1)] = 1
# simplified_board.board_status[(3, 1)] = 1
# simplified_board.printBoard()
# simplified_board.board_status[(2, 2)] = 1
# simplified_board.board_status[(6, 1)] = 2
# simplified_board.board_status[(6, 2)] = 2
# simplified_board.board_status[(5, 1)] = 2
#
# print simplified_board.isEnd()

# print simplified_board.adjacentPositions((5,2))
# print simplified_board.getAllHopPositions((2,1))