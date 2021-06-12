import unittest

from mancala import *


# to apply test make sure the mancal does not call game instance
class TestSum(unittest.TestCase):
    def test_no_steal_normal_turn(self):
        a = take_turn_no_stealing()
        my_side = [4, 4, 4, 4, 4, 4]
        opponent_side = [4, 4, 4, 4, 4, 4]
        my_score = 0
        opponent_score = 0
        slot = 4
        result_of_taking_turn = a.take_turn(my_side, opponent_side, my_score, opponent_score, slot)
        self.assertEqual(result_of_taking_turn, [[4, 4, 4, 0, 5, 5], 1, [4, 4, 4, 4, 4, 5], 0, False],
                         "did not have a right turn")

    def test_no_steal_whole_board(self):
        a = take_turn_no_stealing()
        my_side = [4, 4, 4, 4, 4, 9]
        opponent_side = [4, 4, 4, 4, 4, 4]
        my_score = 0
        opponent_score = 0
        slot = 6
        result_of_taking_turn = a.take_turn(my_side, opponent_side, my_score, opponent_score, slot)
        self.assertEqual(result_of_taking_turn, [[5, 5, 4, 4, 4, 0], 1, [5, 5, 5, 5, 5, 5], 0, False],
                         "did not have a right turn")

    def test_no_steal_next_turn(self):
        a = take_turn_no_stealing()
        my_side = [4, 4, 4, 4, 4, 1]
        opponent_side = [4, 4, 4, 4, 4, 4]
        my_score = 0
        opponent_score = 0
        slot = 6
        result_of_taking_turn = a.take_turn(my_side, opponent_side, my_score, opponent_score, slot)
        self.assertEqual(result_of_taking_turn, [[4, 4, 4, 4, 4, 0], 1, [4, 4, 4, 4, 4, 4], 0, True],
                         "did not have a right turn")

    def test_no_steal_next_turn_whole_board(self):
        a = take_turn_no_stealing()
        my_side = [4, 4, 4, 4, 4, 14]
        opponent_side = [4, 4, 4, 4, 4, 4]
        my_score = 0
        opponent_score = 0
        slot = 6
        result_of_taking_turn = a.take_turn(my_side, opponent_side, my_score, opponent_score, slot)
        self.assertEqual(result_of_taking_turn, [[5, 5, 5, 5, 5, 1], 2, [5, 5, 5, 5, 5, 5], 0, True],
                         "did not have a right turn")

    def test_check_board_is_not_empty(self):
        test_board = Board(True)
        self.assertFalse(test_board.empty_side())

    def test_check_board_is_empty(self):
        test_board = Board(True)
        test_board.my_side = [0, 0, 0, 0, 0, 0]
        self.assertTrue(test_board.empty_side())

    def test_opp_score_when_user_board_empty(self):
        test_board = Board(True)
        test_board.my_side = [0, 0, 0, 0, 0, 0]
        test_board.empty_side()
        self.assertEqual(test_board.opponent_score, 4 * 6)

    def test_user_score_when_opp_board_empty(self):
        test_board = Board(True)
        test_board.opponent_side = [0, 0, 0, 0, 0, 0]
        test_board.empty_side()

        self.assertEqual(test_board.my_score, 4 * 6)

    def test_fliping(self):
        test_board = Board(True)
        test_board.my_side = [7, 0, 1, 2, 5, 0]
        a = test_board.opponent_side
        test_board.board_flip()
        self.assertEqual(a, test_board.my_side)

    def test_stealing(self):
        a = take_turn_with_stealing()
        my_side = [4, 4, 4, 4, 1, 0]
        opponent_side = [4, 4, 4, 4, 4, 4]
        my_score = 0
        opponent_score = 0
        slot = 5
        result_of_taking_turn = a.take_turn(my_side, opponent_side, my_score, opponent_score, slot)
        self.assertEqual(result_of_taking_turn, [[4, 4, 4, 4, 0, 0], 5, [4, 4, 4, 4, 4, 0], 0, False],
                         "did not have a right turn")


if __name__ == '__main__':
    unittest.main()
