from Tkinter import *
import gameClass
import Net

theGame = gameClass.Game(19)
theNet = Net.Net()

root = Tk()
wid = 640
hei = 700

player = -1
pieces = []

canvas = Canvas(root,width=wid,height=hei)

boardImage = PhotoImage(file = './GoBoard.gif')
checkImage = PhotoImage(file = './check.gif')
xImage = PhotoImage(file = './x.gif')
canvas.create_image(320,320, image=boardImage)
canvas.create_image(213,670, image=checkImage)
canvas.create_image(426,670, image=xImage)
canvas.pack()

def callback(event):
  global player
  global pieces
  global theGame
  print "clicked at", event.x, event.y
  if event.y < 640:
    col = (event.y+16)/32-1
    row = (event.x+16)/32-1
    if theGame.place(player,row,col):
      player = -1*player

    if player == 1:
      move = theNet.getMove(theGame.board)
      if theGame.place(player,move[0],move[1]):
        player = -1*player
      else:
        print "computer picked an illegal move, please move for the computer"

    pieces = []
    for i in range(len(theGame.board)):
      for j in range(len(theGame.board[i])):
        if theGame.board[i][j] == 1:
          pieces.append([PhotoImage(file = './WhiteStone.gif'),i,j])
        if theGame.board[i][j] == -1:
          pieces.append([PhotoImage(file = './BlackStone.gif'),i,j])
    canvas.delete(ALL)
    canvas.create_image(320,320, image=boardImage)
    for piece in pieces:
      canvas.create_image(piece[1]*32+32,piece[2]*32+32,image=piece[0])
    canvas.pack()
  else:
    if event.x < 320:
      theNet.train(1)
    else:
      theNet.train(-1)

canvas.bind("<Button-1>", callback)

root.mainloop()
