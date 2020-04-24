##snake.py
##Keaton "Lil Keet" Payne
##4/1/20

#Quick var changes
##Argument may be a string or a tuple of three
##numbers corresponding to actual colormode
bordercol = "red"
foodcol = "red"
headcol = "black"
tailcol = "gray"

##'arrow', 'turtle', 'circle', 'square', 'triangle', 'classic'
##Circle and square are best, as the turtles don't actually
##turn direction. It looks awkward with other shapes
headshape = "square"
tailshape = "square"
foodshape = "circle"

##Max length of snake (mostly for debug or startup speed)
tailnum = 361

##Time in between movements in miliseconds (1000 in 1 second)
delay = 150


import turtle
import tkinter as tk
from random import choice


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
    turtscreen.update()

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


    
    
    
#Start tkinter and turtle
root = tk.Tk()
canvas = tk.Canvas(master = root, width = 500, height = 500)
turtscreen = turtle.TurtleScreen(canvas)
canvas.pack()

#Stop the screen from updating
turtscreen.tracer(0, 0)

#Important vars
field = range(-225, 250, 25)
coords = {}
length = -1

score = tk.StringVar()
score.set("Score: " + str(length))

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

#Bind keyboard presses to directions
tk.Label(root, textvariable=score).pack(side = tk.LEFT)
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
root.mainloop()
