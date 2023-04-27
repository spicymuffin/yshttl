import turtle
import random
import time
turtle.setup(500, 500)

window = turtle.Screen()
window.title("kill me")

the_turtle = turtle.getturtle()
the_turtle.speed(0)
while True:
    the_turtle.right(random.randint(-45, 45))
    the_turtle.forward(20)

    if the_turtle.position()[0] > 250:
        the_turtle.penup()
        the_turtle.setposition(-250, the_turtle.position()[1])
        the_turtle.pendown()
    if the_turtle.position()[0] < -250:
        the_turtle.penup()
        the_turtle.setposition(250, the_turtle.position()[1])
        the_turtle.pendown()
    if the_turtle.position()[1] > 250:
        the_turtle.penup()
        the_turtle.setposition(the_turtle.position()[1], -250)
        the_turtle.pendown()
    if the_turtle.position()[1] < -250:
        the_turtle.penup()
        the_turtle.setposition(the_turtle.position()[1], 250)
        the_turtle.pendown()
