class game:
     def __init__(self):
         print("to play mancala with stealing enter y without stealing enter any key")
         user_choice=input()
         if(user_choice=='y' ):
             self.board=board(stealing=True)
             print("you choosed playing with stealing")
         else:
             self.board=board(stealing=False)
             print("you choosed playing without stealing")
         self.loop()
     def loop(self):
         while(self.check_winner()==False):
             self.user_turn()
             self.check_winner()
             self.Ai_turn()
         self.end_game()    
     def user_turn(self,turn_board=True):
         if(turn_board):             
             print("user flipped")
             self.board.board_flip() 
         self.board.print_board() 
         print("choose a slot to play")
         slot=input()
         play_another_time=self.board.board_turn(slot)[4]
         self.board.print_board() 
         if(play_another_time):
              self.user_turn(False) 
     def check_winner(self):
         if(self.board.empty_side()):
             print(self.board.get_current_winner())
         else:
             return False

     def Ai_turn(self,turn_board=True):
         if(turn_board):
             pass
             print("AI flipped")
             self.board.board_flip()
         self.board.print_board() 
         slot=input()
         play_another_time=self.board.board_turn(slot)[4]
         if(play_another_time):
              self.Ai_turn(False)
             
     def end_game(self):
          print("do you want to play another time press s if you want exit press e")
          a=input()
          if(a=='s'):
              game()
          elif(a=='e'):
              exit()
          else:
              self.end_game()


class board:
    def __init__(self,stealing):
        self.my_side=[4,4,4,4,4,4]
        self.opponent_side=[4,4,4,4,4,4]
        self.my_score=0
        self.opponent_score=0
        if (stealing):
           self.turn=take_turn_with_stealing()
        else:
            self.turn=take_turn_no_stealing()
        
    def print_board(self):
            my_str=stringfy(self.my_side)
            opponent_str=stringfy(self.opponent_side)
            print("    "+opponent_str )
            print(str(self.opponent_score)+"                           " +str(self.my_score))
            print("    "+my_str )

    def empty_side(self):
           #this wil return if one of  board sides is empty and add other gems in score of the other user 
           user_has_gems=any(self.my_side)
           opp_has_gems=any(self.opponent_side)
           if(user_has_gems and opp_has_gems):
               return False
           elif(user_has_gems and not(opp_has_gems)):
               self.my_score+=sum(self.my_side)
               return True
           else:
               self.opponent_score+=sum(self.opponent_side)

               return True
    def get_current_winner(self):
        
        if(my_score>opponent_score):
            return "you won score is {} :{}".format(my_score,opponent_score)
        elif(my_score<opponent_score):
            return "you lost score is {} :{}".format(my_score,opponent_score)
        else:
            return " draw score is {} :{}".format(my_score,opponent_score)
        
    def board_flip(self):
          self.opponent_side.reverse()
          self.my_side.reverse()
          self.opponent_side,self.opponent_score,self.my_side,self.my_score=self.my_side,self.my_score,self.opponent_side,self.opponent_score
          return self
               
    def board_turn(self,slot):
       [ self.my_side,self.my_score,self.opponent_side,self.opponent_score,Next]= self.turn.take_turn(self.my_side,self.opponent_side,self.my_score,self.opponent_score,int(slot))
       return [ self.my_side,self.my_score,self.opponent_side,self.opponent_score,Next]
  



def stringfy(arr):
#takes an array and convert it into a string
    st=""
    for i in arr:
        st+=str(i)+"  "
    return st    


class take_turn_no_stealing:

    def take_turn(self,my_side,opponent_side,my_score,opponent_score,slot):
        circular_array=my_side+[my_score]+opponent_side
        gems_value= circular_array[slot-1]
        Next_turn=((gems_value+slot)%len(circular_array)==7)
        circular_array[slot-1]=0
        for i in range(gems_value):
            circular_array[(slot+i)%len(circular_array)]+=1
        return [circular_array[0:6],circular_array[6],circular_array[12:6:-1],opponent_score,Next_turn]
         
class take_turn_with_stealing:
    
    def take_turn(self,my_side,opponent_side,my_score,opponent_score,slot):
        circular_array=my_side+[my_score]+opponent_side
        gems_value= circular_array[slot-1]
        Next_turn=((gems_value+slot)%len(circular_array)==7)
        circular_array[slot-1]=0
        for i in range(gems_value-1):
            circular_array[(slot+i)%len(circular_array)]+=1
        last_item_Position_in_board=(slot+gems_value-1)%len(circular_array)
        if(self.will_i_steal(circular_array,gems_value,slot)):
                other_side_pos=12-(last_item_Position_in_board)
                gems_other_side=circular_array[other_side_pos]
                circular_array[other_side_pos]=0
                circular_array[6]+=(gems_other_side+1)
        else:
            circular_array[last_item_Position_in_board]+=1
            
        return [circular_array[0:6],circular_array[6],circular_array[12:6:-1],opponent_score,Next_turn]
   




    def will_i_steal(self,circular_array,gems_value,slot):
        """
i will steal when last slot is empty on myside and has gens on other side of board
        """
        last_item_Position_in_board=(slot+gems_value-1)%len(circular_array)
        last_slot_empty=(circular_array[last_item_Position_in_board]==0)
        if(last_slot_empty):
           print("last_slot_empty")  
           last_slot_is_on_my_side=last_item_Position_in_board<6
           if(last_slot_is_on_my_side):
              print(last_item_Position_in_board)  
              print(circular_array)   
              other_side_pos=12-(last_item_Position_in_board) #13 is size of circular array- the score
              print(other_side_pos)
              
              other_side_has_gems_is_not_empty=(circular_array[other_side_pos]!=0)
              if(other_side_has_gems_is_not_empty):
                  print("stole")
                  return True
        return False
        
if __name__ == '__main__':
	
	game() 

