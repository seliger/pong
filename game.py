import sys
import random
import pygame   

from pygame.locals import *
from pygame.rect import *

# "Constants"
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

BALL_SIZE = 20
BALL_SPEED = 3

PADDLE_HEIGHT = 100
PADDLE_WIDTH = 20
PADDLE_SPEED = 6

BORDERWIDTH = 25

# Initialize pygame
pygame.init()

# Accept repeat keys
pygame.key.set_repeat(1,10)

# Compute geometry of screen
screen_size = width, height = 1600, 900
mid_screen = width / 2, height / 2

# Instantiate our game board objects
screen = pygame.display.set_mode(screen_size)
fence = Rect(0, 0, width, height)
#midfield = 
paddles = [
    Rect(int((width * 0.15)), int(mid_screen[1] - (PADDLE_HEIGHT / 2)), PADDLE_WIDTH, PADDLE_HEIGHT),
    Rect(int((width * 0.85)), int(mid_screen[1] - (PADDLE_HEIGHT / 2)), PADDLE_WIDTH, PADDLE_HEIGHT)
    ]
ball = Rect(mid_screen[0], mid_screen[1], BALL_SIZE, BALL_SIZE)

# Randomly start the ball in one direction or the other for either axis.
# Speed is a list of two values [x, y] that drives the horizontal and
# vertical speed of the ball.
speed = [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])]
current_speed = BALL_SPEED

# Set up a clock to help control frames per second
game_clock = pygame.time.Clock()

# Main event loop
game_loop = True

# This loop will run until game_loop is set to False. When it is set
# to False by an event, the loop will exit and Pygame will shut down
# gracefully.
while game_loop:

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        game_loop = False
    if pygame.key.get_pressed()[pygame.K_q] and paddles[0].top > BORDERWIDTH:
        paddles[0].move_ip([0, -PADDLE_SPEED])
    if pygame.key.get_pressed()[pygame.K_a] and paddles[0].bottom < (height - BORDERWIDTH):
        paddles[0].move_ip([0, PADDLE_SPEED])
    if pygame.key.get_pressed()[pygame.K_p] and paddles[1].top > BORDERWIDTH:
        paddles[1].move_ip([0, -PADDLE_SPEED])
    if pygame.key.get_pressed()[pygame.K_l] and paddles[1].bottom < (height - BORDERWIDTH):
        paddles[1].move_ip([0, PADDLE_SPEED])


    # AI Code
    if (ball.left + (BALL_SIZE / 2)) < (width * 0.28) and speed[0] < 0:
        if (ball.bottom - (BALL_SIZE /2)) < paddles[0].top and paddles[0].top > BORDERWIDTH:
            paddles[0].move_ip([0, -PADDLE_SPEED])
        elif (ball.top + (BALL_SIZE /2)) > paddles[0].bottom and paddles[1].bottom < (height - BORDERWIDTH):
            paddles[0].move_ip([0, PADDLE_SPEED])

    if (ball.left + (BALL_SIZE / 2)) > (width * 0.72) and speed[0] > 0:
        if (ball.bottom - (BALL_SIZE /2)) < paddles[1].top and paddles[0].top > BORDERWIDTH:
            paddles[1].move_ip([0, -PADDLE_SPEED])
        elif (ball.top + (BALL_SIZE /2)) > paddles[1].bottom and paddles[1].bottom < (height - BORDERWIDTH):
            paddles[1].move_ip([0, PADDLE_SPEED])


    # Parse through any events that have occurred sice the last loop
    for event in pygame.event.get():            
        if event.type == pygame.QUIT:
            game_loop = False

    # Advance the ball forward, based on previously set speed parameters.
    ball.move_ip(speed)

    # If the ball touches the top or bottom border, bounce
    if ball.top < BORDERWIDTH or ball.bottom > height - BORDERWIDTH:
        speed[1] = -speed[1]

    # If the ball ends up behind a paddle, reset the ball and record the score
    if ball.left < int(width * 0.05) or ball.right > int(width * 0.95):
        current_speed = BALL_SPEED

        # Ensure the losing side gets the ball
        if ball.left < mid_screen[0]:
            speed[0] = -BALL_SPEED
        else:
            speed[0] = BALL_SPEED

        # Randomly shoot the ball up or down
        speed[1] = random.choice([-BALL_SPEED, BALL_SPEED])

        ball.update(mid_screen[0], random.randrange(BORDERWIDTH + BALL_SIZE, height - BORDERWIDTH - BALL_SIZE), BALL_SIZE, BALL_SIZE)

    # Check for other situations
    else:
        # Detect if the ball hit a paddle. The collision variable holds
        # the numeric ID of the paddle touched
        collision = ball.collidelist(paddles)
        if  collision >= 0:
            current_speed += 1
            speed[0] = -speed[0]

            # Ensure we aren't stuck in a collision
            if collision == 0:
                ball.update(paddles[collision].right + 1, ball.top, ball.height, ball.width)
            else:
                ball.update(paddles[collision].left - ball.width - 1, ball.top, ball.height, ball.width)

            # If we hit the top part of the paddle, ensure the ball bounces up
            if (ball.top - paddles[collision].top) + (BALL_SIZE / 2) < round(PADDLE_HEIGHT * 0.45):
                speed[1] = -BALL_SPEED
            # If we hit the bottom part of the paddle, ensure the ball bounces down
            elif (ball.top - paddles[collision].top) + (BALL_SIZE / 2) > round(PADDLE_HEIGHT * 0.55):
                speed[1] = BALL_SPEED 
            # If we hit the midsection, the ball bounces in a straight line
            else:
                speed[1] = 0
            

    # Place all the objects for the current frame
    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, fence, BORDERWIDTH * 2)
    for paddle in paddles:
        pygame.draw.rect(screen, GRAY, paddle)
        
    pygame.draw.rect(screen, GRAY, ball)

    # Display the new frame 
    pygame.display.update()

    # Ensure the game runs at a reasonable speed
    game_clock.tick(240)


# Shutdown pygame gracefully
pygame.quit()
