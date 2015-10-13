import math
import random

class Tree:
  def __init__(self,value,parent=None):
    self.parent = parent
    self.value = value
    self.children = []

  def addChild(self,value):
    self.children.append(Tree(value,self))

class Node:
  def __init__(self):
    self.input = 0
    self.forward = [] # [[node,weightPos,weightNeg],[node,weightPos,weightNeg],...]
    self.threshold = 0.5

  def increaseInput(self,ammount):
    self.input = self.input + ammount

class Net:
  def __init__(self):
    self.size = 19
    self.inputLayer = []
    for i in range(self.size):
      self.inputLayer.append([])
      for j in range(self.size):
        self.inputLayer[i].append(Node())

    self.firstLayer = []
    for i in range(500):
      self.firstLayer.append(Node())
      for row in self.inputLayer:
        for node in row:
          node.forward.append([self.firstLayer[i],(random.random()-0.5)*2,(random.random()-0.5)*2])

    self.secondLayer = []
    for i in range(500):
      self.secondLayer.append(Node())
      for node in self.firstLayer:
        node.forward.append([self.secondLayer[i],(random.random()-0.5)/29,(random.random()-0.5)/29])
        # 29 is a magic number chosen so that approximately half of all nodes in second layer are active

    self.outputLayer = []
    for i in range(self.size):
      self.outputLayer.append([])
      for j in range(self.size):
        self.outputLayer[i].append(Node())
        for node in self.secondLayer:
          node.forward.append([self.outputLayer[i][j],random.random()-0.5,random.random()-0.5])

  def getMove(self,board):
    for row in self.inputLayer:
      for node in row:
        node.input = 0
    for node in self.firstLayer:
      node.input = 0
    for node in self.secondLayer:
      node.input = 0
    for row in self.outputLayer:
      for node in row:
        node.input = 0

    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == 1:
          self.inputLayer[i][j].input = 1
          for fore in self.inputLayer[i][j].forward:
              fore[0].increaseInput(fore[1])
        elif board[i][j] == -1:
          self.inputLayer[i][j].input = -1
          for fore in self.inputLayer[i][j].forward:
              fore[0].increaseInput(fore[2])

    for node in self.firstLayer:
      for fore in node.forward:
        if node.input > node.threshold:
          fore[0].increaseInput(fore[1])
        elif node.input < -1*node.threshold:
          fore[0].increaseInput(fore[2])

    for node in self.secondLayer:
      for fore in node.forward:
        if node.input > node.threshold:
          fore[0].increaseInput(fore[1])
        elif node.input < -1*node.threshold:
          fore[0].increaseInput(fore[2])

    largest = [0,0]
    for i in range(len(self.outputLayer)):
      for j in range(len(self.outputLayer[i])):
        if self.outputLayer[i][j].input > self.outputLayer[largest[0]][largest[1]].input:
          largest = [i,j]

    return largest

  def train(self,direction):
    largest = [0,0]
    for i in range(len(self.outputLayer)):
      for j in range(len(self.outputLayer[i])):
        if self.outputLayer[i][j].input > self.outputLayer[largest[0]][largest[1]].input:
          largest = [i,j]

    trainingTree = Tree(self.outputLayer[largest[0]][largest[1]])

    print 'training second layer nodes'

    for secondLayerNode in self.secondLayer:
      for fore in secondLayerNode.forward:
        if fore[0] == trainingTree.value:
          if secondLayerNode.input > 0.5:
            if fore[1] > 0:
              trainingTree.addChild([secondLayerNode,1])
              fore[1] = fore[1] + fore[1]*0.1*direction
            else:
              trainingTree.addChild([secondLayerNode,-1])
              fore[1] = fore[1] + fore[1]*0.1*direction
          elif secondLayerNode.input < -0.5:
            if fore[2] > 0:
              trainingTree.addChild([secondLayerNode,1])
              fore[2] = fore[2] + fore[2]*0.1*direction
            else:
              trainingTree.addChild([secondLayerNode,-1])
              fore[2] = fore[2] + fore[2]*0.1*direction

    print 'training first layer nodes'

    for secondLayerTree in trainingTree.children:
      for firstLayerNode in self.firstLayer:
        for fore in firstLayerNode.forward:
          if fore[0] == secondLayerTree.value[0]:
            if firstLayerNode.input > 0.5:
              if fore[1]*secondLayerTree.value[1] > 0:
                secondLayerTree.addChild([firstLayerNode,secondLayerTree.value[1]])
                fore[1] = fore[1] + fore[1]*0.01*direction
              else:
                secondLayerTree.addChild([firstLayerNode,-1*secondLayerTree.value[1]])
                fore[1] = fore[1] + fore[1]*0.01*direction
            elif firstLayerNode.input < -0.5:
              if fore[2]*secondLayerTree.value[1] > 0:
                secondLayerTree.addChild([firstLayerNode,secondLayerTree.value[1]])
                fore[2] = fore[2] + fore[2]*0.01*direction
              else:
                secondLayerTree.addChild([firstLayerNode,-1*secondLayerTree.value[1]])
                fore[2] = fore[2] + fore[2]*0.01*direction

    print 'training input layer nodes'

    for secondLayerTree in trainingTree.children:
      for firstLayerTree in secondLayerTree.children:
        for i in range(len(self.outputLayer)):
          for j in range(len(self.outputLayer[i])):
            for fore in self.outputLayer[i][j].forward:
              if fore[0] == firstLayerTree.value[0]:
                if self.inputLayer[i][j].input > 0.5:
                  if fore[1]*firstLayerTree.value[1] > 0:
                    fore[1] = fore[1] + fore[1]*0.001*direction
                  else:
                    fore[1] = fore[1] + fore[1]*0.001*direction
                elif self.inputLayer[i][j].input < -0.5:
                  if fore[2]*firstLayerTree.value[1] > 0:
                    fore[2] = fore[2] + fore[2]*0.001*direction
                  else:
                    fore[2] = fore[2] + fore[2]*0.001*direction

    print 'finished training'
