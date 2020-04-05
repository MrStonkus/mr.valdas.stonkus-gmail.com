# Simple Snake game in Python3.8
# By Valdas Stonkus

import turtle
import time
import random
import winsound
import sys

# Functions
def update_score(score):
    pen.clear()
    if score[0] > score[1]:
        score[1] = score[0]
    pen.write(f'Rezultatas: {score[0]}  Rekordas: {score[1]}  Nebežaisti \"Q\"', align='center',
              font=('Courier', 24, 'normal'))
    return score

def go_up():
    global nextDirection
    if nextDirection != 'down':
        nextDirection = 'up'
def go_down():
    global nextDirection
    if nextDirection != 'up':
        nextDirection = 'down'
def go_left():
    global nextDirection
    if nextDirection != 'right':
        nextDirection = 'left'
def go_right():
    global nextDirection
    if nextDirection != 'left':
        nextDirection = 'right'

def quit_app():
    wn.bye()

def move(nextDirection):
    if nextDirection == 'up':
        y = head.ycor()
        head.sety(y+move_step)
    if nextDirection == 'down':
        y = head.ycor()
        head.sety(y-move_step)
    if nextDirection == 'left':
        x = head.xcor()
        head.setx(x-move_step)
    if nextDirection == 'right':
        x = head.xcor()
        head.setx(x+move_step)

def game_over(score):
    time.sleep(1)
    for segment in segments:
        segment.hideturtle()
    segments.clear()
    head.goto(-10, 10)
    global nextDirection
    nextDirection = 'stop'
    score[0] = 0
    update_score(score)
    return score

def draw_grid():
    x = -300
    for ctr in range(31):  # draw 30 lines
        grid.penup()
        grid.goto(x, 300)
        grid.pendown()
        grid.goto((x, -300))
        x += 20
    y = 300
    for ctr2 in range(31):  # draw 30 lines
        grid.penup()
        grid.goto(-300, y)
        grid.pendown()
        grid.goto((300, y))
        y -= 20
    grid.hideturtle()

app_run = True
delay = 0.1
move_step = 20
nextDirection = 'stop'

segments = []  # The tail of snake
score = [0, 0]

# Set up the screen
wn = turtle.Screen()
wn.title('Snake game by @Valdas Stonkus v1.2')
wn.bgcolor('green')
wn.setup(width=1000, height=800)
wn.tracer(0)  # Turns off screen updates

grid = turtle.Turtle()
draw_grid()

# set up score
pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(0, 320)
update_score(score)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape('square')
head.color('black')
head.penup()
head.goto(-10, 10)
head.direction = 'stop'

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape('circle')
food.shapesize(0.8)
food.color('red')
food.penup()
food.goto(-10, 90)

# Keyboard bindings
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')
wn.onkeypress(quit_app, 'q')
wn.listen()

# Main game loop
while app_run:
    head.direction = nextDirection
    move(nextDirection)
    wn.update()

    # Check a collision with the border and by body
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        score = game_over(score)
    for segment in segments:
        if segment.distance(head) < 20:
            score = game_over(score)

    # Check the collision of head and food
    if head.distance(food) < 20:
        winsound.PlaySound("sound1.wav", winsound.SND_ASYNC)

        # Move the food to a random spot
        x = random.randrange(-290, 290, 20)
        y = random.randrange(-290, 290, 20)
        food.goto(x, y)

        # Update score
        score[0] += 10
        score = update_score(score)

        # Add a segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color('grey')
        new_segment.penup()
        segments.append(new_segment)

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to the head
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    time.sleep(delay)

wn.mainloop()
