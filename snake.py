##snake.py
##Keaton "Lil Keet" Payne
##4/1/20

#Quick var changes
##Argument may be a string or a tuple of three
##numbers corresponding to actual colormode
bordercol = "Red"
foodcol = "Red"
headcol = "Black"
tailcol = "Gray"
backgroundcol = "White"

##'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'
##Circle and square are best, as the turtles don't actually
##turn direction. It looks awkward with other shapes
headshape = "Square"
tailshape = "Square"
foodshape = "Circle"

##Max length of snake (mostly for debug or startup speed)
tailnum = 361

##Time in between movements in miliseconds (1000 in 1 second)
delay = 500


import turtle
import tkinter as tk
from random import choice

import os
import sys



def forward(event=None):
    #Disable manual movement
    root.bind("<space>", lambda e: None)
    
    
    #Store old coordinates for first tail
    pos = coords["t"] = t.pos()
    for i in range(tailnum):
        coords[i] = globals()["t" + str(i)].pos()
    
    #Get coordinates of main turtle
    x = pos[0]
    y = pos[1]
    
    #Determine direction and change coordinates accordingly
    if north:
        y += 25
    elif east:
        x += 25
    elif south:
        y -= 25
    elif west:
        x -= 25
        
    t.goto(x, y)
    
    #Check if user has found the food turtle
    if (x, y) == food.pos():
        newfood()
    #Or is out of bounds
    elif x not in field or y not in field:
        endgame()
    #Or is on his own tail
    elif length > 0:
        for i in range(length):
            if (x, y) == coords[i]:
                endgame()
    
    #Move tail turtles
    for i in range(length):
        currentturt = globals()["t" + str(i)]
        if i == 0:
            currentturt.goto(coords["t"])
        else:
            currentturt.goto(coords[i - 1])   
        currentturt.showturtle()
        
    #Loop forward movement
    turtscreen.update()
    root.after(delay, forward)


#Food turtle moves location and score increases
def newfood():
    #Change vars
    global length
    global score
    global delay
    length += 1
    score.set("Score: " + str(length))
    delay = int(delay * .99)
    
    #Move food turtle
    food.hideturtle()
    
    #Make sure not to appear on another turtle
    while True:
        x = choice(field)
        y = choice(field)
        
        for i in range(tailnum):
            if (x, y) == coords[i]:
                break
        else:
            if (x, y) != coords["t"] and (x, y) != t.pos():
                break
        
    food.goto(x, y)
    food.showturtle()
    turtscreen.update()
        
def endgame():
    #Disable movement
    global forward
    def forward(event=None):
        pass
    
    ender.write("GAME OVER", font=("Times New Roman", 16, "normal"), align="center")
    ender.goto(0, -25)
    ender.write("Score: " + str(length), font=("Times New Roman", 16, "normal"), align="center")
    ender.goto(0, 0)
    endgamebtn.configure(text="End Game", command = e)
    turtscreen.update()
    
#Restarts program
def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)
    
    
        
#Functions that change direction variable
#
#(event var is the keypress info, in the format
#of keysym=w keycode=87 char='w' x=702 y=322)
def n(event=None):
    global north
    global east
    global south
    global west
    
    if not south:
        north = True
        east = west = False
    
def e(event=None):
    global north
    global east
    global south
    global west
    
    if not west:
        east = True
        north = south = False    
    
def s(event=None):
    global north
    global east
    global south
    global west
    
    if not north:
        south = True
        east = west = False    

def w(event=None):
    global north
    global east
    global south
    global west
    
    if not east:
        west = True
        south = north = False    



#Startup Window
startup = tk.Tk()
startup.title("Snake")

#Option Radiobuttons
difficulties = [
    ("Peaceful", 500),
    ("Easy", 300),
    ("Normal", 200),
    ("Hard", 100),
    ("Insane", 50)
    ]
colors = ("Red", "Black", "Gray", "White", "Blue", "Green", "Gold", "Purple")
shapes = ("Square", "Circle", "Triangle")

delaytk = tk.IntVar()
delaytk.set(300)

bordercoltk = tk.StringVar()
bordercoltk.set(bordercol)
backgroundcoltk = tk.StringVar()
backgroundcoltk.set(backgroundcol)
foodcoltk = tk.StringVar()
foodcoltk.set(foodcol)
headcoltk = tk.StringVar()
headcoltk.set(headcol)
tailcoltk = tk.StringVar()
tailcoltk.set(tailcol)
coldict = {"Border":bordercoltk, "Background":backgroundcoltk, "Food":foodcoltk, "Head":headcoltk, "Tail":tailcoltk}

