# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 20:44:37 2016

@author: Rutger
"""

from Tkinter import *
from numpy import *
from copy import deepcopy

###############################################################################
class Chess(object):
    #--------------------------------------------------------------------------
    def __init__(self):
        self.conf = array([['RB','HB','BB','QB','KB','BB','HB','RB'], \
                           ['PB','PB','PB','PB','PB','PB','PB','PB'], \
                           ['','','','','','','',''], \
                           ['','','','','','','',''], \
                           ['','','','','','','',''], \
                           ['','','','','','','',''], \
                           ['PW','PW','PW','PW','PW','PW','PW','PW'], \
                           ['RW','HW','BW','QW','KW','BW','HW','RW']])
                           
    #--------------------------------------------------------------------------
    def Move(self, start, end):
        self.conf[end] = self.conf[start]
        self.conf[start] = ''
        
        
###############################################################################
class Board(Frame):
    #--------------------------------------------------------------------------
    def __init__(self, master = None):
        Frame.__init__(self, master)
        w,h = self.master.winfo_screenwidth(),self.master.winfo_screenheight()
        self.master.overrideredirect(1)
        self.master.geometry("%dx%d+0+0" % (w, h)) 
#        self.master.grab_set()
#        self.master.focus_set()
        
        self.size = 8
        self.border_width = 20
        self.c_width = 75
        self.B_width = self.size * self.c_width + 3 * self.border_width/1.645
        
        self.fs = 8
        self.Piece_dic = {}
        
        self.Image_dic = {}
        
        self.lb_height = 33    
        
        self.Load_Images()
        self.Create_Board()
        self.Create_Others()
        
    #--------------------------------------------------------------------------    
    def Load_Images(self):
        self.Image_dic['PW'] = PhotoImage(file ='ChessPieces/Pawn_White.gif')
        self.Image_dic['QW'] = PhotoImage(file ='ChessPieces/Queen_White.gif')
        self.Image_dic['KW'] = PhotoImage(file ='ChessPieces/King_White.gif')
        self.Image_dic['RW'] = PhotoImage(file ='ChessPieces/Rook_White.gif')
        self.Image_dic['BW'] = PhotoImage(file ='ChessPieces/Bishop_White.gif')
        self.Image_dic['HW'] = PhotoImage(file ='ChessPieces/Horse_White.gif')
        self.Image_dic['PB'] = PhotoImage(file ='ChessPieces/Pawn_Black.gif')
        self.Image_dic['QB'] = PhotoImage(file ='ChessPieces/Queen_Black.gif')
        self.Image_dic['KB'] = PhotoImage(file ='ChessPieces/King_Black.gif')
        self.Image_dic['RB'] = PhotoImage(file ='ChessPieces/Rook_Black.gif')
        self.Image_dic['BB'] = PhotoImage(file ='ChessPieces/Bishop_Black.gif')
        self.Image_dic['HB'] = PhotoImage(file ='ChessPieces/Horse_Black.gif')   
        self.Image_dic[''] = PhotoImage(file ='ChessPieces/Empty.gif')
        
    #--------------------------------------------------------------------------
    def Create_Board(self):
        self.board = Canvas(self.master, width = self.B_width, \
                            height = self.B_width, \
                            background = 'black')
        self.board.grid(row = 0, rowspan = 4, padx = (30,0), pady = 30)  
        
        self.Create_Cells()
        
    #--------------------------------------------------------------------------
    def Create_Cells(self):
        for i in range(self.size):
            x0 = self.border_width + i*self.c_width
            x1 = x0 + self.c_width
            for j in range(self.size):
                y0 = self.border_width + j*self.c_width
                y1 = y0 + self.c_width
                colour = 'brown'
                if not (i + j) % 2:
                    colour = 'white'
                Square = self.board.create_rectangle(x0,y0,x1,y1, \
                                                fill = colour, width = 0)
                self.board.tag_lower(Square)
                
                xc = (x0 + x1)/2
                yc = (y0 + y1)/2
                self.Piece_dic[j,i] = self.board.create_image(xc, yc, \
                                      tags = 'abcdefgh'[j]+'abcdefgh'[i])
                self.board.create_text(self.border_width/2, yc, \
                                       text = '87654321'[j], \
                                       font = ("Verdana",self.fs), \
                                       fill = 'white')
                
                
            self.board.create_text(xc, y1 + self.border_width/2, \
                                   text = 'abcdefgh'[i], \
                                   font = ("Verdana",self.fs), \
                                   fill = 'white')
                   
    #--------------------------------------------------------------------------                                          
    def Create_Others(self):
        self.Create_Entry1() 
        self.Create_Listboxes()
        #self.Create_Timers()
        self.Create_Menu()
        
    #--------------------------------------------------------------------------
    def Create_Entry1(self):
        self.EntryFrame = Frame(self.master)
        self.EntryFrame.grid(row = 0, column = 1, padx = 10, sticky = S)
        Label(self.EntryFrame, text = 'Enter move below:').pack()
        self.e1 = Entry(self.EntryFrame)
        self.e1.pack()
        
    #--------------------------------------------------------------------------
    def Create_Listboxes(self):
        self.frame = Frame(self.master, bd = 2, relief = SUNKEN)
        self.frame.grid(row = 1, column = 1, padx = 10, sticky = S)
        
        self.lb1 = Listbox(self.frame, height = self.lb_height, \
                           width = 3, bd = 0, state = DISABLED)        
        self.lb2 = Listbox(self.frame, height = self.lb_height, \
                           width = 10, bd = 0)
        self.lb3 = Listbox(self.frame, height = self.lb_height, \
                           width = 10, bd = 0)
                           
        self.lb1.pack(side = LEFT)
        self.lb2.pack(side = LEFT)
        self.lb3.pack(side = LEFT)
        
        self.scrollbar = Scrollbar(self.frame, command=self.lb1.yview, \
                                   orient=VERTICAL)
        self.scrollbar.pack(side = RIGHT, fill = Y)
        
        self.ListBoxScroll()
        self.ListBoxConfigurate()
        
    #--------------------------------------------------------------------------
    def ListBoxScroll(self):        
        def scr1(*args):
            self.scrollbar.set(args[0], args[1])
            self.lb2.yview_moveto(args[0])
            
        def scr2(*args):
            self.scrollbar.set(args[0], args[1])
            self.lb3.yview_moveto(args[0])
            
        def scr3(*args):
            self.scrollbar.set(args[0], args[1])
            self.lb1.yview_moveto(args[0])
            
        self.lb1.configure(yscrollcommand = scr1)
        self.lb2.configure(yscrollcommand = scr2)
        self.lb3.configure(yscrollcommand = scr3)
        
    #--------------------------------------------------------------------------
    def ListBoxConfigurate(self):
        def Right1(event):
            index = self.lb2.curselection()[0]
            self.lb3.selection_set(index)
            self.lb3.activate(index)
            self.lb3.focus_set()
            
        def Right2(event):
            index = self.lb3.curselection()[0]
            if not index + 1 == self.lb3.size():
                self.lb2.selection_set(index + 1)
                self.lb2.activate(index + 1)
                self.lb2.focus_set()
            
        def Left1(event):
            index = self.lb3.curselection()[0]
            self.lb2.selection_set(index)
            self.lb2.activate(index)
            self.lb2.focus_set()
            
        def Left2(event):
            index = self.lb2.curselection()[0]
            if index:
                self.lb3.selection_set(index - 1)
                self.lb3.activate(index - 1)
                self.lb3.focus_set()
            
        
        self.lb2.bind('<Right>', Right1)
        self.lb2.bind('<Left>', Left2)
        self.lb3.bind('<Right>', Right2)
        self.lb3.bind('<Left>', Left1)
        self.lb2.bind('<Tab>', lambda e: 'break')
        self.lb3.bind('<Tab>', lambda e: 'break')
        
    #--------------------------------------------------------------------------
    def ListBoxDown(self):
        self.lb1.yview_moveto(1)
        self.lb2.yview_moveto(1)
        self.lb3.yview_moveto(1) 
        
    #--------------------------------------------------------------------------    
    def Create_Timers(self):
        self.TimerB = Label(self.master, text = 'iets')
        self.TimerB.grid(column = 2, row = 0)
        self.TimerW = Label(self.master, text = 'iets anders')
        self.TimerW.grid(column = 2, row = 0)
        
    #--------------------------------------------------------------------------
    def Create_Menu(self):   
        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff = False)
        self.menubar.add_cascade(label = 'Game', menu = self.filemenu)
#        editmenu = Menu(self.menubar, tearoff=0)
#        editmenu.add_command(label="Undo", command=donothing)
#        
#        editmenu.add_separator()
#        
#        editmenu.add_command(label="Cut", command=donothing)
#        editmenu.add_command(label="Copy", command=donothing)
#        editmenu.add_command(label="Paste", command=donothing)
#        editmenu.add_command(label="Delete", command=donothing)
#        editmenu.add_command(label="Select All", command=donothing)
#        
#        self.menubar.add_cascade(label="Edit", menu=editmenu)
#        helpmenu = Menu(self.menubar, tearoff=0)
#        helpmenu.add_command(label="Help Index", command=donothing)
#        helpmenu.add_command(label="About...", command=donothing)
#        self.menubar.add_cascade(label="Help", menu=helpmenu)
        
        self.master.config(menu=self.menubar)
        
        
###############################################################################
class Popup(Toplevel):
    #--------------------------------------------------------------------------
    def __init__(self, parent, color, i, j):
        Toplevel.__init__(self, parent)
        self.transient(parent)
        self.parent = parent

        body = Frame(self)
        self.initial_focus = self.body(body, color, i, j)
        body.pack(padx=5, pady=5)

        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", lambda e: None)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+900,
                                  parent.winfo_rooty()+400))

        self.initial_focus.focus_set()
        self.wait_window(self)

    #--------------------------------------------------------------------------
    def body(self, master, color, i, j):
        self.color = color
        self.Load_Images()
        Label(master, text = 'Click a piece to promote the pawn to:').grid()
        colour = 'brown'
        if not (i + j) % 2:
            colour = 'white'
        frame = Frame(master)
        self.Queen = Button(frame, image = [self.QB, self.QW][self.color], \
                            background = colour, relief = RAISED, \
                            command = lambda: self.PieceClick('Q'))
        self.Queen.pack(side = LEFT)
        self.Rook = Button(frame, image = [self.RB, self.RW][self.color], \
                           background = colour, relief = RAISED, \
                           command = lambda: self.PieceClick('R'))
        self.Rook.pack(side = LEFT)
        self.Bishop = Button(frame, image = [self.BB, self.BW][self.color], \
                             background = colour, relief = RAISED, \
                             command = lambda: self.PieceClick('B'))
        self.Bishop.pack(side = LEFT)
        self.Horse = Button(frame, image = [self.HB, self.HW][self.color], \
                            background = colour, relief = RAISED, \
                            command = lambda: self.PieceClick('H'))
        self.Horse.pack(side = LEFT)
        frame.grid()
    
    #--------------------------------------------------------------------------    
    def Load_Images(self):
        self.QW = PhotoImage(file ='ChessPieces/Queen_White.gif')
        self.QB = PhotoImage(file ='ChessPieces/Queen_Black.gif')
        self.RW = PhotoImage(file ='ChessPieces/Rook_White.gif')
        self.RB = PhotoImage(file ='ChessPieces/Rook_Black.gif')
        self.BW = PhotoImage(file ='ChessPieces/Bishop_White.gif')
        self.BB = PhotoImage(file ='ChessPieces/Bishop_Black.gif')
        self.HW = PhotoImage(file ='ChessPieces/Horse_White.gif')
        self.HB = PhotoImage(file ='ChessPieces/Horse_Black.gif')

    #--------------------------------------------------------------------------
    def PieceClick(self, piece, event=None):
        self.withdraw()
        self.update_idletasks()
        self.pp = piece + ['B','W'][self.color]
        self.Exit()

    #--------------------------------------------------------------------------
    def Exit(self, event=None):
        self.parent.focus_set()
        self.destroy()
        
        
###############################################################################
class Game(Board, Chess):
    #--------------------------------------------------------------------------
    def __init__(self):
        self.cb = Board()
        self.ID = self.cb.Image_dic
        self.Start()
        self.Set_Menu()
        self.Bind_Keys()
        #self.BindListBoxes()
        
    #--------------------------------------------------------------------------
    def Start(self):
        for n in range(3):
            lb = [self.cb.lb1, self.cb.lb2, self.cb.lb3][n]
            lb.configure(state = 'normal')
            lb.delete(0, lb.size())
            if not n:
                lb.configure(state = 'disabled')
            
        self.turn = True
        self.turns = 0
        
        self.color = 1
        self.cg = Chess()
        self.full_game = [deepcopy(self.cg.conf)]
        
        self.DragAbility = True
        self.UpdateMoveAbility()
        self.drag = False
        self.x = 0
        self.y = 0
        self.item = None        
        
        self.Rokade = [[1, 1], [1, 1]]
        self.Eps = []
        
        self.Update()
        
    #--------------------------------------------------------------------------
    def Set_Menu(self):
        self.cb.filemenu.add_command(label = 'New Game', command = self.Start)
        self.cb.filemenu.add_separator()
        self.cb.filemenu.add_command(label = 'Quit Game', command = self.cb.master.destroy)
    
    #--------------------------------------------------------------------------
    def Update(self):
        for n in range(self.cb.size):
            for m in range(self.cb.size):
                self.cb.board.itemconfigure(self.cb.Piece_dic[n,m], \
                                            image = self.ID[self.cg.conf[n,m]])
      
    #--------------------------------------------------------------------------
    def Bind_Keys(self):   
        self.cb.e1.bind('<Return>', self.Input)
        for n in range(self.cb.size):
            for m in range(self.cb.size):
                self.cb.board.tag_bind('abcdefgh'[n]+'abcdefgh'[m], \
                                       '<ButtonPress-1>', \
                                       self.ButtonPress)
                self.cb.board.tag_bind('abcdefgh'[n]+'abcdefgh'[m], \
                                       '<ButtonRelease-1>', \
                                       self.ButtonRelease)
                self.cb.board.tag_bind('abcdefgh'[n]+'abcdefgh'[m], \
                                       '<B1-Motion>', \
                                       self.Motion)
    
    #--------------------------------------------------------------------------           
    def ButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        self.item = self.cb.board.find_closest(event.x, event.y)[0]
        if (self.cg.conf[self.cb.Piece_dic.keys()\
           [self.cb.Piece_dic.values().index(self.item)]]+'--')\
           [1] == self.Movable and self.DragAbility:
            self.cb.board.tag_raise(self.item)
            self.x = self.StartX = event.x
            self.y = self.StartY = event.y
            self.drag = True

    #--------------------------------------------------------------------------
    def ButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        if self.drag:
            self.x = 0
            self.y = 0
            self.EndX = event.x
            self.EndY = event.y
            self.drag = False
            
            self.MovePiece()
        
    #--------------------------------------------------------------------------
    def Motion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        if self.drag:
            delta_x = event.x - self.x
            delta_y = event.y - self.y
            # move the object the appropriate amount
            self.cb.board.move(self.item, delta_x, delta_y)
            # record the new position
            self.x = event.x
            self.y = event.y
    
    #-------------------------------------------------------------------------- 
    def MovePiece(self):
        delta_x = self.StartX - self.EndX
        delta_y = self.StartY - self.EndY
        self.cb.board.move(self.item, delta_x, delta_y)
        
        try:
            From = self.cb.board.find_overlapping(self.StartX, self.StartY, \
                                                  self.StartX, self.StartY)[1]
            To = self.cb.board.find_overlapping(self.EndX, self.EndY, \
                                                self.EndX, self.EndY)[1]
            Start = \
               self.cb.Piece_dic.keys()[self.cb.Piece_dic.values().index(From)]                                    
            End = \
               self.cb.Piece_dic.keys()[self.cb.Piece_dic.values().index(To)]
            if self.cg.conf[Start] and Start != End:
                if self.cg.conf[End]:
                    Type = '×'
                else:
                    Type = '-'
                self.input = 'abcdefgh'[Start[1]] + '87654321'[Start[0]] + \
                             Type + \
                             'abcdefgh'[End[1]] + '87654321'[End[0]]
                self.CodeProcess(self.input)
        except:
            pass
        self.Update()
        
    #--------------------------------------------------------------------------
    def DisableMove(self):
        self.DragAbility = False
        self.cb.e1.configure(state = 'disabled')

    #--------------------------------------------------------------------------        
    def EnableMove(self):
        self.DragAbility = True
        self.cb.e1.configure(state = 'normal')
        
    #--------------------------------------------------------------------------
    def UpdateMoveAbility(self):
        if self.color:
            self.Movable = 'W'
        else:
            self.Movable = 'B'
        
    #-------------------------------------------------------------------------- 
    def Input(self, event):
        self.input = self.cb.e1.get()
        if 'x' in self.input:
            self.input = self.input.replace('x','×')
        self.cb.e1.delete(0, END)
        self.CodeProcess(self.input)
        self.Update()
        
    #--------------------------------------------------------------------------   
    def CodeProcess(self, Input):
        self.code = Code(self.cb.master, Input, self.cg.conf, \
                         self.color, self.Rokade, self.Eps)
        if not self.code.error:
            if self.code.piece[0] == 'K' and sum(self.Rokade[self.color]):
                self.Rokade[self.color] = [0, 0]
            elif self.code.piece[0] == 'R' \
                 and sum(self.Rokade[self.color]) \
                 and (self.code.start[1] == 0 or self.code.start[1] == 7):
                self.Rokade[self.color][self.code.start[1]/7] = 0
            self.cg.Move(self.code.start, self.code.end)
            if self.code.RookAfterRokade:
                self.cg.Move(*self.code.RookAfterRokade)
            self.Update()
            if self.code.PawnPromotion():
                self.cg.conf[self.code.end] = self.code.pp 
                self.Update()
            self.Eps = self.code.EPsCreated
            if self.code.EPHit:
                self.cg.conf[self.code.EPHit] = ''
                self.code.boardstate[self.code.EPHit] = ''
                self.code.CheckForCheck(False)
                self.Update()
            self.full_game.append(deepcopy(self.cg.conf))
            self.AddToListbox(self.code.code)    
            self.color = (self.color + 1) % 2
            self.UpdateMoveAbility()
        
    #--------------------------------------------------------------------------     
    def AddToListbox(self, Input):
        if self.turn:
            self.turns += 1
            self.cb.lb1.configure(state = NORMAL)
            self.cb.lb1.insert(END, str(self.turns) + '.')
            self.cb.lb1.configure(state = DISABLED)
            self.cb.lb2.insert(END, Input)
            self.cb.lb3.insert(END, '')
            self.turn = False
        else:
            self.cb.lb3.delete(END)
            self.cb.lb3.insert(END, Input)
            self.turn = True
        self.cb.ListBoxDown()

    #--------------------------------------------------------------------------  
    def BindListBoxes(self):
        for lb in (self.cb.lb2, self.cb.lb3):
            for key in ('<Right>', '<Left>', '<Up>', '<Down>', '<1>'):
                lb.bind(key, self.LookBack, add=True)
        
        
    #--------------------------------------------------------------------------  
    def LookBack(self, event):
        for i in range(2):
            print 'a####################'
            try:
                print 'b'
                index = self.cb.lb2.curselection()[0]
                print 'c',index
                turn = index * 2 + 1
                print 'd',turn
            except:
                print 'e'
                index = self.cb.lb3.curselection()[0]
                print 'f',index
                turn = index * 2 + 2
                print 'g',turn
            print 'h',turn
            self.cg.conf = self.full_game[turn]
            print 'i'
            self.DisableMove()
            print 'j'
            self.Update()      
            print 'k'
            
        
###############################################################################        
class Code():
    #--------------------------------------------------------------------------
    def __init__(self, master, code, boardstate, color, rokade, EPs):
        #print '__init__'
        self.master = master
        self.code = code
        self.boardstate = deepcopy(boardstate)
        self.color = color
        self.rokade = rokade
        self.RookAfterRokade, self.RokadeDone = 0, False
        self.EPsPossible = EPs
        self.EPsCreated = []
        self.EPHit = ()
        self.error = False
        self.size = len(self.boardstate)
        self.Process()
    
    #--------------------------------------------------------------------------    
    def Process(self):
        #print 'Process'
        try:
            if self.code == '0-0-0':
                n = str(7 * (self.color))
                self.code = 'e' + n + '-c' + n
            elif self.code == '0-0':
                n = str(7 * (self.color))
                self.code = 'e' + n + '-g' + n
            if '×' in self.code:
                self.start_end = self.code.split('×')
            elif '-' in self.code:
                self.start_end = self.code.split('-')
            if self.start_end[1][-1] in ('Q', 'R', 'B', 'H'):
                self.pp = self.start_end[1][-1]
            else:
                self.pp = ''
            self.start = list('87654321').index(self.start_end[0][-1]), \
                         list('abcdefgh').index(self.start_end[0][-2])
            self.end = list('87654321').index(self.start_end[1][-1]), \
                       list('abcdefgh').index(self.start_end[1][-2])
            self.piece = self.boardstate[self.start]
            self.endpiece = self.boardstate[self.end]
            if self.endpiece:
                if (self.endpiece[1] == 'W' and self.color):
                    self.error = True
                elif (self.endpiece[1] == 'B' and not self.color):
                    self.error = True
            if not self.error:        
                if not self.piece:
                    self.error = True
                elif (self.piece[1] == 'W' and not self.color):
                    self.error = True
                elif (self.piece[1] == 'B' and self.color):
                    self.error = True
                elif self.start == self.end:
                    self.error = True
                else:
                    self.error = self.PieceControl(self.piece, self.start, \
                    self.end, self.color, self.endpiece, True, True)
            if not self.error and not self.RokadeDone:
                self.CheckForCheck()
            elif self.RokadeDone:
                self.Pos_King()
                if not self.Rook(self.RookAfterRokade[1], \
                                 [self.KW, self.KB][self.color]):
                    self.code += '+'
        except:
            self.error = True
            
    #--------------------------------------------------------------------------    
    def CheckForCheck(self, withmove = True):
        #print 'CheckForCheck'
        if withmove:
            self.Move(self.start, self.end)
        self.Pos_King()
        coverwhite, coverblack = self.CoverageField()
        if coverwhite[self.KB]:
            if not self.color:
                self.error = True
            else:
                self.code += '+'
        if coverblack[self.KW]:
            if self.color:
                self.error = True
            else:
                self.code += '+'
               
    #--------------------------------------------------------------------------      
    def PawnPromotion(self):
        #print 'PawnPromotion'
        if not self.error and (self.piece + '-')[0] == 'P' \
           and (self.end[0] == 0 or self.end[0] == 7):
            if not self.pp:
                popup = Popup(self.master, self.color, *self.end)
                self.pp = popup.pp
            self.boardstate[self.end] = self.pp
            self.code += self.pp[0]
            check = True
            if self.color:
                check = self.PieceControl(self.pp, self.end, self.KW)
            elif not self.color:
                check = self.PieceControl(self.pp, self.end, self.KB)
            if not check:
                self.code += '+'
            return True    
      
    #--------------------------------------------------------------------------   
    def Rokade(self, Type):
        #print 'Rokade'
        error = False
        if Type == 'long':
            coverwhite, coverblack = self.CoverageField()
            if not self.color:
                if coverwhite[0,4]:
                    error = True
                for n in (2,3):
                    if coverwhite[0,n] or self.boardstate[0,n]:
                        error = True
                if not self.boardstate[0,0] == 'RB':
                    error = True
                if self.boardstate[0,1]:
                    error = True                            
            else:
                if coverblack[7,4]:
                    error = True
                for n in (2,3):
                    if coverblack[7,n] or self.boardstate[7,n]:
                        error = True
                if not self.boardstate[7,0] == 'RW':
                    error = True
                if self.boardstate[7,1]:
                    error = True 
        elif Type == 'short':
            coverwhite, coverblack = self.CoverageField()
            if not self.color:
                if coverwhite[0,4]:
                    error = True
                for n in (5,6):
                    if coverwhite[0,n] or self.boardstate[0,n]:
                        error = True
                if not self.boardstate[0,0] == 'RB':
                    error = True                          
            else:
                if coverblack[7,4]:
                    error = True
                for n in (5,6):
                    if coverblack[7,n] or self.boardstate[7,n]:
                        error = True
                if not self.boardstate[7,0] == 'RW':
                    error = True
        return error
    
    #--------------------------------------------------------------------------      
    def Rook(self, start, end):
        #print 'Rook'
        error = False
        if start[0] == end[0]:
            if start[1] < end[1]:
                for n in range(1, end[1] - start[1]):
                    if self.boardstate[start[0], start[1] + n]:
                        error = True
                        break
            elif start[1] > end[1]:
                for n in range(1, start[1] - end[1]):
                    if self.boardstate[start[0], start[1] - n]:
                        error = True
                        break
        elif start[1] == end[1]:
            if start[0] < end[0]:
                for n in range(1, end[0] - start[0]):
                    if self.boardstate[start[0] + n, start[1]]:
                        error = True
                        break
            elif start[0] > end[0]:
                for n in range(1, start[0] - end[0]):
                    if self.boardstate[start[0] - n, start[1]]:
                        error = True
                        break
        else:
            error = True
        return error
        
    #--------------------------------------------------------------------------    
    def Horse(self, start, end):
        #print 'Horse'
        error = False
        if abs(start[0] - end[0]) == 2 and \
           abs(start[1] - end[1]) == 1:
            pass
        elif abs(start[0] - end[0]) == 1 and \
             abs(start[1] - end[1]) == 2:
            pass
        else:
            error = True
        return error
    
    #--------------------------------------------------------------------------            
    def Bishop(self, start, end):
        #print 'Bishop'
        error = False
        if abs(start[0] - end[0]) == abs(start[1] - end[1]):
            if start[0] < end[0]:
                if start[1] < end[1]:
                    for n in range(1, end[0] - start[0]):
                        if self.boardstate[start[0] + n, start[1] + n]:
                            error = True
                            break
                elif start[1] > end[1]:
                    for n in range(1, end[0] - start[0]):
                        if self.boardstate[start[0] + n, start[1] - n]:
                            error = True
                            break
                else:
                    error = True
            elif start[0] > end[0]:
                if start[1] < end[1]:
                    for n in range(1, start[0] - end[0]):
                        if self.boardstate[start[0] - n, start[1] + n]:
                            error = True
                            break
                elif start[1] > end[1]:
                    for n in range(1, start[0] - end[0]):
                        if self.boardstate[start[0] - n, start[1] - n]:
                            error = True
                            break
                else:
                    error = True
            else:
                error = True
        else:
            error = True
        return error
    
    #--------------------------------------------------------------------------            
    def Queen(self, start, end):
        #print 'Queen'
        return not(not self.Rook(start, end) or not self.Bishop(start, end))
        
    #--------------------------------------------------------------------------    
    def Pawn(self, color, start, end, endpiece, EP):
        #print 'Pawn'
        error = False
        if (start,end) in self.EPsPossible:
            self.EPHit = (start[0], end[1])
            self.code += ' e.p.'
        elif not color:
            if start[0] == 1 and end[0] == 3 and start[1] == end[1]:
                if self.boardstate[2, start[1]] or endpiece:
                    error = True
                elif EP:
                    if start[1] < 7:
                        if self.boardstate[3, start[1] + 1] == 'PW':
                            self.EPsCreated.append( \
                            ((3, start[1] + 1), (2, start[1])))
                    if start[1] > 0:
                        if self.boardstate[3, start[1] - 1] == 'PW':
                            self.EPsCreated.append( \
                            ((3, start[1] - 1), (2, start[1])))
            elif end[0] - start[0] == 1 and \
                 start[1] == end[1] and not endpiece:
                pass
            elif end[0] - start[0] == 1 and \
                 abs(start[1] - end[1]) == 1 and endpiece:
                pass
            else:
                error = True
        elif color:
            if start[0] == 6 and end[0] == 4 and start[1] == end[1]:
                if self.boardstate[5, start[1]] or endpiece:
                    error = True
                elif EP:
                    if start[1] < 7:
                        if self.boardstate[4, start[1] + 1] == 'PB':
                            self.EPsCreated.append( \
                            ((4, start[1] + 1), (5, start[1])))
                    if start[1] > 0:
                        if self.boardstate[4, start[1] - 1] == 'PB':
                            self.EPsCreated.append( \
                            ((4, start[1] - 1), (5, start[1])))
            elif start[0] - end[0] == 1 and \
                 start[1] == end[1] and not endpiece:
                pass
            elif start[0] - end[0] == 1 and \
                 abs(start[1] - end[1]) == 1 and endpiece:
                pass
            else:
                error = True
        return error
        
    #--------------------------------------------------------------------------    
    def King(self, start, end, rokade):
        #print 'King'
        error = False
        if rokade:
            n = 7 * self.color
            if self.rokade[self.color][0] and self.end == (n,2):
                if not self.Rokade('long'):
                    self.RookAfterRokade = ((n,0), (n,3))
                    self.code = '0-0-0'
                    self.RokadeDone = True
            elif self.rokade[self.color][1] and self.end == (n,6):
                if not self.Rokade('short'):
                    self.RookAfterRokade = ((n,7), (n,5))
                    self.code = '0-0'
                    self.RokadeDone = True
        if not self.RokadeDone:
            if abs(start[0] - end[0]) <= 1 and \
               abs(start[1] - end[1]) <= 1:
                pass
            else:
                error = True
        return error
     
    #--------------------------------------------------------------------------   
    def Move(self, start, end):
        #print 'Move'
        self.boardstate[end] = self.boardstate[start]
        self.boardstate[start] = ''
        
    #--------------------------------------------------------------------------  
    def CoverageField(self):
        #print 'CoverageField'
        coverwhite = zeros(self.size**2).reshape(self.size, self.size)
        coverblack = zeros(self.size**2).reshape(self.size, self.size)
        for n in range(self.size):
            for m in range(self.size):
                start = (n,m)
                piece = self.boardstate[start]
                if piece:
                    if piece[1] == 'W':
                        for i in range(self.size):
                            for j in range(self.size):
                                end = (i,j)
                                endpiece = self.boardstate[end]
                                if start != end and (endpiece + 'AB')[1] == 'B' \
                                   and not coverwhite[end]:
                                    if not self.PieceControl(piece, start, end, 1):
                                        coverwhite[end] = 1
                    elif piece[1] == 'B':
                        for i in range(self.size):
                            for j in range(self.size):
                                end = (i,j)
                                endpiece = self.boardstate[end]
                                if start != end and (endpiece + 'AW')[1] == 'W' \
                                   and not coverblack[end]:
                                    if not self.PieceControl(piece, start, end, 0):
                                        coverblack[end] = 1
        return coverwhite, coverblack
                                
    #--------------------------------------------------------------------------                 
    def Pos_King(self):
        #print 'Pos_King'
        for m in range(self.size):
            for n in range(self.size):
                if self.boardstate[m,n] == 'KW':
                    self.KW = (m,n)
                elif self.boardstate[m,n] == 'KB':
                    self.KB = (m,n)
                    
    #--------------------------------------------------------------------------    
    def PieceControl(self, piece, start, end, color = 0, endpiece = '-', rokade = False, EP = False):
        #print 'PieceControl'
        error = False
        if piece[0] == 'R':
            error = self.Rook(start, end)
        elif piece[0] == 'H':
            error = self.Horse(start, end)
        elif piece[0] == 'B':
            error = self.Bishop(start, end)
        elif piece[0] == 'Q':
            error = self.Queen(start, end)
        elif piece[0] == 'P':
            error = self.Pawn(color, start, end, endpiece, EP)
        elif piece[0] == 'K':
            error = self.King(start, end, rokade)
        return error
          
          
###############################################################################      
if __name__ == '__main__':
    game = Game()
    game.cb.mainloop()