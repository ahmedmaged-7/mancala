board = [4, 4, 4, 4, 4, 4,
         4, 4, 4, 4, 4, 4]
#player 1 AI
#player 0 human
class Node:
    def __init__(self, data,player,score,depth,alpha=None,beta=None):
        self.children = []
        self.alpha=None
        self.beta=None
        self.score=score
        self.data = data
        self.player=player
        self.depth=depth
    def insert(self): 
        if self.depth==5:return
        print("data--->",self.data,self.score,self.player)
        for l in self.NextMovePred(self.data,self.player,self.score):
            self.children.append(Node(l["data"],l["player"],l["Score"],self.depth+1))
        for l in self.children:
            print(" child--->",l.data,l.score,l.player)
        for l in self.children:
            l.insert()
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
   
c=Node(board,0,[0,0],0)
c.insert()
