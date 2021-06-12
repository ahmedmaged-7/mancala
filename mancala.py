import datetime
import os.path
import pickle

from NOde import *


class Game:
    def __init__(self):

        self.gameRound = 1
        self.difficulty = 1
        self.board = Board(True)
        self.verbose = False
        print("New game : enter \"n\" \nLoad game : enter \"l\" ")
        new_game = input()

        if new_game == "n":
            self.playNew()
        else:
            self.loadGame()

    def playNew(self):

        print("Choose a difficulty level from \"1\" to \"9\" (1 = Very Easy , 9 = Very Hard) : ")
        self.difficulty = int(input())

        print("To play Mancala with stealing enter \"y\" without stealing enter any key")
        user_choice = input()

        if user_choice == 'y':
            print("you chose playing with stealing")
        else:
            self.board.__init__(False)
            print("you chose playing without stealing")

        print("if you want verbose mode please enter v else enter any key")
        user_verbose = input()

        if user_verbose == "v":
            self.verbose = True

        self.loop()

    def saveGame(self):
        if not os.path.isdir("saves/"):
            os.mkdir("saves/")

        print("Enter file name : ")
        fileName = "saves/" + input() + ".mancala.pkl"

        tempMySide = list(self.board.my_side)
        tempOpSide = list(self.board.opponent_side)
        tempMyScore = self.board.my_score
        tempOpScore = self.board.opponent_score
        isStealing = self.board.isStealing
        gameRound = self.gameRound

        with open(fileName, 'wb') as file:
            pickle.dump({"my_side": tempMySide, "op_side": tempOpSide, "myScore": tempMyScore, "opScore": tempOpScore,
                         "isStealing": isStealing, "difficulty": self.difficulty, "gameRound": gameRound},
                        file)
        print(pickle.load(open(fileName, "rb")))

    def loadGame(self):

        print("Enter file name to be loaded : ")
        filePath = "saves/" + input() + ".mancala.pkl"

        if os.path.isfile(filePath):
            state = pickle.load(open(filePath, "rb"))
            self.board.__init__(state["isStealing"])
            self.board.my_side = state["my_side"]
            self.board.opponent_side = state["op_side"]
            self.board.my_score = state["myScore"]
            self.board.opponent_score = state["opScore"]
            self.difficulty = state["difficulty"]
            self.gameRound = state["gameRound"]
            self.loop()
        else:
            print("File not found !")
            self.__init__()

    def loop(self):

        turn = False

        while not self.check_winner():
            print(f"Round : {self.gameRound}")
            self.user_turn(turn)

            if self.check_winner():
                break

            self.Ai_turn()
            turn = True
            self.gameRound += 1

            print("Enter \"q\" if you want to save the game and quit, or enter \"c\" to continue.")
            if input() == "q":
                self.saveGame()
                break

        self.end_game()

    def user_turn(self, turn_board=True):

        if turn_board:
            print("user flipped")

        self.board.print_board()
        print("choose a slot to play")
        slot = input()
        play_another_time = self.board.board_turn(slot)[4]
        self.board.print_board(True)

        if play_another_time and max(self.board.my_side) != 0:
            self.board.opponent_side.reverse()
            self.user_turn(False)

    def check_winner(self):

        if self.board.empty_side():
            print(self.board.get_current_winner())
            return True
        else:
            return False

    def Ai_turn(self):

        currentBoard, score = self.board.get_board()
        a = datetime.datetime.now()
        slot, stats_returned, branchingFactorList = ai_choice(currentBoard, score, self.board.isStealing,
                                                              maxDepth=self.difficulty)
        slot += 1

        if self.verbose:
            print(
                f"Tree Size = {branchingFactorList[0]} , Non Leaf Nodes = {branchingFactorList[1]} ,"
                f" cut-offs = {branchingFactorList[2]} , branching factor = {branchingFactorList[3]} ")
            print(
                f"max_depth_explored  {stats_returned[0]} , Number of leaf nodes = {len(stats_returned[1])} , cut"
                f"-offs per level = {stats_returned[2]}  ")

        b = datetime.datetime.now()
        c = b - a
        print(f"AI took {c.total_seconds()} seconds to find the best move")
        print("Slot-------->", slot)

        play_another_time = self.board.board_turn(slot, True)[4]
        self.board.print_board()

        if play_another_time and max(self.board.opponent_side) != 0:
            self.board.opponent_side.reverse()
            self.Ai_turn()

    def end_game(self):
        print("do you want to play another time press \"s\" if you want exit press \"e\"")
        a = input()
        if a == 's':
            self.__init__()
        elif a == 'e':
            exit()
        else:
            self.end_game()


