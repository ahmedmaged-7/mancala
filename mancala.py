import os.path
import pickle

from NOde import *


class Game:
    def __init__(self):
        self.max_depth=5
        self.gameRound = 1
        self.board = Board(True)

        print("New game : enter \"n\" \nLoad game : enter \"l\" ")
        new_game = input()

        if new_game == "n":
            self.playNew()
        else:
            self.loadGame()

    def playNew(self):

        print("To play Mancala with stealing enter \"y\" without stealing enter any key")
        user_choice = input()
        if user_choice == 'y':
            print("you chose playing with stealing")
        else:
            self.board.isStealing = False
            print("you chose playing without stealing")
        print("choose the diffculty level :enter e for easy m for normal or enter h for hard") 
        diffculty = input()
        if(diffculty=="e"):
             self.max_depth=1
        elif(diffculty=="h"):
             self.max_depth=7   # i choosed 8 because anything after that will excede the time limit
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
        #tempMySide.reverse()
        #tempOpSide.reverse()

        with open(fileName, 'wb') as file:
            pickle.dump({"my_side": tempMySide, "op_side": tempOpSide, "myScore": tempMyScore, "opScore": tempOpScore,
                         "isStealing": isStealing, "gameRound": gameRound},
                        file)
        print(pickle.load(open(fileName, "rb")))

    def loadGame(self):

        print("Enter file name to be loaded : ")
        filePath = "saves/" + input() + ".mancala.pkl"

        if os.path.isfile(filePath):
            state = pickle.load(open(filePath, "rb"))
            self.board.my_side = state["my_side"]
            self.board.opponent_side = state["op_side"]
            self.board.my_score = state["myScore"]
            self.board.opponent_score = state["opScore"]
            self.board.isStealing = state["isStealing"]
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
            self.check_winner()
            self.Ai_turn(self.max_depth)
            self.board.print_board()
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
            # self.board.board_flip()
        self.board.print_board()
        print("choose a slot to play")
        slot = input()
        play_another_time = self.board.board_turn(slot)[4]
        # self.board.print_board()
        if play_another_time:
            self.user_turn(False)

    def check_winner(self):
        if self.board.empty_side():
            print(self.board.get_current_winner())
        else:
            return False

    def Ai_turn(self, max_depth,turn_board=True):
        # if turn_board:
        #     currentBoard, score = self.board.get_board()
        #     print("AI flipped")
        #     self.board.board_flip()
        # else:
        #     self.board.board_flip()
        #     currentBoard, score = self.board.get_board()
        #     self.board.board_flip()
        currentBoard, score = self.board.get_board()
        # self.board.print_board()
        # slot = input()
        slot = ai_choice(currentBoard, score,max_depth) + 1
        print("Slot-------->", slot)
        play_another_time = self.board.board_turn(slot, True)[4]
        self.board.print_board()
        print("\n")
        if play_another_time:
            self.Ai_turn(max_depth,False)

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
        a.reverse()
        board = self.my_side + a
        score = [self.my_score, self.opponent_score]
        return [board, score]

    def print_board(self):
        my_str = stringfy(self.my_side)
        opponent_str = stringfy(self.opponent_side)
        print("\n")
        print("AI\n")
        print("    " + opponent_str)
        print(str(self.opponent_score) + "                                    " + str(self.my_score))
        print("    " + my_str)
        print("                                      User\n")
        print("\n")

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

    def board_flip(self):
        self.opponent_side.reverse()
        self.my_side.reverse()

        tempSide = list(self.opponent_side)
        tempScore = self.opponent_score

        self.opponent_side, self.opponent_score, self.my_side, self.my_score = (
            list(self.my_side), self.my_score, list(tempSide), tempScore)
        return self

    def board_turn(self, slot, isFlip=False):
        if isFlip:
            self.opponent_side.reverse()
            [tempOpponent_side, self.opponent_score, tempMy_side, self.my_score, Next] = self.turn.take_turn(
                self.opponent_side,
                self.my_side,
                self.opponent_score,
                self.my_score,
                int(slot))
            tempOpponent_side.reverse()
        else:
            [tempMy_side, self.my_score, tempOpponent_side, self.opponent_score, Next] = self.turn.take_turn(
                self.my_side,
                self.opponent_side,
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
        st += str(i) + "    "
    return st


class take_turn_no_stealing:

    def take_turn(self, my_side, opponent_side, my_score, opponent_score, slot):
        opponent = list(opponent_side)
        # opponent.reverse()
        circular_array = my_side + [my_score] + opponent
        gems_value = circular_array[slot - 1]
        Next_turn = ((gems_value + slot) % len(circular_array) == 7)
        circular_array[slot - 1] = 0
        for i in range(gems_value):
            circular_array[(slot + i) % len(circular_array)] += 1
        opponent = list(circular_array[7:13])
        # opponent.reverse()
        return [circular_array[0:6], circular_array[6], opponent, opponent_score, Next_turn]


class take_turn_with_stealing:

    def take_turn(self, my_side, opponent_side, my_score, opponent_score, slot):
        # print(my_side)
        # print(opponent_side)
        opponent = list(opponent_side)
        # opponent.reverse()
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
        # print(opponent)
        # opponent.reverse()
        # print(opponent)
        # print(circular_array[0:6])
        # print(opponent)
        return [circular_array[0:6], circular_array[6], opponent, opponent_score, Next_turn]

    def will_i_steal(self, circular_array, gems_value, slot):
        """
i will steal when last slot is empty on myside and has gens on other side of board
        """
        last_item_Position_in_board = (slot + gems_value - 1) % len(circular_array)
        last_slot_empty = (circular_array[last_item_Position_in_board] == 0)
        if last_slot_empty:
            #print("last_slot_empty")
            last_slot_is_on_my_side = last_item_Position_in_board < 6
            if last_slot_is_on_my_side:
                #print(last_item_Position_in_board)
                #print(circular_array)
                other_side_pos = 12 - last_item_Position_in_board  # 13 is size of circular array- the score
                #print(other_side_pos)

                other_side_has_gems_is_not_empty = (circular_array[other_side_pos] != 0)
                if other_side_has_gems_is_not_empty:
                    #print("stole")
                    return True
        return False


if __name__ == '__main__':
    Game()
