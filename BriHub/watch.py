# [green_dot, green_dot_days,boll_band_sq,boll_band_sq_days, boll_band_dip, 
#    'IP', 'IP', 'IP', daily_rwb, stochastic, stoch_under, 'IP', 'IP', 'IP','IP']

import tkinter as tk


# grab the data - update this with a date check plz
file = open('dataset.txt', 'r')
input = file.readlines()
file.close()

stock = []
green_dot = []
green_dot_days = []
boll_band_sq = []
boll_band_sq_days = []
boll_band_dip = []
# IP
# IP
# IP
daily_rwb = [] 
stochastic = []
stoch_under = []
# IP
# IP
# IP
# IP


for j in range(0, len(input)):
    
    splat = input[j].split(" ")
    
    # assign each stock value to its name, ensure type
    stock.append(splat[0])
    green_dot.append(splat[1])
    green_dot_days.append(int(splat[2]))
    boll_band_sq.append(splat[3])
    boll_band_sq_days.append(int(splat[4]))
    boll_band_dip.append(splat[5])
    # IP
    # IP
    # IP
    daily_rwb.append(splat[9])
    stochastic.append(float(splat[10]))
    stoch_under.append(splat[11])
    # IP
    # IP
    # IP
    # IP
    
    # clean up some values
    if(green_dot_days[j] == 6969): 
        green_dot_days[j] = "N/A"
    if(boll_band_sq_days[j] == '6969'): 
        boll_band_sq_days[j] = "N/A"
    stochastic[j] = round(stochastic[j], 2)
    
# now its time to build the GUI

root = tk.Tk()
root.wm_title("Watchlist")

# scrollbar = Scrollbar(root)
# scrollbar.grid(column = 15)

# image_green = tk.PhotoImage(file="green.gif")
# image_blue = tk.PhotoImage(file="blue.gif")
# image_red = tk.PhotoImage(file="red.gif")

tk.Label(root, text = "Stock",padx = 10, font=("Arial", 10)).grid(row = 0, column = 0)
tk.Label(root, text = "GDOT", padx = 5, font=("Arial", 10)).grid(row = 0, column = 1)
tk.Label(root, text = "BBSQ", padx = 5, font=("Arial", 10)).grid(row = 0, column = 2)
tk.Label(root, text = "BBDP", padx = 5, font=("Arial", 10)).grid(row = 0, column = 3)
tk.Label(root, text = "GLBO", padx = 5, font=("Arial", 10)).grid(row = 0, column = 4)
tk.Label(root, text = "StUn", padx = 5, font=("Arial", 10)).grid(row = 0, column = 5)
tk.Label(root, text = "Stg2", padx = 5, font=("Arial", 10)).grid(row = 0, column = 6)
tk.Label(root, text = "DRWB", padx = 5, font=("Arial", 10)).grid(row = 0, column = 7)
tk.Label(root, text = "Dist", padx = 5, font=("Arial", 10)).grid(row = 0, column = 8)
tk.Label(root, text = "BGrL", padx = 5, font=("Arial", 10)).grid(row = 0, column = 9)
tk.Label(root, text = "",     padx = 10, font=("Arial", 10)).grid(row = 0, column = 10)
tk.Label(root, text = "Stock",padx = 10, font=("Arial", 10)).grid(row = 0, column =11)
tk.Label(root, text = "GDOT", padx = 5, font=("Arial", 10)).grid(row = 0, column = 12)
tk.Label(root, text = "BBSQ", padx = 5, font=("Arial", 10)).grid(row = 0, column = 13)
tk.Label(root, text = "BBDP", padx = 5, font=("Arial", 10)).grid(row = 0, column = 14)
tk.Label(root, text = "GLBO", padx = 5, font=("Arial", 10)).grid(row = 0, column = 15)
tk.Label(root, text = "StUn", padx = 5, font=("Arial", 10)).grid(row = 0, column = 16)
tk.Label(root, text = "Stg2", padx = 5, font=("Arial", 10)).grid(row = 0, column = 17)
tk.Label(root, text = "DRWB", padx = 5, font=("Arial", 10)).grid(row = 0, column = 18)
tk.Label(root, text = "Dist", padx = 5, font=("Arial", 10)).grid(row = 0, column = 19)
tk.Label(root, text = "BGrL", padx = 5, font=("Arial", 10)).grid(row = 0, column = 20)
tk.Label(root, text = "",     padx = 10, font=("Arial", 10)).grid(row = 0, column = 21)
tk.Label(root, text = "Stock",padx = 10, font=("Arial", 10)).grid(row = 0, column =22)
tk.Label(root, text = "GDOT", padx = 5, font=("Arial", 10)).grid(row = 0, column = 23)
tk.Label(root, text = "BBSQ", padx = 5, font=("Arial", 10)).grid(row = 0, column = 24)
tk.Label(root, text = "BBDP", padx = 5, font=("Arial", 10)).grid(row = 0, column = 25)
tk.Label(root, text = "GLBO", padx = 5, font=("Arial", 10)).grid(row = 0, column = 26)
tk.Label(root, text = "StUn", padx = 5, font=("Arial", 10)).grid(row = 0, column = 27)
tk.Label(root, text = "Stg2", padx = 5, font=("Arial", 10)).grid(row = 0, column = 28)
tk.Label(root, text = "DRWB", padx = 5, font=("Arial", 10)).grid(row = 0, column = 29)
tk.Label(root, text = "Dist", padx = 5, font=("Arial", 10)).grid(row = 0, column = 30)
tk.Label(root, text = "BGrL", padx = 5, font=("Arial", 10)).grid(row = 0, column = 31)