class Board:
    def __init__(self, stealing):

        self.my_side = [4, 4, 4, 4, 4, 4]
        self.opponent_side = [4, 4, 4, 4, 4, 4]
        self.my_score = 0
        self.opponent_score = 0
        self.isStealing = stealing

        if self.isStealing:
            self.turn = take_turn_with_stealing()
        else:
            self.turn = take_turn_no_stealing()

    def get_board(self):
        a = self.opponent_side.copy()
        currentBoard = self.my_side + a
        score = [self.my_score, self.opponent_score]
        return [currentBoard, score]

    def print_board(self, isReverse=False):
        if isReverse:
            self.opponent_side.reverse()

        my_str = stringfy(self.my_side)
        opponent_str = stringfy(self.opponent_side)
        print("\t\t\tAI\n")
        print("    " + opponent_str)
        print(str(self.opponent_score) + "                           " + str(self.my_score))
        print("    " + my_str)
        print("\n\t\t\tUser")
        print("\n")

        if isReverse:
            self.opponent_side.reverse()

    def empty_side(self):
        # this wil return if one of  board sides is empty and add other gems in score of the other user
        user_has_gems = any(self.my_side)
        opp_has_gems = any(self.opponent_side)
        if user_has_gems and opp_has_gems:
            return False
        elif user_has_gems and not opp_has_gems:
            self.my_score += sum(self.my_side)
            return True
        else:
            self.opponent_score += sum(self.opponent_side)

            return True

    def get_current_winner(self):

        if self.my_score > self.opponent_score:
            return "you won score is {} :{}".format(self.my_score, self.opponent_score)
        elif self.my_score < self.opponent_score:
            return "you lost score is {} :{}".format(self.my_score, self.opponent_score)
        else:
            return " draw score is {} :{}".format(self.my_score, self.opponent_score)

    def board_turn(self, slot, isFlip=False):

        if isFlip:
            [tempOpponent_side, self.opponent_score, tempMy_side, self.my_score, Next] = self.turn.take_turn(
                self.opponent_side,
                self.my_side,
                self.opponent_score,
                self.my_score,
                int(slot))
            tempOpponent_side.reverse()
        else:
            temp = list(self.opponent_side)
            temp.reverse()
            [tempMy_side, self.my_score, tempOpponent_side, self.opponent_score, Next] = self.turn.take_turn(
                self.my_side,
                temp,
                self.my_score,
                self.opponent_score,
                int(slot))

        self.my_side = list(tempMy_side)
        self.opponent_side = list(tempOpponent_side)

        return [self.my_side, self.my_score, self.opponent_side, self.opponent_score, Next]


def stringfy(arr):
    # takes an array and convert it into a string
    st = ""
    for i in arr:
        st += str(i) + "  "
    return st


class take_turn_no_stealing:

    def take_turn(self, my_side, opponent_side, my_score, opponent_score, slot):
        opponent = list(opponent_side)
        circular_array = my_side + [my_score] + opponent
        gems_value = circular_array[slot - 1]
        Next_turn = ((gems_value + slot) % len(circular_array) == 7)
        circular_array[slot - 1] = 0

        for i in range(gems_value):
            circular_array[(slot + i) % len(circular_array)] += 1
        opponent = list(circular_array[7:13])

        return [circular_array[0:6], circular_array[6], opponent, opponent_score, Next_turn]


class take_turn_with_stealing:

    def take_turn(self, my_side, opponent_side, my_score, opponent_score, slot):

        opponent = list(opponent_side)
        circular_array = my_side + [my_score] + opponent
        gems_value = circular_array[slot - 1]
        Next_turn = ((gems_value + slot) % len(circular_array) == 7)
        circular_array[slot - 1] = 0

        for i in range(gems_value - 1):
            circular_array[(slot + i) % len(circular_array)] += 1
        last_item_Position_in_board = (slot + gems_value - 1) % len(circular_array)

        if self.will_i_steal(circular_array, gems_value, slot):
            other_side_pos = 12 - last_item_Position_in_board
            gems_other_side = circular_array[other_side_pos]
            circular_array[other_side_pos] = 0
            circular_array[6] += (gems_other_side + 1)
        else:
            circular_array[last_item_Position_in_board] += 1
        opponent = list(circular_array[7:13])

        return [circular_array[0:6], circular_array[6], opponent, opponent_score, Next_turn]

    def will_i_steal(self, circular_array, gems_value, slot):
        """
            i will steal when last slot is empty on myside and has gens on other side of board
        """
        last_item_Position_in_board = (slot + gems_value - 1) % len(circular_array)
        last_slot_empty = (circular_array[last_item_Position_in_board] == 0)

        if last_slot_empty:
            last_slot_is_on_my_side = last_item_Position_in_board < 6

            if last_slot_is_on_my_side:
                other_side_pos = 12 - last_item_Position_in_board  # 13 is size of circular array- the score
                other_side_has_gems_is_not_empty = (circular_array[other_side_pos] != 0)

                if other_side_has_gems_is_not_empty:
                    print("stole")
                    return True
        return False


if __name__ == '__main__':
    Game()
