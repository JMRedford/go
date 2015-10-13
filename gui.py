from Tkinter import *
import gameClass
import Net
import cPickle as pickle

theGame = gameClass.Game(19)
try:
  theNet = pickle.load(open('netFile.dat','r'))
except IOError:
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
saveImage = PhotoImage(file = './SaveIcon.gif')
canvas.create_image(320,320, image=boardImage)
canvas.create_image(160,670, image=checkImage)
canvas.create_image(320,670, image=xImage)
canvas.create_image(480,670, image=saveImage)
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
      while not theGame.place(player,move[0],move[1]):
        print 'the net chose an illegal move, training'
        theNet.train(-1)
        move = theNet.getMove(theGame.board)
      player = -1*player

    pieces = []
    for i in range(len(theGame.board)):
      for j in range(len(theGame.board[i])):
        if theGame.board[i][j] == 1:
          pieces.append([PhotoImage(file = './WhiteStone.gif'),i,j])
        if theGame.board[i][j] == -1:
          pieces.append([PhotoImage(file = './BlackStone.gif'),i,j])
    canvas.delete(ALL)
    canvas.create_image(320,320, image=boardImage)
    canvas.create_image(160,670, image=checkImage)
    canvas.create_image(320,670, image=xImage)
    canvas.create_image(480,670, image=saveImage)
    for piece in pieces:
      canvas.create_image(piece[1]*32+32,piece[2]*32+32,image=piece[0])
    canvas.pack()
  else:
    if event.x < 213:
      theNet.train(1)
    elif event.x < 426:
      theNet.train(-1)
    else:
      # save net
      print 'saving net'
      pickle.dump(theNet,open("netFile.dat","w+"),-1)
      print 'finished saving net'
      

canvas.bind("<Button-1>", callback)

root.mainloop()