offset = 33

for k in range(0, offset):
    
    # stock name
    tk.Label(root, text = stock[k], font=("Arial", 10)).grid(row = k+1, column = 0)
    tk.Label(root, text = stock[k+offset], font=("Arial", 10)).grid(row = k+1, column = 11)
    tk.Label(root, text = stock[k+2*offset], font=("Arial", 10)).grid(row = k+1, column = 22)
    
    # green dot - days are in the middle 
    if (green_dot[k] == 'True'):
        tk.Label(root, text = green_dot_days[k], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 1)
    if (green_dot[k+offset] == 'True'):
        tk.Label(root, text = green_dot_days[k+offset], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 12)
    if (green_dot[k+offset] == 'True'):
        tk.Label(root, text = green_dot_days[k+2*offset], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 23)
        
    # bb sq - days are in the middle 
    if (boll_band_sq[k] == 'True'):
        tk.Label(root, text = boll_band_sq_days[k], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 2)
    if (boll_band_sq[k+offset] == 'True'):
        tk.Label(root, text = boll_band_sq_days[k+offset], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 13)    
    if (boll_band_sq[k+2*offset] == 'True'):
        tk.Label(root, text = boll_band_sq_days[k+2*offset], padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column =24)    
    
    # bb dip 
    if (boll_band_dip[k] == 'True'):
        tk.Label(root, text = " ", padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 3)
    if (boll_band_dip[k+offset] == 'True'):
        tk.Label(root, text = " ", padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 14) 
    if (boll_band_dip[k+2*offset] == 'True'):
        tk.Label(root, text = " ", padx = 10, bg = 'green', font=("Arial", 10)).grid(row = k+1, column = 25) 
    
    # IP Green Line Breakouts
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 4)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 15)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 26)
    
    # stoch_under
    if (stoch_under[k] == 'True'):
        tk.Label(root, text = stochastic[k], padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 5)
    if (stoch_under[k+offset] == 'True'):
        tk.Label(root, text = stochastic[k+offset], padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 16)
    if (stoch_under[k+2*offset] == 'True'):
        tk.Label(root, text = stochastic[k+2*offset], padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 27)
    
    # IP Stage 2
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 6)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 17)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 28)
    
    # rwb indicator
    if (daily_rwb[k] == 'True'):
        tk.Label(root, text = " ", padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 7)
    if (daily_rwb[k+offset] == 'True'):
        tk.Label(root, text = " " , padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 18)
    if (daily_rwb[k+2*offset] == 'True'):
        tk.Label(root, text = " " , padx = 10, bg = 'blue', font=("Arial", 10)).grid(row = k+1, column = 29)    
        
    # IP dist. days
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 8)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 19)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 30)
    # IP Stage below green line
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 9)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 20)
    tk.Label(root, text = "IP", padx = 10, font=("Arial", 10)).grid(row = k+1, column = 31)



# show window
root.mainloop()