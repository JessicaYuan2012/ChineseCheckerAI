import numpy as np
from collections import defaultdict


def diffOfAvgVerDistToGoalVertex(state):
    board = state[1]
    size = board.size
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    dist1 = np.mean([pos[0] - 1 for pos in player_piece_pos_list1])
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    dist2 = np.mean([2 * size - 1 - pos[0] for pos in player_piece_pos_list2])
    return 'diff of avg vertical dist', dist2 - dist1  # weight should be positive


def diffOfAvgSquaredVerDistToGoalVertex(state):
    # take squared of vertical distance to penalize trailing pieces
    board = state[1]
    size = board.size
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    dist1 = np.mean([(pos[0] - 1) ** 2 for pos in player_piece_pos_list1])
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    dist2 = np.mean([(2 * size - 1 - pos[0]) ** 2 for pos in player_piece_pos_list2])
    return 'diff of avg squared vertical dist', dist2 - dist1  # weight should be positive


def getVerticalAdvanceList1(state):
    board = state[1]
    player_piece_pos_list = board.getPlayerPiecePositions(1)

    ver_adv_dict = defaultdict(int)
    # check moves
    for pos in player_piece_pos_list:
        for adj_pos in board.adjacentPositions(pos):
            if board.isEmptyPosition(adj_pos):
                ver_adv_dict[pos] = max(ver_adv_dict[pos], pos[0] - adj_pos[0])

    # check hops
    for pos in player_piece_pos_list:
        for new_pos in board.getAllHopPositions(pos):
            ver_adv_dict[pos] = max(ver_adv_dict[pos], pos[0] - new_pos[0])
    return ver_adv_dict.values()


def getVerticalAdvanceList2(state):
    board = state[1]
    player_piece_pos_list = board.getPlayerPiecePositions(2)

    ver_adv_dict = defaultdict(int)
    # check moves
    for pos in player_piece_pos_list:
        for adj_pos in board.adjacentPositions(pos):
            if board.isEmptyPosition(adj_pos):
                ver_adv_dict[pos] = max(ver_adv_dict[pos], adj_pos[0] - pos[0])
    # check hops
    for pos in player_piece_pos_list:
        for new_pos in board.getAllHopPositions(pos):
            ver_adv_dict[pos] = max(ver_adv_dict[pos], new_pos[0] - pos[0])
    return ver_adv_dict.values()


def diffOfAvgMaxVerticalAdvance(state):
    mean1 = np.mean(getVerticalAdvanceList1(state))
    mean2 = np.mean(getVerticalAdvanceList2(state))
    return 'diff of avg max vertical advance', mean2 - mean1  # weight should be negative


def diffOfMaxVerticalAdvance(state):
    max1 = max(getVerticalAdvanceList1(state))
    max2 = max(getVerticalAdvanceList2(state))
    return 'diff of max vertical advance', max2 - max1


def diffOfAvgHorDistToCenter(state):
    # average horizontal distance to vertical center
    board = state[1]
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    dist1 = sum([abs(col - board.getColNum(row) * 1.0 / 2) for row, col in player_piece_pos_list1]) * 1.0 / len(
        player_piece_pos_list1)
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    dist2 = sum([abs(col - board.getColNum(row) * 1.0 / 2) for row, col in player_piece_pos_list2]) * 1.0 / len(
        player_piece_pos_list2)
    return 'diff of avg horizontal abs dist', dist2 - dist1


def diffOfAvgSquaredHorDistToCenter(state):
    board = state[1]
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    dist1 = sum([(col - board.getColNum(row) * 1.0 / 2) ** 2 for row, col in player_piece_pos_list1]) * 1.0 / len(
        player_piece_pos_list1)
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    dist2 = sum([(col - board.getColNum(row) * 1.0 / 2) ** 2 for row, col in player_piece_pos_list2]) * 1.0 / len(
        player_piece_pos_list2)
    return 'diff of avg squared horizontal dist(+/-)', dist2 - dist1


def diffOfVerticalVariance(state):
    board = state[1]
    player_piece_row_list1 = [pos[0] for pos in board.getPlayerPiecePositions(1)]
    var1 = np.var(player_piece_row_list1)
    player_piece_row_list2 = [pos[0] for pos in board.getPlayerPiecePositions(2)]
    var2 = np.var(player_piece_row_list2)
    return 'diff of vertical var', var2 - var1


def diffOfHorDistVariance(state):
    board = state[1]
    player_piece_pos_list1 = board.getPlayerPiecePositions(1)
    var1 = np.var([(col - board.getColNum(row) * 1.0 / 2) for row, col in player_piece_pos_list1])
    player_piece_pos_list2 = board.getPlayerPiecePositions(2)
    var2 = np.var([(col - board.getColNum(row) * 1.0 / 2) for row, col in player_piece_pos_list2])
    return 'diff of horizontal var', var2 - var1


def intercept(state):
    return 'intercept', 1.0
