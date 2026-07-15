# minesweeper
simple minesweeper game in python with tkinter  

the code is not perfect dont judge.  

# How to use
To play you should only need to download the executable dist/minesweeper.exe (I hope it works)  
If you want to modify the code, you can modify it in minesweeper.py and build it with the command 

```bash
pyinstaller --onefile --windowed --icon=flag.ico --name Minesweeper minesweeper.py
```  

Build it without `--windowed` for debugging with terminal.  
`--onefile` flag bundles your Python script and all its dependencies into a standalone executable file, you can remove this if you want too.  

# Note
`minesweeper_template.ipynb` was the original task by my teacher. The task was to implement `updateMineField`, `createMines` and `openSafePos`.  
Good thing I am a minesweeper fan so I decided to continue it further 😎👍  
