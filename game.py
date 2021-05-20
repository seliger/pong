import sys
import random
import pygame

from pygame.locals import *
from pygame.rect import *

# "Constants"
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (180, 180, 180)

BALL_SIZE = 15
BALL_SPEED = 12

PADDLE_HEIGHT = 80
PADDLE_WIDTH = 10
PADDLE_SPEED = 24

BORDERWIDTH = 10


# Initialize pygame
pygame.init()


# Compute geometry of screen
screen_info = pygame.display.Info()
screen_size = width, height = (screen_info.current_w, screen_info.current_h)
mid_screen = width / 2, height / 2

# Instantiate our game board objects
screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
#midfield =
paddles = [
    Rect(int((width * 0.10)), int(mid_screen[1] - (PADDLE_HEIGHT / 2)), PADDLE_WIDTH, PADDLE_HEIGHT),
    Rect(int((width * 0.90)), int(mid_screen[1] - (PADDLE_HEIGHT / 2)), PADDLE_WIDTH, PADDLE_HEIGHT)
    ]
ball = Rect(mid_screen[0], mid_screen[1], BALL_SIZE, BALL_SIZE)


pygame.display.set_caption("Pong")

# Accept repeat keys
pygame.key.set_repeat(1,10)


def draw_borders(s, x, y, w, h, bw, c):
    pygame.draw.rect(s, c, (x, y, w, bw))
    pygame.draw.rect(s, c, (x, y+h-bw, w, bw))
    pygame.draw.rect(s, c, (x, y, bw, h))
    pygame.draw.rect(s, c, (x+w-bw, y, bw, h))


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
    if ball.left < (width * 0.28) and speed[0] < 0:
        if ball.bottom < paddles[0].top and paddles[0].top > BORDERWIDTH:
            paddles[0].move_ip([0, -PADDLE_SPEED])

        elif ball.top > paddles[0].bottom and paddles[1].bottom < (height - BORDERWIDTH):
            paddles[0].move_ip([0, PADDLE_SPEED])

    if ball.right > (width * 0.72) and speed[0] > 0:
        if ball.bottom < paddles[1].top and paddles[0].top > BORDERWIDTH:
            paddles[1].move_ip([0, -PADDLE_SPEED])
        elif ball.top > paddles[1].bottom and paddles[1].bottom < (height - BORDERWIDTH):
            paddles[1].move_ip([0, PADDLE_SPEED])

    # Check the paddles to make sure they don't exceed the border walls
    for paddle in paddles:
        if paddle.top < BORDERWIDTH:
            paddle.move_ip([0, BORDERWIDTH - paddle.top])
        elif paddle.bottom > height - BORDERWIDTH:
            paddle.move_ip([0, -(BORDERWIDTH - (height - paddle.bottom))])

    # Parse through any events that have occurred sice the last loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    # Advance the ball forward, based on previously set speed parameters.
    ball.move_ip(speed)

    # # If the ball touches the top or bottom border, bounce
    # if ball.top < BORDERWIDTH or ball.bottom > height - BORDERWIDTH:
    #     speed[1] = -speed[1]

    # Check to ensure the ball is within the fence, else adjust accordingly
    if ball.top < BORDERWIDTH:
        ball.move_ip([0, BORDERWIDTH - ball.top])
        speed[1] = -speed[1]
    elif ball.bottom > height - BORDERWIDTH:
        ball.move_ip([0, -(BORDERWIDTH - (height - ball.bottom))])
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

    draw_borders(screen, 0, 0, width, height, BORDERWIDTH, GRAY)

    for paddle in paddles:
        pygame.draw.rect(screen, GRAY, paddle)

    pygame.draw.rect(screen, GRAY, ball)

    # Display the new frame
    pygame.display.update()

    # Ensure the game runs at a reasonable speed
    game_clock.tick(60)


# Shutdown pygame gracefully
pygame.quit()
