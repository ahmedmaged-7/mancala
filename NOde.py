import random
board = [4, 4, 4, 4, 4, 4,
         4, 4, 4, 4, 4, 4]

class Node:
    def __init__(self, data,player,score,depth,alpha=None,beta=None):
        self.children = []
        self.alpha=None
        self.beta=None
        self.score=score # list of 2 contains score of each player
        self.data = data
        self.evaluateValue=None
        self.player=player
        self.depth=depth
    def insert(self):  # Compare the new value with the parent node
        if self.depth==2:
            self.evaluateValue=self.Utility(self.data)
            return
        print("data--->",self.data,self.score,self.player)
        for l in self.NextMovePred(self.data,self.player,self.score):
            self.children.append(Node(l["data"],l["player"],l["Score"],self.depth+1))
        for l in self.children:
            print(" child--->",l.data,l.score,l.player)
        for l in self.children:
            l.insert()
    def Utility(self,data):
        return random.randint(0,50)
    def NextMovePred(self,data,player,score):
        MoveList=[]
        ScoreInc=[0,0]
        for i,l in zip(range(player*6,player*6+6),data[player*6 : player*6+6]):
            if not l : continue
            node=dict()
            List = data.copy()
            ScoreInc=score.copy()
            spot = i
            List[i] = 0
            PT=player
            if l +i > 6 * player +6:
                l-=1
                ScoreInc[player]+=1
                PT=player ^1
            elif l +i == 6 * player +6:
                l-=1
                ScoreInc[player]+=1
            else : PT= player ^1
            for _ in range(l):
                spot=(spot+1)%12
                List[spot]+=1
            node["data"]=List
            node["player"]=PT
            node["Score"]=ScoreInc
            MoveList.append(node)
        return MoveList
    def _IsLeaf(self,node):
        if not node.children:
            return True
        return False
    def synset_count(self):
        if not self.children :return 1
        for z in self.children:
            if z.children:
                return 0
        return 1
    def synset_no(self):
        if not self.children:return 0
        count =0
        for a in self.children:
            count+= a.synset_no()
        if not count : return 1
        #for b in self.children:
        #    b.synset_no()
        return count

c=Node(board,0,[0,0],0)
c.insert()
