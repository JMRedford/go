class Game:
  def __init__(self, size):
    self.size = size
    self.whiteCaptures = 0
    self.blackCaptures = 0
    self.moveList = []
    self.board = []
    self.ko = [-1,-1] # row, column of illegal move via ko
    for i in range(size):
      self.board.append([])
      for j in range(size):
        self.board[i].append(0)
  
  def groupAt(self, row, col):
    # returns list representing group currently on board at location [row][col]
    if self.board[row][col] == 0:
      raise KeyError('groupAt called with empty space')
      return []
    else:
      player = self.board[row][col]
      group = []
      toCheckForNeighbors = [[row,col]]
      
      while len(toCheckForNeighbors) > 0:
        group.append(toCheckForNeighbors[0])
        toCheckRow = toCheckForNeighbors[0][0]
        toCheckCol = toCheckForNeighbors[0][1]
        toCheckForNeighbors.pop(0)
        if (toCheckRow > 0 and self.board[toCheckRow-1][toCheckCol] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow-1 and location[1] == toCheckCol:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow-1,toCheckCol])
        if (toCheckRow < self.size - 1 and self.board[toCheckRow+1][toCheckCol] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow+1 and location[1] == toCheckCol:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow+1,toCheckCol])
        if (toCheckCol > 0 and self.board[toCheckRow][toCheckCol-1] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow and location[1] == toCheckCol-1:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow,toCheckCol-1])   
        if (toCheckCol < self.size - 1 and self.board[toCheckRow][toCheckCol+1] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow and location[1] == toCheckCol+1:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow,toCheckCol+1])
      return group
  
  def groupWith(self, player, row, col):
    # returns list representing group which would result if player plays on [row][col]
    if self.board[row][col] != 0:
      raise KeyError('groupWith called with non-empty space')
      return []
    else:  
      group = []
      toCheckForNeighbors = [[row,col]]
      checkedForNeighbors = []
      while len(toCheckForNeighbors) > 0:
        group.append(toCheckForNeighbors[0])
        toCheckRow = toCheckForNeighbors[0][0]
        toCheckCol = toCheckForNeighbors[0][1]
        toCheckForNeighbors.pop(0)
        if (toCheckRow > 0 and self.board[toCheckRow-1][toCheckCol] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow-1 and location[1] == toCheckCol:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow-1,toCheckCol])
        if (toCheckRow < self.size - 1 and self.board[toCheckRow+1][toCheckCol] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow+1 and location[1] == toCheckCol:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow+1,toCheckCol])
        if (toCheckCol > 0 and self.board[toCheckRow][toCheckCol-1] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow and location[1] == toCheckCol-1:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow,toCheckCol-1])   
        if (toCheckCol < self.size - 1 and self.board[toCheckRow][toCheckCol+1] == player):
          inList = False
          for location in group:
            if location[0] == toCheckRow and location[1] == toCheckCol+1:
              inList = True
          if not inList:
            toCheckForNeighbors.append([toCheckRow,toCheckCol+1])
      return group

  def isCaptured(self, groupList):
    # if there is any empty space around the members of the group, return false
    for location in groupList:
      if (location[0] > 0 and self.board[location[0]-1][location[1]] == 0):
        if not [location[0]-1,location[1]] in groupList:
          return False
      if (location[0] < self.size - 1 and self.board[location[0]+1][location[1]] == 0):
        if not [location[0]+1,location[1]] in groupList:
          return False
      if (location[1] > 0 and self.board[location[0]][location[1]-1] == 0):
        if not [location[0],location[1]-1] in groupList:
          return False
      if (location[1] < self.size - 1 and self.board[location[0]][location[1]+1] == 0):
        if not [location[0],location[1]+1] in groupList:
          return False
    return True

  def captureGroup(self, groupList):
    player = self.board[groupList[0][0]][groupList[0][1]]
    for location in groupList:
      self.board[location[0]][location[1]] = 0
      if player == 1:
        self.whiteCaptures = self.whiteCaptures + 1
      else:
        self.blackCaptures = self.blackCaptures + 1

  def place(self, player, row, col): # player = 1 for white, -1 for black
    if (self.board[row][col] != 0):
      # move illegal via space already filled
      return False
    elif (row == self.ko[0] and col == self.ko[1]):
      # move illegal via ko
      return False
    else:
      #check for move illegal via self-capture
      if self.isCaptured(self.groupWith(player,row,col)):
        return False
      else:
        self.board[row][col] = player
        self.moveList.append([player,row,col])
        try:
          if row > 0 and self.board[row-1][col] != player and self.isCaptured(self.groupAt(row-1,col)):
            self.captureGroup(self.groupAt(row-1,col))
        except KeyError:
          pass
        try:
          if row < self.size - 1 and self.board[row+1][col] != player and self.isCaptured(self.groupAt(row+1,col)):
            self.captureGroup(self.groupAt(row+1,col))
        except KeyError:
          pass
        try:
          if col > 0 and self.board[row][col-1] != player and self.isCaptured(row,col-1):
            self.captureGroup(self.groupAt(row,col-1))
        except:
          pass
        try:  
          if col < self.size - 1 and self.board[row][col+1] != player and self.isCaptured(self.groupAt(row,col+1)):
            self.captureGroup(self.groupAt(row,col+1))
        except KeyError:
          pass
        return True
