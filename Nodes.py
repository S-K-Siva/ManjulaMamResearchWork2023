from packet import packet
class Node:
    def __init__(self):
        self.xAxis = 0
        self.yAxis = 0
        self.i = 0
        self.j = 0
        self.id = 0
        self.power = 0.5
        self.closureNeighbour,self.equalNeighbour,self.furtherNeighbour = [],[],[]
        self.neighbours = []
        self.p = None
        self.isCompromisedNode = False
        self.isAttacker = False
