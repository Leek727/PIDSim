import pygame
import numpy as np
import random

pygame.init()

width, height = 1000, 1000
# Set up the drawing window
screen = pygame.display.set_mode([width, height])


# constants
dt = .01
g = 9.81
mu_k = 0.31
mu_s = 0.31

class Body:
    def __init__(self, x, m, v):
        # position, mass, velocity
        self.x = x
        self.m = m
        self.v = v

    def update(self,F=0):
        # apply a force to the body for a single timestep
        N = self.m * g
        f = 0
        if self.v == 0:
            # static friction
            f = mu_s * N / self.m
        else:
            f = mu_k * N / self.m


        a = F / self.m
        self.v += a * dt

        if (self.v < 0 and f < 0) or (self.v > 0 and f > 0):
            f *= -1

        if (self.v == 0):
            f = 0

        self.v += f * dt
        self.x += self.v * dt

def pprint(num):
    if num > 0:
        print("  " + str(num), end="")

    else:
        print(" " + str(num), end="")

box = Body(0, 20, 0)
scale = 3

# pid vars
integral = 0
error = 0
previous_error = None
setpoint = 500/3

#Kp = .95
Kp = 20
Ki = .005
Kd = 30

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    # PID controller
    error = setpoint - box.x
    integral += error * dt

    if previous_error == None:
        previous_error = error

    derivative = (error - previous_error) / dt

    output = Kp * error + Ki * integral + Kd * derivative
    previous_error = error

    pprint(round(Kp * error, 2))
    pprint(round(Ki * integral, 2))
    pprint(round(Kd * derivative, 2))
    pprint(round(output, 2))
    print()


    # update loop
    box.update(output)

    box_width = box.m * scale
    left = box.x * scale - box_width / 2
    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(left, height-box.m * scale, box_width, box.m * scale))
    pygame.draw.line(screen, (255, 0, 0), (setpoint * scale, height), (setpoint * scale, height * .75))

    # Flip the display    
    pygame.display.flip()
    #clock.tick(120)

pygame.quit()