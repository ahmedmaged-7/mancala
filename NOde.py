import threading
import time
board = [4, 4, 4, 4, 4, 4,
         4, 4, 4, 4, 4, 4]

"""import sys
def ono ():
    while True:
        char = sys.stdin.read(1)
        print ("You pressed: "+char)
        char = sys.stdin.read(1)
t1 = threading.Thread(target=ono)
t1.start()
"""

#player 0 humano

#player 1 AI
"""
The branching factor can be cut down by a pruning algorithm.
The average branching factor can be quickly calculated as the number of non-root nodes (the size of the tree, minus one; or the number of edges) divided by the number of non-leaf nodes (the number of nodes with children). 

"""

class stats:
   def __init__(self,max_depth):
         self.cut_off=[0 for x in range(max_depth)] 
         self.leaf_values_evaluated=[]
         self.max_depth_explored=0 #i am not so sure of this
   def inc_cut_off(self,depth):
         self.cut_off[depth]+=1
         if(depth>self.max_depth_explored):
             self.max_depth_explored=depth
   def leaf_node_eval(self,index,score):
           self.leaf_values_evaluated.append([index,score])

   def return_stats(self):
       return [self.max_depth_explored,self.leaf_values_evaluated,self.cut_off]       

class Node:
    def __init__(self, data, player, score, max_depth,stats,depth=0,index=None):
        self.children = []
        self.index=index
        self.NextMove=None
        self.nextMoveIndex=None
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.score = score  # list of 2 contains score of each player
        self.data = data
        self.evaluateValue = None
        self.player = player
        self.depth = depth
        self.cutoff=False
        self.max_depth=max_depth
        self.stats=stats
        

    def AlphaBeta(self,alpha,beta):
        if   self._IsLeaf(self):
            return self.evaluateValue,self.alpha,self.beta
        self.NextMove=self.children[0]
        self.nextMoveIndex=0
        self.alpha=alpha
        self.beta=beta
        for i,l in enumerate(self.children):
            value,alphaT,betaT = l.AlphaBeta(self.alpha,self.beta)
            if self.player == 1:
                if value==None:value=float('-inf')
                if betaT==float('inf'):betaT=float('-inf')
                self.alpha = max(value, self.alpha,betaT)
                if l.beta > self.NextMove.beta :
                    self.NextMove = l
                    self.nextMoveIndex=i
            else:
                if value==None:value=float('inf')
                if alphaT==float('-inf'):alphaT=float('inf')
                self.beta = min(value, self.beta,alphaT)
                if l.alpha < self.NextMove.alpha :
                    self.NextMove = l
                    self.nextMoveIndex=i

            if self.alpha >= self.beta :
                self.cutoff = True
                self.stats.inc_cut_off(self.depth)
                #print("cutoff")
                break
                #return self.evaluateValue,self.alpha,self.beta
        return self.evaluateValue,self.alpha,self.beta
    def insert(self):
        if self.depth == self.max_depth:
            self.evaluateValue = self.Utility(self)
            self.stats.leaf_node_eval(self.index,self.evaluateValue )
            return
        #print("data--->", self.data, self.score, self.player)
        for l in self.NextMovePred(self.data, self.player, self.score):
            self.children.append(Node(l["data"], l["player"], l["Score"], self.max_depth,self.stats,self.depth + 1,l["index"]))
        for l in self.children:
            pass#print(" child--->", l.data, l.score, l.player)
        for l in self.children:
            l.insert()
    def getNextMove(self):
        pass
    """        if not self.children : return None
        NextMove=self.children[0]
        for l in self.children[1:]:
            if  self.player :   #AI get max  score
                if NextMove.beta < l.beta:
                    NextMove=l
            else   :   #human get min score
                if NextMove.alpha > l.alpha:
                    NextMove=l
        return NextMove"""
    def printTree(self):
        if self._IsLeaf(self):return
        print("data--->", self.data, self.score, self.player,self.alpha,self.beta,self.evaluateValue,self.cutoff)
        for l in self.children:
            print(" child--->", l.data, l.score, l.player,l.alpha,l.beta,l.evaluateValue,l.cutoff)
        for l in self.children:
            l.printTree()
    def Utility(self, data):
        Score=0
        Score-=sum(data.data[0:6])
        Score += sum(data.data[6:])
        for i,l in enumerate(data.data[0:6]):
            if l + i > 6:
                Score-=1
        for i, l in enumerate(data.data[6:]):
            if l + i > 6:
                Score += 1

        return Score+4*(data.score[1] - data.score[0])


    def NextMovePred(self, data, player, score): #get list of all possible moves
        MoveList = []
        ScoreInc = [0, 0]
        for i, l in zip(range(player * 6, player * 6 + 6), data[player * 6: player * 6 + 6]):
            if not l: continue
            node = dict()
            List = data.copy()
            ScoreInc = score.copy()
            spot = i
            List[i] = 0
            PT = player
            if l + i > 6 * player + 6:
                l -= 1
                ScoreInc[player] += 1
                PT = player ^ 1
            elif l + i == 6 * player + 6:
                l -= 1
                ScoreInc[player] += 1
            else:
                PT = player ^ 1
            for _ in range(l):
                spot = (spot + 1) % 12
                List[spot] += 1
            if List[spot]==1 and List[(spot+6)%12] !=0 :
                List[spot]=0
                spot=(spot+6)%12
                ScoreInc[player] +=List[spot]+1
                List[spot]=0
            node["data"] = List
            node["player"] = PT
            node["Score"] = ScoreInc
            node["index"] = i%6
            MoveList.append(node)
        return MoveList
    def get_cut_off(self):
      return self.cut_off_value
    def _IsLeaf(self, node):
        if not node.children:
            return True
        return False

#kb=board
#kp=0
#ks=[0,0]
def ai_choice(kb,ks,max_depth,kp=1):
    stat=stats(max_depth)
    c = Node(kb, kp,ks,max_depth,stat)
    c.insert()
    c.AlphaBeta(float('-inf'),float('inf'))
    k=c.NextMove
    if k == None  :
        c.score[0]+=sum(c.data[0:6])
        c.score[1] += sum(c.data[6:])
        c.data= [0] * 12


    print("list that contain cut off at levels ")
    print(stat.return_stats())
    #print(k.data,k.score,k.player)
    if kp ==k.player :
        pass
    kb=k.data
    kp=k.player
    ks=k.score

    return k.index
