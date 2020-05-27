import tkinter as tk
from tkinter import *

root = tk.Tk()
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )

mylist = Listbox(root, yscrollcommand = scrollbar.set )
for line in range(100):
   test = tk.Label(root, text = "Green Dot", padx = 10, font=("Arial", 10))#.grid(row = k*4+1, column = 1)
   mylist.insert(END, test)

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()