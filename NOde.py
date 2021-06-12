from utility import Utility


# player 0 human

# player 1 AI

class stats:
    def __init__(self, max_depth):
        self.cut_off = [0 for _ in range(max_depth)]
        self.leaf_values_evaluated = []
        self.max_depth_explored = 0

    def inc_cut_off(self, depth):
        self.cut_off[depth] += 1
        if depth > self.max_depth_explored:
            self.max_depth_explored = depth

    def leaf_node_eval(self, index, score):
        self.leaf_values_evaluated.append([index, score])

    def return_stats(self):
        if self.leaf_values_evaluated[len(self.cut_off) - 1] != 0: self.max_depth_explored = len(self.cut_off)
        return [self.max_depth_explored, self.leaf_values_evaluated, self.cut_off]


class Node:
    treeSize = 0
    nonLeafNodes = 0
    cutOffs = 0

    def __init__(self, data, player, score, stat, depth=0, maxDepth=1, index=None):

        Node.treeSize += 1
        Node.nonLeafNodes += 1
        self.children = []
        self.index = index
        self.NextMove = None
        self.alpha = float('-inf')
        self.beta = float('inf')
        self.score = score  # list of 2 contains score of each player
        self.data = data
        self.evaluateValue = None
        self.player = player
        self.depth = depth
        self.maxDepth = maxDepth
        self.cutoff = False
        self.leaves = 0
        self.stats = stat

    def alphaBeta(self, alpha, beta):

        if self._isLeaf(self):
            Node.nonLeafNodes -= 1
            return self.evaluateValue, self.alpha, self.beta

        self.NextMove = self.children[0]
        self.alpha = alpha
        self.beta = beta

        for i, l in enumerate(self.children):
            value, alphaT, betaT = l.alphaBeta(self.alpha, self.beta)

            if self.player == 1:
                if value is None: value = float('-inf')
                if betaT == float('inf'): betaT = float('-inf')
                self.alpha = max(value, self.alpha, betaT)
                if l.beta > self.NextMove.beta:
                    self.NextMove = l
            else:
                if value is None: value = float('inf')
                if alphaT == float('-inf'): alphaT = float('inf')
                self.beta = min(value, self.beta, alphaT)
                if l.alpha < self.NextMove.alpha:
                    self.NextMove = l

            if self.alpha >= self.beta:
                self.cutoff = True
                Node.cutOffs += 1
                Node.nonLeafNodes -= (len(self.children))
                Node.nonLeafNodes += (i + 1)
                self.stats.inc_cut_off(self.depth)
                break

        return self.evaluateValue, self.alpha, self.beta

    def insert(self, stealing):

        if self.depth == self.maxDepth:
            self.evaluateValue = Utility(self)
            self.stats.leaf_node_eval(self.index, self.evaluateValue)
            return

        for l in self.nextMovePred(self.data, self.player, self.score, stealing):
            self.children.append(
                Node(l["data"], l["player"], l["Score"], self.stats, self.depth + 1, self.maxDepth, l["index"]))

        for l in self.children:
            l.insert(stealing)

    def printTree(self):

        if self._isLeaf(self): return
        print("data--->", self.data, self.score, self.player, self.alpha, self.beta, self.evaluateValue, self.cutoff)

        for l in self.children:
            print(" child--->", l.data, l.score, l.player, l.alpha, l.beta, l.evaluateValue, l.cutoff)

        for l in self.children:
            l.printTree()

    def nextMovePred(self, data, player, score, stealing):  # get list of all possible moves

        MoveList = []

        for i, l in zip(range(player * 6, player * 6 + 6), data[player * 6: player * 6 + 6]):

            if not l:
                continue

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

            if stealing and List[spot] == 1 and List[(spot + 6) % 12] != 0:
                List[spot] = 0
                spot = (spot + 6) % 12
                ScoreInc[player] += List[spot] + 1
                List[spot] = 0

            node["data"] = List
            node["player"] = PT
            node["Score"] = ScoreInc
            node["index"] = i % 6
            MoveList.append(node)

        return MoveList

    def _isLeaf(self, node):

        if not node.children:
            return True
        return False


# kb=board
# kp=0
# ks=[0,0]
def ai_choice(kb, ks, stealing, kp=1, maxDepth=1):
    Node.treeSize = 0
    Node.nonLeafNodes = 0
    Node.cutOffs = 0
    stat = stats(maxDepth)
    c = Node(kb, kp, ks, stat, maxDepth=maxDepth)
    c.insert(stealing)
    c.alphaBeta(float('-inf'), float('inf'))
    k = c.NextMove

    return [k.index, stat.return_stats(),
            [Node.treeSize - 1, Node.nonLeafNodes, Node.cutOffs, (Node.treeSize - 1) / Node.nonLeafNodes]]
