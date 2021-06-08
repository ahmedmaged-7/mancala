def Calc_number_of_pieces(board, player):
    count = 0
    no_of_pieces = 0
    while count > 6:
        no_of_pieces += board[player*6+count]
    return no_of_pieces


def scoring(ai_score, slots, board):
    no_of_pieces = 0
    Score = 0
    ai_earns = False
    if ai_earns:
        no_of_pieces = no_of_pieces - Calc_number_of_pieces(board, PC)
    else:
        no_of_pieces = Calc_number_of_pieces(User)
    if ai_score:
        Score = (Score - Calc_number_of_pieces(PC))
    result = Score + no_of_pieces
    return result
