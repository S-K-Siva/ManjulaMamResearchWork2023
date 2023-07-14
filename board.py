from Nodes import Node
from packet import packet
import random
import math as m
class Board:

    def __init__(self):
        self.boardSize = 11
        self.m = 11
        self.offSet = 50
        self.successfulPacketsCount = 0
        self.failurePacketsCount = 0
        self.attackerId = -1
        self.maxValue = self.offSet * (self.boardSize // 2)
        self.board = [[Node() for _ in range(self.boardSize)] for _ in range(self.boardSize)]
        self.nodeById = dict()
        self.sourceNode = None
        self.phantomSquare1 = []
        self.phantomSquare2 = []
        self.compromisedNodes = []
        self.packet = packet()
        self.initialize_board()
        self.attackerNode = None
        self.file = open('attackerMovement.txt', 'w')

    def __del__(self):
        self.file.close()
    def initializeAttacker(self):
        self.board[self.boardSize//2][self.boardSize//2].isAttacker = True
        self.attackerNode = self.board[self.boardSize//2][self.boardSize//2]

    def moveAttacker(self,fromNode,toNode):
        self.file.write(f"Attacker moving from {fromNode.id} to {toNode.id}\n")

        print(type(fromNode))
        print(type(toNode))
        fromNode.isAttacker = False
        toNode.isAttacker = True
        self.attackerNode = toNode

    def initialize_board(self):
        rowValue = self.offSet * (self.boardSize // 2)
        colValue = self.offSet * (self.boardSize // 2)
        nodeCount = 1
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                self.board[i][j].id = nodeCount
                self.board[i][j].i = i
                self.board[i][j].j = j
                self.nodeById[nodeCount] = self.board[i][j]
                nodeCount += 1
                if i < self.m // 2:
                    # TOP-SIDE
                    if j < self.m // 2:
                        # IInd Quadrant
                        self.board[i][j].xAxis = -1 * rowValue
                        self.board[i][j].yAxis = colValue
                        if i == 0 and j == 0:
                            # top-left-corner
                            self.board[i][j].closureNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j + 1])
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                        elif i == 0:
                            # whole top edge case
                            self.board[i][j].equalNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j + 1])
                        elif j == 0:
                            # whole left-side of Quadrant - II
                            self.board[i][j].equalNeighbour.append(self.board[i - 1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i - 1][j + 1])
                        else:
                            # each node that is not on the edges will have 8 neighbors
                            self.board[i][j].equalNeighbour.append(self.board[i - 1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i - 1][j + 1])
                            self.board[i][j].furtherNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].furtherNeighbour.append(self.board[i - 1][j - 1])
                            self.board[i][j].furtherNeighbour.append(self.board[i + 1][j - 1])
                    # Ist Quadrant
                    if j > self.m // 2:
                        self.board[i][j].xAxis = rowValue
                        self.board[i][j].yAxis = colValue
                        if i == 0 and j == self.m - 1:
                            # top-right-corner
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j - 1])
                        elif i == 0:
                            # whole top
                            self.board[i][j].equalNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j + 1])
                        elif j == self.m - 1:
                            # whole right-side of quadrant-1
                            self.board[i][j].equalNeighbour.append(self.board[i - 1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i - 1][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j - 1])
                        else:
                            # the each nodes not in the edges will have 8 neighbors.
                            self.board[i][j].closureNeighbour.append(self.board[i][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i + 1][j - 1])
                            self.board[i][j].closureNeighbour.append(self.board[i - 1][j - 1])
                            self.board[i][j].equalNeighbour.append(self.board[i - 1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i + 1][j])
                            self.board[i][j].furtherNeighbour.append(self.board[i][j + 1])
                            self.board[i][j].furtherNeighbour.append(self.board[i + 1][j + 1])
                            self.board[i][j].furtherNeighbour.append(self.board[i - 1][j + 1])
                    # y-axis
                    if j == self.m // 2:
                        self.board[i][j].xAxis = 0
                        if colValue <= self.offSet:
                            self.board[i][j].yAxis = rowValue

                        # Getting 3 ways of Neighbours Process...
                        if i == 0:
                            #top edge case
                            #equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i][j-1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j+1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                        else:
                            # the nodes which lies in y-axis excluding edge case, will have 8 neighbours
                            # forther neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j+1])
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i][j-1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j+1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                elif i > self.m//2:
                    # BOTTOM SIZE
                    if j < self.m//2:
                        self.board[i][j].xAxis = -1 * rowValue
                        self.board[i][j].yAxis = -1 * colValue

                        if i == self.m-1 and j == 0:
                            # bottom-left-corner
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                        elif i == self.m - 1:
                            # bottom-whole-edge-case
                            # equal neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                        elif j == 0:
                            # whole left-edge case of Quadrant-III
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                        else:
                            # each element that are not in edges will have 8 neighbours
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                            # further neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i][j-1])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j-1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                    # IVth Quandrant
                    if j > self.m//2:
                        self.board[i][j].xAxis = rowValue
                        self.board[i][j].yAxis = -1 * colValue
                        # getting 3 ways of neighbours

                        if i == self.m - 1 and j == self.m-1:
                            # bottom-right-corner-case
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                        elif j == self.m - 1:
                            # bottom-whole-right-side-edge-case
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                        elif i == self.m - 1:
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i][j-1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j+1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                        else:
                            # each node that doesn't lies onthe edge will have 8 neighbours
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                            self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                            # further neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i][j+1])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j+1])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j+1])
                    if j == self.m // 2:
                        self.board[i][j].xAxis = 0
                        self.board[i][j].yAxis = -1 * rowValue
                        # Getting all 3 ways of neighbours
                        if i == self.m - 1:
                            # edge case (bottom)
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i][j-1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j+1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                        else:
                            # each node that not lie in y-axis will have 8 neighbours
                            # equal neighbour
                            self.board[i][j].equalNeighbour.append(self.board[i][j-1])
                            self.board[i][j].equalNeighbour.append(self.board[i][j+1])
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            # further neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j+1])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j-1])
                # x-axis
                elif i == self.m//2:
                    if j < self.m//2:
                        self.board[i][j].xAxis = -1 * colValue
                        self.board[i][j].yAxis = 0
                    if j > self.m//2:
                        self.board[i][j].xAxis = colValue
                        self.board[i][j].yAxis = 0
                    if j == self.m//2:
                        self.board[i][j].xAxis = 0
                        self.board[i][j].yAxis = 0
                        self.board[i][j].id = -1

                    if j == 0:
                        # closure neighbour
                        self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                        self.board[i][j].closureNeighbour.append(self.board[i][j+1])
                        self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                        # equal neighbour
                        self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                        self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                    elif j == self.m-1:
                        # equal neighbour
                        self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                        self.board[i][j].equalNeighbour.append(self.board[i+1][j])
                        # closure neighbour
                        self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                        self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                        self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                    elif j == self.m//2:
                        # exact origin point
                        # for base station all the neighbours are it's closure neighbour.... there will be 8 total neighbours
                        # closure neighbour
                        self.board[i][j].closureNeighbour.append(self.board[i][j+1])
                        self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                        self.board[i][j].closureNeighbour.append(self.board[i+1][j])
                        self.board[i][j].closureNeighbour.append(self.board[i-1][j])
                        self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                        self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])
                        self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                        self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                    else:
                        # each node that doesn't lie on the edges and origin will have 8 neighbours
                        # equal neighbour
                        self.board[i][j].equalNeighbour.append(self.board[i-1][j])
                        self.board[i][j].equalNeighbour.append(self.board[i+1][j])

                        if j < self.m//2:
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j+1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j+1])
                            # further neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i][j-1])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j-1])
                        else:
                            # closure neighbour
                            self.board[i][j].closureNeighbour.append(self.board[i][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i-1][j-1])
                            self.board[i][j].closureNeighbour.append(self.board[i+1][j-1])

                            # further neighbour
                            self.board[i][j].furtherNeighbour.append(self.board[i][j+1])
                            self.board[i][j].furtherNeighbour.append(self.board[i+1][j+1])
                            self.board[i][j].furtherNeighbour.append(self.board[i-1][j+1])
                if j < self.boardSize//2:
                    colValue -= self.offSet
                if j >= self.boardSize//2:
                    colValue += self.offSet

            if i < self.boardSize//2:
                rowValue -= self.offSet
            if i >= self.boardSize//2:
                rowValue += self.offSet
            colValue = self.maxValue

    def printBoard(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                print(f"({self.board[i][j].xAxis},{self.board[i][j].yAxis})",end="")
            print()

    def printBoardById(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                print(self.board[i][j].id,end="\t")
            print()

    def printAllThreeNeighboursDetail(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                print(f"id : {self.board[i][j].id} , co-ordinate: ({self.board[i][j].xAxis},{self.board[i][j].yAxis})")
                print("Closure Neighbours :",[x.id for x in self.board[i][j].closureNeighbour])
                print("Equal Neighbours :",[x.id for x in self.board[i][j].equalNeighbour])
                print("Further Neighbours :",[x.id for x in self.board[i][j].furtherNeighbour])
                print("-"*300)
                print("-"*300)

    def printAllPowersDetail(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                print(self.board[i][j].power,end=" ")
            print()

        print([f'{val.id}:({val.xAxis},{val.yAxis}) ' for key,val in self.nodeById.items()])
        print([val.id for key,val in self.nodeById.items()])


    def setPacket(self,node):
        currentNode = node
        currentNode.p = packet("PEACE")




    def shiftPacket(self,fromNode,toNode):
        print("fromNode's packet",fromNode.p, "and id is {}".format(fromNode.id))
        print("toNode's packet",toNode.p, " and id is {}".format(toNode.id))

        toNode.p = fromNode.p
        fromNode.p = None
        self.sourceNode = toNode



    def SourceAccess(self,id):

        currentNode = None
        try:
            currentNode = self.nodeById[id]
            self.sourceNode=currentNode
            self.setPacket(currentNode)
        except:
            print("The id is invalid")
            print(currentNode)
            newID = int(input("Enter new ID (0->exit):"))
            if newID == 0:
                exit()
            else:
                self.SourceAccess(newID)

    def initializeCompromisedNode(self):
        for _ in range(1):
            while True:
                compromisedNodeId = random.choice(list(self.nodeById.keys()))
                if compromisedNodeId in self.compromisedNodes:
                    continue
                else:
                    self.nodeById[compromisedNodeId].isCompromisedNode = True
                    self.compromisedNodes.append(compromisedNodeId)
                    break
        print("Compromised Node:",self.compromisedNodes)
    def powerReduction(self,currentNode):
        if currentNode is not None:
            self.sourceNode = currentNode
            if currentNode.isCompromisedNode or currentNode.id == -1:
                return True
            consumption = (self.packet.eEelc * self.packet.k) + (self.packet.eAmp * (self.packet.k * 50))
            currentNode.power -= consumption
            return False
        return False
    def transferPowerReduction(self,fromNode,toNode):
        if fromNode is not None and toNode is not None:
            self.powerReduction(fromNode)
            self.powerReduction(toNode)

    def getPhantomSquare(self,currentNode,Square1):
        self.SourceAccess(currentNode)
        currentNode = self.nodeById[currentNode]
        self.setPacket((currentNode))
        if currentNode.isAttacker:
            self.failurePacketsCount += 1
            self.moveAttacker(self.attackerNode,currentNode)
            return currentNode,self.nodeById,False,True

        hMax = m.ceil((self.boardSize//2)//4)
        hMax += 2
        print("HMax:",hMax)
        A = None
        B = None
        C = None
        D = None

        if currentNode.i - hMax >= 0 and currentNode.j - hMax >= 0:
            print("YES A")
            A = self.board[currentNode.i - hMax][currentNode.j - hMax]
        if currentNode.i - hMax >= 0 and currentNode.j + hMax < self.boardSize:
            print("YES B")
            B = self.board[currentNode.i - hMax][currentNode.j + hMax]
        if currentNode.i + hMax < self.boardSize and currentNode.j - hMax >= 0:
            print("YES C")
            C = self.board[currentNode.i + hMax][currentNode.j - hMax]
        if currentNode.i + hMax < self.boardSize and currentNode.j + hMax < self.boardSize:
            print("YES D")
            D = self.board[currentNode.i + hMax][currentNode.j + hMax]

        print("4 edges are ...")
        print("Source S:({},{})".format(currentNode.i,currentNode.j))
        if A:
            if not B:
                B = self.board[A.i][self.boardSize-1]
                if D:
                    B = self.board[A.i][D.j]
            if C and not D:
                D = self.board[C.i][self.boardSize - 1]
                if B:
                    D = self.board[C.i][B.j]
            if not C:
                C = self.board[self.boardSize-1][A.j]
                if D:
                    C = self.board[D.i][A.j]

        if B:
            if not A:
                A = self.board[B.i][0]
            if not C:
                if D:
                    C = self.board[D.i][0]
                else:
                    if not C:
                        D = self.board[self.boardSize-1][B.j]
                    else:
                        D = self.board[C.i][B.j]

        if C:
            if not A:
                A = self.board[0][C.j]
            if not D:
                D = self.board[C.i][self.boardSize-1]
                if B:
                    D = self.board[C.i][B.j]
            if not B:
                if A:
                    B = self.board[A.i][self.boardSize-1]
                    if D:
                        B = self.board[A.i][D.j]

        if D:
            if not C:
                C = self.board[D.i][0]
            if not B:
                B = self.board[0][D.j]
            if not A:
                if B:
                    A = self.board[B.i][0]
        # printing 4 sides of phantomSquare
        print("A:({},{})".format(A.i,A.j))
        print("B:({},{})".format(B.i,B.j))
        print("C:({},{})".format(C.i,C.j))
        print("D:({},{})".format(D.i,D.j))

        for i in range(A.i,D.i+1):
            for j in range(A.j,D.j+1):
                if self.board[i][j].id == -1:
                    self.file.write("While traversing the base station has been deted!");
                if self.board[i][j].isAttacker:
                    self.file.write(f"Attacker has been detected while spreading {self.board[i][j].id} {self.board[i][j].isAttacker}\n")
                    return self.board[i][j],self.nodeById,False,True


                if i <= self.boardSize-1 and j <= self.boardSize -1:
                    try:
                        if self.board[i][j+1].isAttacker:
                            self.file.write(f"Attacker has been detected while spreading {self.board[i][j+1].id} {self.board[i][j+1].isAttacker}\n")
                            self.moveAttacker(self.attackerNode,self.board[i][j])
                            self.attackerNode = self.board[i][j]
                            self.failurePacketsCount += 1
                            return self.board[i][j],self.nodeById,False,True
                    except:
                        pass
                    if self.powerReduction(self.board[i][j]):
                        print(self.phantomSquare1)
                        print(self.board[i][j].id, "Sending through FRW")
                        # send to base station through forward random walk
                        # self.forwardRandomWalk(self.board[i][j]) # send through main file
                        return self.board[i][j],self.nodeById,True,False


                    self.powerReduction(self.board[i][j])
                    if Square1:
                        self.phantomSquare1.append(self.board[i][j])
                    else:
                        self.phantomSquare2.append(self.board[i][j])
                    # self.phantomSquare1.append(self.board[i][j])
                else:
                    break


        # select random phantom element from phantomSquare...
        if Square1:
            print(self.phantomSquare1)
            phantomElement1 = random.choice(list(self.phantomSquare1))
        else:
            print(self.phantomSquare2)
            phantomElement1 = random.choice(list(self.phantomSquare2))
        # phantomElement1 = list(self.phantomSquare1)[-1]
        return phantomElement1,self.nodeById,False,False

    def visualizeCoordinate(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                print("({},{})".format(i,j),end=" ")
            print()

    def checkAttacker(self,currentNode):
        if currentNode.isAttacker:
            return currentNode.i,currentNode.j,True
        try:
            if self.board[currentNode.i+1][currentNode.j]:
                if self.board[currentNode.i+1][currentNode.j].isAttacker:
                    return currentNode.i+1,currentNode.j,True
        except:
            pass
        try:
            if self.board[currentNode.i+1][currentNode.j+1]:
                if self.board[currentNode.i+1][currentNode.j+1].isAttacker:
                    return currentNode.i+1,currentNode.j+1,True
        except:
            pass
        try:
            if self.board[currentNode.i+1][currentNode.j-1]:
                if self.board[currentNode.i+1][currentNode.j-1].isAttacker:
                    return currentNode.i+1,currentNode.j-1,True
        except:
            pass
        try:
            if self.board[currentNode.i][currentNode.j+1]:
                if self.board[currentNode.i][currentNode.j+1].isAttacker:
                    return currentNode.i,currentNode.j+1,True
        except:
            pass
        try:
            if self.board[currentNode.i][currentNode.j-1]:
                if self.board[currentNode.i][currentNode.j-1].isAttacker:
                    return currentNode.i,currentNode.j-1,True
        except:
            pass
        try:
            if self.board[currentNode.i-1][currentNode.j]:
                if self.board[currentNode.i-1][currentNode.j].isAttacker:
                    return currentNode.i-1,currentNode.j,True
        except:
            pass
        try:
            if self.board[currentNode.i-1][currentNode.j+1]:
                if self.board[currentNode.i-1][currentNode.j+1].isAttacker:
                    return currentNode.i-1,currentNode.j+1,True
        except:
            pass
        try:
            if self.board[currentNode.i-1][currentNode.j-1]:
                if self.board[currentNode.i-1][currentNode.j-1].isAttacker:
                    return currentNode.i-1,currentNode.j-1,True
        except:
            pass
        return currentNode.i,currentNode.j,False
    def shortestPath(self,currentNode,destNode):
        print("CurrentNode:({},{})\nDestNode:({},{})".format(currentNode.i,currentNode.j,destNode.i,destNode.j))
        trackX,trackY = currentNode.i,currentNode.j
        if self.board[trackX][trackY].isAttacker and trackX != self.boardSize//2 and trackY != self.boardSize//2:
            self.failurePacketsCount += 1
            self.moveAttacker(self.attackerNode,self.board[trackX][trackY])
            return False,True,False
        # print(trackX,trackY)
        prevX,prevY = None,None
        if trackX == destNode.i and trackY == destNode.j:
            return False,False,False
        while trackX != destNode.i and trackY != destNode.j:
            #checking attacker
            isAttackerAtI, isAttackerAtJ, isAttacker = self.checkAttacker(self.board[trackX][trackY])
            trackPresentNode = self.board[trackX][trackY]
            if self.board[trackX][trackY] == currentNode:
                prevX = currentNode.i
                prevY = currentNode.j
            else:
                self.shiftPacket(self.board[prevX][prevY],self.board[trackX][trackY])
                prevX = trackX
                prevY = trackY
            if currentNode.id == -1:

                return True,False,False
            if self.board[trackX][trackY].isCompromisedNode:
                # directly move to base station
                # self.forwardRandomWalk(self.board[trackX][trackY])
                self.sourceNode = self.board[trackX][trackY]
                return False,False,True
            else:
                if self.board[trackX][trackY] != currentNode:
                    if self.board[trackX][trackY].power != 0:

                        sendToBase = self.powerReduction(self.board[trackX][trackY])

                        if sendToBase:
                            # direct to base station through forward random walk.
                            # self.forwardRandomWalk(self.board[trackX][trackY])
                            self.sourceNode = self.board[trackX][trackY]
                            return False,False,True
                    else:
                        # the node has no power to transfer the packet, hence the packet is died/stuck in-between.
                        self.failurePacketsCount += 1
                        return False, True, False

            if trackX > destNode.i:
                trackX -= 1
            elif trackX == destNode.i:
                break
            else:
                trackX += 1
            if trackY > destNode.j:
                trackY -= 1
            elif trackY == destNode.j:
                break
            else:
                trackY += 1
            # if attacker , then packet sending failed
            if trackX == isAttackerAtI and trackY == isAttackerAtJ and isAttacker:
                self.attackerNode = trackPresentNode
                self.moveAttacker(self.attackerNode,trackPresentNode)
                self.failurePacketsCount += 1
                return False,True,False
        while trackX != destNode.i:
            isAttackerAtI, isAttackerAtJ, isAttacker = self.checkAttacker(self.board[trackX][trackY])
            trackPresentNode = self.board[trackX][trackY]
            if self.board[trackX][trackY] == currentNode:
                prevX = currentNode.i
                prevY = currentNode.j
            else:
                self.shiftPacket(self.board[prevX][prevY],self.board[trackX][trackY])
                prevX = trackX
                prevY = trackY
            if currentNode.id == -1:

                return True, False, False
            if self.board[trackX][trackY].isCompromisedNode:
                # directly move to base station
                # self.forwardRandomWalk((self.board[trackX][trackY]))
                self.sourceNode = self.board[trackX][trackY]
                return False, False, True
            else:
                if self.board[trackX][trackY] != currentNode:
                    if self.board[trackX][trackY].power != 0:
                        sendToBase = self.powerReduction(self.board[trackX][trackY])
                        if sendToBase:
                            # direct to base station through forward random walk.
                            # self.forwardRandomWalk(self.board[trackX][trackY])
                            self.sourceNode = self.board[trackX][trackY]
                            return False, False, True
                    else:
                        # the node has no power to transfer the packet, hence the packet is died/stuck in-between.
                        self.failurePacketsCount += 1
                        return False, True, False

            if trackX > destNode.i:
                trackX -= 1
            elif trackX == destNode.i:
                break
            else:
                trackX += 1
            # if attackernode is the next node to move, then the packet sending failes
            if trackX == isAttackerAtI and trackY == isAttackerAtJ and isAttacker:
                self.attackerNode = trackPresentNode
                self.moveAttacker(self.attackerNode,trackPresentNode)
                self.failurePacketsCount += 1
                return False,True,False

        while trackY != destNode.j:
            isAttackerAtI, isAttackerAtJ, isAttacker = self.checkAttacker(self.board[trackX][trackY])
            trackPresentNode = self.board[trackX][trackY]
            if self.board[trackX][trackY] == currentNode:
                prevX = currentNode.i
                prevY = currentNode.j
            else:
                self.shiftPacket(self.board[prevX][prevY],self.board[trackX][trackY])
                prevX = trackX
                prevY = trackY
            if currentNode.id == -1:
                return True, False, False

            if self.board[trackX][trackY].isCompromisedNode:
                # directly move to base station
                # self.forwardRandomWalk(self.board[trackX][trackY])
                self.sourceNode = self.board[trackX][trackY]
                return False, False, True
            else:
                if self.board[trackX][trackY] != currentNode:
                    if self.board[trackX][trackY].power != 0:
                        sendToBase = self.powerReduction(self.board[trackX][trackY])
                        if sendToBase:
                            # send to base station directly through FRW
                            # self.forwardRandomWalk(self.board[trackX][trackY])
                            self.sourceNode = self.board[trackX][trackY]
                            return False, False, True
                    else:
                        # the node has no power to transfer the packet, hence the packet is died/stuck in-between.
                        print("No power in node")
                        self.failurePacketsCount += 1
                        return False, True, False


            if trackY > destNode.j:
                trackY -= 1
            elif trackY == destNode.j:
                break
            else:
                trackY += 1
            # if attacker node is the next to move, then the packet sending fails
            if trackX == isAttackerAtI and trackY == isAttackerAtJ and isAttacker:
                self.attackerNode = trackPresentNode
                self.moveAttacker(self.attackerNode,trackPresentNode)
                self.failurePacketsCount += 1
                return False,True,False
        if trackX != destNode.i and trackY != destNode.j:
            print("YES")
        else:
            self.shiftPacket(self.board[prevX][prevY],self.board[trackX][trackY])
            print(trackX,trackY)
            self.sourceNode = self.board[trackX][trackY]

        return False,False,False


    def packetSplittingFourPieces(self,currentNode):
        hMax = m.ceil((self.boardSize // 2) // 4)
        hMax += 2
        # splitting packet into 4 pices for sure!.
        A = None
        B = None
        C = None
        D = None

        if currentNode.i - hMax >= 0 and currentNode.j - hMax >= 0:
            print("YES A")
            A = self.board[currentNode.i - hMax][currentNode.j - hMax]
        if currentNode.i - hMax >= 0 and currentNode.j + hMax < self.boardSize:
            print("YES B")
            B = self.board[currentNode.i - hMax][currentNode.j + hMax]
        if currentNode.i + hMax < self.boardSize and currentNode.j - hMax >= 0:
            print("YES C")
            C = self.board[currentNode.i + hMax][currentNode.j - hMax]
        if currentNode.i + hMax < self.boardSize and currentNode.j + hMax < self.boardSize:
            print("YES D")
            D = self.board[currentNode.i + hMax][currentNode.j + hMax]

        if A:
            if not B:
                B = self.board[A.i][self.boardSize-1]
                if D:
                    B = self.board[A.i][D.j]
            if C and not D:
                D = self.board[C.i][self.boardSize - 1]
                if B:
                    D = self.board[C.i][B.j]
            if not C:
                C = self.board[self.boardSize-1][A.j]
                if D:
                    C = self.board[D.i][A.j]

        if B:
            if not A:
                A = self.board[B.i][0]
            if not C:
                if D:
                    C = self.board[D.i][0]
                else:
                    if not C:
                        D = self.board[self.boardSize-1][B.j]
                    else:
                        D = self.board[C.i][B.j]

        if C:
            if not A:
                A = self.board[0][C.j]
            if not D:
                D = self.board[C.i][self.boardSize-1]
                if B:
                    D = self.board[C.i][B.j]
            if not B:
                if A:
                    B = self.board[A.i][self.boardSize-1]
                    if D:
                        B = self.board[A.i][D.j]

        if D:
            if not C:
                C = self.board[D.i][0]
            if not B:
                B = self.board[0][D.j]
            if not A:
                if B:
                    A = self.board[B.i][0]
        return [A,B,C,D]
    def packetSplittingNPieces(self):
        pass



    def forwardRandomWalk(self,fromNode):
        currentNode = fromNode
        if currentNode.isAttacker:
            self.failurePacketsCount += 1
            return
        while currentNode.id != -1:
            self.sourceNode = currentNode
            nextNode = random.choice(list(currentNode.closureNeighbour))
            self.shiftPacket(currentNode,nextNode)
            currentNode = nextNode
        if currentNode.id == -1:
            self.successfulPacketsCount += 1
            print("Packet reached to BaseStation")
            print(currentNode.id)



    '''
    TO-DO
    1 . configure Shortest Path Algorithm
    2 . configure forward Random Walk Algorithm
    3 . put compromised node(upto 10/20 - each quandrant should have!), once the packet reach compromised node, directly it goes to base station by Shortest Path Algorithm, It won't continue the process.
    4 . configure Power reduction Algorithm
    '''

