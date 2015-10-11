import math
import random

class Node:
  def __init__(self):
    self.input = 0
    self.forward = [] # [[node,weightPos,weightNeg],[node,weightPos,weightNeg],...]
    self.threshold = 0.5
    self.output = 0

  def increaseInput(self,ammount):
    self.input = self.input + ammount
    if (self.input > self.threshold or self.input < -1*self.threshold):
      self.output = self.input/math.pow(math.pow(self.input,2),0.5)
    else:
      self.output = 0

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
          node.forward.append([self.firstLayer[i],(random.random()-0.5)*4,(random.random()-0.5)*4])

    self.secondLayer = []
    for i in range(500):
      self.secondLayer.append(Node())
      for node in self.firstLayer:
        node.forward.append([self.secondLayer[i],(random.random()-0.5),(random.random()-0.5)])

    self.outputLayer = []
    for i in range(self.size):
      self.outputLayer.append([])
      for j in range(self.size):
        self.outputLayer[i].append(Node())
        for node in self.secondLayer:
          node.forward.append([self.outputLayer[i][j],(random.random()-0.5)/100,(random.random()-0.5)/100])

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
          for fore in self.inputLayer[i][j].forward:
              fore[0].increaseInput(fore[1])
        elif board[i][j] == -1:
          for fore in self.inputLayer[i][j].forward:
              fore[0].increaseInput(fore[2])

    for node in self.firstLayer:
      for fore in node.forward:
        if node.output > 0:
          fore[0].increaseInput(fore[1])
        elif node.output < 0:
          fore[0].increaseInput(fore[2])

    for node in self.secondLayer:
      for fore in node.forward:
        if node.output > 0:
          fore[0].increaseInput(fore[1])
        elif node.output < 0:
          fore[0].increaseInput(fore[2])

    largest = [0,0]
    for i in range(len(self.outputLayer)):
      for j in range(len(self.outputLayer[i])):
        if self.outputLayer[i][j].input > self.outputLayer[largest[0]][largest[1]].input:
          largest = [i,j]

    return largest

  def train(self,direction):
    # TODO: write this ;)
    pass
    # find paths of activated nodes that increase the value of the move 
      # adjust weight of the paths in the direction
    # find paths of activated nodes that decrease the value of the move 
      # adjust weight of the paths opposite the direction