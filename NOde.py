import random

board = [4, 4, 4, 4, 4, 4,
         4, 4, 4, 4, 4, 4]

#player 0 human
#player 1 AI 
class Node:
    def __init__(self, data, player, score, depth):
        self.children = []
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.score = score  # list of 2 contains score of each player
        self.data = data
        self.evaluateValue = None
        self.player = player
        self.depth = depth
        self.cutoff=False
    def AlphaBeta(self,alpha,beta):
        if self.evaluateValue != None :
            return self.evaluateValue,self.alpha,self.beta
        self.alpha=alpha
        self.beta=beta
        for l in self.children:
            value,alphaT,betaT = l.AlphaBeta(self.alpha,self.beta)
            if self.player == 1:
                if value==None:value=float('-inf')
                if betaT==float('inf'):betaT=float('-inf')
                self.alpha = max(value, self.alpha,betaT)
            else:
                if value==None:value=float('inf')
                if alphaT==float('-inf'):alphaT=float('inf')
                self.beta = min(value, self.beta,alphaT)
            if self.alpha >= self.beta :
                self.cutoff = True
                print("cutoff")
                break
                #return self.evaluateValue,self.alpha,self.beta
        return self.evaluateValue,self.alpha,self.beta
    def insert(self):  
        if self.depth == 2:
            self.evaluateValue = self.Utility(self.data)
            return
        print("data--->", self.data, self.score, self.player)
        for l in self.NextMovePred(self.data, self.player, self.score):
            self.children.append(Node(l["data"], l["player"], l["Score"], self.depth + 1))
        for l in self.children:
            print(" child--->", l.data, l.score, l.player)
        for l in self.children:
            l.insert()
    def getNextMove(self):
        NextMove=self.children[0]
        for l in self.children[1:]:
            if  self.player :   #AI get max  score
                if NextMove.beta < l.beta:
                    NextMove=l
            else   :   #human get min score
                if NextMove.alpha > l.alpha:
                    NextMove=l
        return NextMove
    def printTree(self):
        if self._IsLeaf(self):return
        print("data--->", self.data, self.score, self.player,self.alpha,self.beta,self.evaluateValue,self.cutoff)
        for l in self.children:
            print(" child--->", l.data, l.score, l.player,l.alpha,l.beta,l.evaluateValue,l.cutoff)
        for l in self.children:
            l.printTree()
    def Utility(self, data):
        return random.randint(0, 500)

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
            node["data"] = List
            node["player"] = PT
            node["Score"] = ScoreInc
            MoveList.append(node)
        return MoveList 

    def _IsLeaf(self, node):
        if not node.children:
            return True
        return False


c = Node(board, 1, [0, 0], 0)
c.insert()
c.AlphaBeta(float('-inf'),float('inf'))
print("----------------\n")
c.printTree()
k=c.getNextMove()
print(k.data,k.score)
