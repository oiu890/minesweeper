# pyinstaller --onefile --windowed --icon=flag.ico --name Minesweeper minesweeper.py
# pyinstaller --onefile --icon=flag.ico --name Minesweeper_Debug minesweeper.py

from tkinter import *
from tkinter import messagebox
from random import sample
import time

class mineSweeper(Frame):
    def __init__(self, rows, cols):
        Frame.__init__(self)
        self.rows = rows
        self.cols = cols

        # trying to scale it bigger
        maxDim = max(rows, cols)
        fontSize = max(8, min(16, 240 // maxDim))
        self.cellFont = ("Arial", fontSize)
        print(fontSize)
        # so that my (self proclaimed) amazing clock detail can show
        topFontSize = 24
        self.topFont = ("Arial", topFontSize)

        self.mineFields = []
        self.mines = []
        self.count = 0
        self.gameOver = False
        # initialize the mineFields 2D list (row x col) with each cell a list
        # containing a button and a number indicating the number of mines a round it.
        self.retryBtn = Button(self, text="Retry", command=self.restart)
        self.retryBtn.grid(row=self.rows+1, column=0, columnspan=self.cols//2, sticky="ew")

        self.quitBtn = Button(self, text="Quit", command=self.winfo_toplevel().destroy)
        self.quitBtn.grid(row=self.rows+1,column=self.cols//2,columnspan=self.cols-self.cols//2,sticky="ew")
        
        self.menuBtn = Button(self, text="Menu", command=self.menu)
        self.menuBtn.grid(row = self.rows+2,column=0,columnspan=self.cols,sticky="ew")

        self.neighbours =  [
                [-1,-1],[-1,0],[-1,1],
                [0,-1],        [0,1],
                [1,-1],[1,0],[1,1]
            ]
        # top left: (r-1,c-1), top left: (r-1,c+1)
        # bottom left: (r+1,c-1), bottom right: (r+1,c+1)

        for r in range(rows):
            temp = []
            for c in range(cols):
                b = Button(self, height=1, width=2,font=self.cellFont)
                if (r+c)%2 == 0:
                    # print(cols%2,r)
                    b.config(bg = "DarkOliveGreen2") #1,3,5 (even rows)
                else:
                    b.config(bg = "DarkOliveGreen1") #0,2,4 (all)
                
           
                b.grid(row=r+1, column=c)
                b.bind('<Button-3>', self.clickButton(r, c, 'R'))
                b.bind('<Button-1>', self.clickButton(r, c, 'L'))
         
                temp.append([b,0])
            self.mineFields.append(temp)

        # print(self.mineFields)

        # self.grid() positions and displays the current object instance (self) 
        # within its parent container using a two-dimensional grid
        self.grid()


        # Randomly convert 10% of the mineFields into mines
        self.createMines()
        # Update the number of mines around each cell.
        self.updateMineField()

        self.flagCount = 0
        self.flagVar = StringVar()
        self.flagVar.set(f"🚩 x{len(self.mines)}")
        self.flagLabel = Label(self, textvariable=self.flagVar,font = self.topFont)
        self.flagLabel.grid(row=0, column=0, columnspan=self.cols//2, sticky="ew")
        # self.mainloop()
        # timer
        self.clocks = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚']
        self.startTime = 0
        self.timerRunning = False
        self.elapsed = 0
        self.timeVar = StringVar()
        self.timeVar.set("🕛 0")
        self.curclock = 0
        self.timerLabel = Label(self,textvariable=self.timeVar,font = self.topFont)
        self.timerLabel.grid(row=0, column=self.cols//2,columnspan=self.cols - self.cols//2,sticky = "ew")


        
    def clickButton(self, r, c, clickType):

        def helper(event):
            if self.gameOver:
                return
            if not self.timerRunning:
                self.startTimer()

            print(clickType + " Click @ " + str(r) + ", " + str(c))

            if clickType == 'L':
                if self.mineFields[r][c][0]["text"] == "🚩":
                    return #its a flag, dont open it
                
                if self.mineFields[r][c][0]["state"] == DISABLED and self.mineFields[r][c][0]["text"] != "🚩":
                    # tried to implement chording
                    self.check_mines(r,c)
                    return

                if self.mineFields[r][c][1] != -1: #safe
                    self.openSafePos(r,c)
                else:
                    self.game_over(r,c)
                    
            elif clickType == "R":
                # print(self.mineFields[r][c][0]["state"])
                # check if its a flag alr, check that its not a number??
                if self.mineFields[r][c][0]["text"] == "":
                    self.mineFields[r][c][0]["text"] = "🚩"
                    self.mineFields[r][c][0].config(state = DISABLED)
                    self.flagCount += 1

                elif not self.mineFields[r][c][0]["text"].isdigit(): 
                    # print(self.mineFields[r][c][0]["text"],'text')
                    self.mineFields[r][c][0]["text"] = ""
                    self.mineFields[r][c][0].config(state = NORMAL)
                    self.flagCount -= 1
                self.flagVar.set(f"🚩 x{len(self.mines) - self.flagCount}")
                # self.mineFields[r][c][0].config(state = DISABLED)

            self.check_win()

            # print(self.count,'count',(self.rows*self.cols),int(0.1 * (self.rows*self.cols)), (self.rows*self.cols) - int(0.1 * (self.rows*self.cols)))
            

        return helper

    def openSafePos(self, r, c):
        # recursively open up all cells (by calling openSafePos) that do not have mines
        # that are connected to cell at (r,c)
        # print()
        print('opening',r,c)
        # if self.mine

        if self.mineFields[r][c][0]["state"] == DISABLED: #opened
            return 
        button = self.mineFields[r][c][0]
        val = self.mineFields[r][c][1]
        
        button.config(relief = SUNKEN,state = DISABLED)
        # button.config(bg = "khaki")
        if (r+c)%2 == 0:
            button.config(bg = "bisque")
        else:
            button.config(bg = "blanched almond")

        
        self.count += 1

        # if val isnt 0 then its a number and you should display
        # recursion stops at a number as well
        if val != 0:
            button["text"] = str(val)
            return

        rows = self.rows
        cols = self.cols
        #iterate a 3x3 grid around the cell
        for dr, dc in self.neighbours:
            nr = r + dr
            nc = c + dc
            if (nr < 0) or (nr >= rows) or (nc < 0) or (nc >= cols):
                continue #out of valid range
            
            if self.mineFields[nr][nc][1] != -1: #recursively open if not a bomb
                self.openSafePos(nr,nc)
         
    def check_mines(self,r,c):
        num_mines = int(self.mineFields[r][c][1])


        rows = self.rows
        cols = self.cols
        mc = 0
        safes = []
        for dr, dc in self.neighbours:
            nr = r + dr
            nc = c + dc
            if (nr < 0) or (nr >= rows) or (nc < 0) or (nc >= cols):
                continue #out of valid range
            if self.mineFields[nr][nc][0]["text"] == "🚩":
                mc += 1
            else:
                safes.append([nr,nc])

        if mc == num_mines:
            for rr, cc in safes:
                if self.mineFields[rr][cc][1] == -1:
                    self.game_over(rr,cc)
                
                    return
                else:
                    self.openSafePos(rr, cc)
        self.check_win()
            
    def createMines(self):
        # -1: mine
        # 0-8: number of mines around
        coords = [(i,j) for i in range(self.rows) for j in range(self.cols)]
        # print(coords)
        density = 0.15 + (0.05625  * ((self.rows*self.cols - 64)/416))
        num_mines = int(density * (self.rows*self.cols))
        # print(num_mines)
        mines = sample(coords,num_mines)
        # print(mines,'sample mines')
        self.mines = mines
        for coord in mines:
            row = coord[0]
            col = coord[1]
            self.mineFields[row][col][1] = -1
            #update surrounding mines
            # neighbours = [
            #     [-1,-1],[-1,0],[-1,1],
            #     [0,-1],        [0,1],
            #     [1,-1],[-1,0],[1,1]
            # ]

            # top left: (r-1,c-1), top left: (r-1,c+1)
            # bottom left: (r+1,c-1), bottom right: (r+1,c+1)


    def updateMineField(self):
        # update the mineFields after mines are created
        # for example, self.mineFields[3][3][1] = 7
        # this means that the number of mines around the cell at (3,3) is 7
        # pass 
        rows = self.rows
        cols = self.cols
        # print(self.mines,'mines')
        for mine in self.mines:
            miner = mine[0]
            minec = mine[1]
            # print(miner,minec,'mine coord')
            for dr, dc in self.neighbours:
                nr  = dr + miner
                nc = dc + minec
                # print(nr,nc,(dr,dc))
                if (nr < 0) or (nr >= rows) or (nc < 0) or (nc >= cols):
                    continue #out of valid range
             
                # print(grid[nr][nc][1])
                if self.mineFields[nr][nc][1] == -1:
                    continue #its a mine
                else:
                    self.mineFields[nr][nc][1] += 1
                
                # self.mineFields[nr][nc][1] +
    def game_over(self, r, c):
        self.stopTimer()
        self.gameOver = True
        colour = "red"
        self.mineFields[r][c][0].config(text="💣", bg=colour)
        # self.display_all()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.mineFields[r][c][1] == -1:
                    self.mineFields[r][c][0].config(state = DISABLED,text = "💣",relief = SUNKEN,bg = colour)
        
        messagebox.showinfo("GG", "Game Over")
        
    def startTimer(self):
        if not self.timerRunning:
            self.timerRunning = True
            self.startTime = time.time()
            self.updateTimer()
        
    def updateTimer(self):
        if self.timerRunning:
            self.elapsed = int(time.time() - self.startTime)
            clocks = self.clocks
            self.curclock = self.curclock%12
            # self.curclock += 1
            print(self.curclock,'new update',self.elapsed)    
                
            self.timeVar.set(f"{clocks[self.curclock]} {self.elapsed}")
            self.curclock += 1
            self.after(1000,self.updateTimer)

    def stopTimer(self):
        self.elapsed = int(time.time() - self.startTime)
        clocks = self.clocks
        self.timeVar.set(f"{clocks[self.curclock]} {self.elapsed}")
        self.timerRunning = False

    def restart(self):
        # root = self.winfo_toplevel()
        self.destroy() 
        # StartMenu(root)
        mineSweeper(self.rows,self.cols)
    
    def menu(self):
        root = self.winfo_toplevel()
        self.destroy()
        StartMenu(root)
        centerWindow(root)

    def check_win(self):
        if self.count == self.rows * self.cols - len(self.mines):
            self.stopTimer()
            messagebox.showinfo("GG", f"WIN! Time: {self.elapsed}s")




class StartMenu:
    def __init__(self, root):

        self.root = root
        root.title("Minesweeper Setup")

        Label(root, text="Rows:").grid(row=3, column=0)
        Label(root, text="Columns:").grid(row=4, column=0)

        self.rowsEntry = Entry(root)
        self.colsEntry = Entry(root)

        self.rowsEntry.insert(0, "10")
        self.colsEntry.insert(0, "10")

        self.rowsEntry.grid(row=3, column=1)
        self.colsEntry.grid(row=4, column=1)
        Button(root,text="Easy (9x9)",
            command=lambda:self.start(9,9)).grid(row=0, column=0, columnspan=2, sticky="ew")

        Button(root,text="Medium (16x16)",
            command=lambda:self.start(16,16)).grid(row=1, column=0, columnspan=2, sticky="ew")

        Button(root,text="Hard (20x34)",
            command=lambda:self.start(20,24)).grid(row=2, column=0, columnspan=2, sticky="ew")

        Button(
            root,
            text="Start Game",
            command=lambda: self.start(self.rowsEntry.get(),self.colsEntry.get())
        ).grid(row=5, column=0,columnspan = 2,sticky='ew')

        Button(root,text = "Quit",command=lambda: self.root.winfo_toplevel().destroy()).grid(row=6,column=0,columnspan = 2,sticky='ew')

    def start(self,r,c):
        # just some input validation 
        try:
            r,c = int(r),int(c)
        except ValueError:
            messagebox.showerror("Invalid input","Please enter only numbers")

        if r *c > 2000: 
            messagebox.showerror(
                "TOO LARGE :(","Max 2000 cells sorry"
            )
            return
        if r< 5 or c< 5:
            messagebox.showerror("TOO SMALL :(","min 5x5 size")
            return
        
        self.root.destroy() 

        game = Tk()
        # centerWindow(game)
        game.title("Minesweeper")
        mineSweeper(r,c)
        centerWindow(game)
        

def centerWindow(win):
    # this is supposed to centre the window but it doesnt rlly work properly for some reason..?
    # oh i fixed it HAHAHAH was calling it before mineSweeper initialised (wrong), should be called after
    win.update_idletasks()
    w = win.winfo_reqwidth()
    h = win.winfo_reqheight()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    root = Tk()
    StartMenu(root)
    centerWindow(root)
    root.mainloop()