headshapetk = tk.StringVar()
headshapetk.set(headshape)
tailshapetk = tk.StringVar()
tailshapetk.set(tailshape)
foodshapetk = tk.StringVar()
foodshapetk.set(foodshape)
shapedict = {"Head":headshapetk, "Tail":tailshapetk, "Food":foodshapetk}


#Add startup widgets
tk.Label(startup, text="Difficulty:", padx=10, pady=15).grid(row=0)
for text, time in difficulties:
    btn = tk.Radiobutton(startup, text=text, variable=delaytk, value=time, indicatoron=0, cursor="hand2", padx=10, pady=5)
    btn.grid(row=0, column=(difficulties.index((text, time))) + 1)

tk.Label(startup, text="Select A Color", padx=10, pady=15).grid(row=1, column=0, columnspan=(len(colors) + 1))

rowcount = 2
for string, tkvar in coldict.items():
    tk.Label(startup, text=(string + ":")).grid(row=rowcount)
    for color in colors:
        btn = tk.Radiobutton(startup, text=color, variable=tkvar, value=color, indicatoron=0, cursor="hand2", padx=10, pady=5)
        btn.grid(row=rowcount, column=(colors.index(color) + 1))
    rowcount += 1

tk.Label(startup, text="Select A Shape", padx=10, pady=15).grid(row=rowcount, column=0, columnspan=(len(colors) + 1))
rowcount += 1

for string, tkvar in shapedict.items():
    tk.Label(startup, text=(string + ":")).grid(row=rowcount)
    for shape in shapes:
        btn = tk.Radiobutton(startup, text=shape, variable=tkvar, value=shape, indicatoron=0, cursor="hand2", padx=10, pady=5)
        btn.grid(row=rowcount, column=(shapes.index(shape) + 1))
    rowcount += 1    

tk.Label(startup, text="").grid(row=99) #just for spacing
tk.Button(startup, text="Start", command=startup.destroy, cursor="hand2").grid(row=100, column=0)
tk.Button(startup, text="Exit", command=exit, cursor="hand2").grid(row=100, column=1000)

#Start the startup window
startup.maxsize(668, 447)
startup.minsize(668, 447)
startup.mainloop()
    


#Start tkinter and turtle
root = tk.Tk()
canvas = tk.Canvas(master = root, width = 500, height = 500)
turtscreen = turtle.TurtleScreen(canvas)
turtscreen.bgcolor(backgroundcoltk.get())
canvas.pack()

#Stop the screen from updating
turtscreen.tracer(0, 0)

#Important vars
field = range(-225, 250, 25)
coords = {}
length = -1

#Tk Variables
score = tk.StringVar()
score.set("Score: " + str(length))

delay = delaytk.get()

bordercol = bordercoltk.get()
foodcol = foodcoltk.get()
headcol = headcoltk.get()
tailcol = tailcoltk.get()

headshape = headshapetk.get().lower()
tailshape = tailshapetk.get().lower()
foodshape = foodshapetk.get().lower()

#Initiate turtles
t = turtle.RawTurtle(turtscreen)
food = turtle.RawTurtle(turtscreen)
ender = turtle.RawTurtle(turtscreen)

#The "tails"
for i in range(tailnum):
    turt = globals()["t" + str(i)] = turtle.RawTurtle(turtscreen)
    turt.hideturtle()
    turt.up()
    turt.speed(0)
    turt.shape(tailshape)
    turt.color(tailcol)
    coords[i] = turt.pos()
    
#Setup
t.up()
t.shape(headshape)
t.color(headcol)
t.speed(1)
coords["t"] = t.pos()

food.up()
food.shape("circle")
food.speed(0)

ender.hideturtle()
ender.up()

#Border wall
food.goto(-250, -250)
food.seth(0)
food.down()
food.color(bordercol)
food.pensize(25)
for side in range(4):
    food.fd(500)
    food.left(90)
food.up()
food.color(foodcol)

newfood()

#Tkinter Buttons and Labels at bottom of window

tk.Label(root, textvariable=score).pack(side=tk.LEFT)
tk.Button(root, text="Exit", command=exit, cursor="hand2").pack(side = tk.RIGHT)
endgamebtn = tk.Button(root, text="End Game", command=endgame, cursor="hand2").pack(side = tk.RIGHT)
tk.Button(root, text="Restart", command=restart, cursor="hand2").pack(side = tk.RIGHT)

#Bind keyboard presses to directions
root.bind("w", n)
root.bind("d", e)
root.bind("a", w)
root.bind("s", s)

root.bind("<space>", forward)

#Starts program
west = False
e()
turtscreen.update()
root.title("Snake")
root.maxsize(500, 530)
root.minsize(500, 530)
root.mainloop()
