import pygame
import numpy as np
import random

pygame.init()

width, height = 1000, 1000
# Set up the drawing window
screen = pygame.display.set_mode([width, height])


# constants
dt = .1
g = 9.81
mu_k = 0.04
mu_s = 0.05

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

        else:
            f = 0


        self.v += f * dt
        self.x += self.v * dt


box = Body(0, 20, 0)

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    box.update()
    scale = 3
    pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(box.x * scale, height-box.m * scale, box.m * scale, box.m * scale))

    # Flip the display    
    pygame.display.flip()
    clock.tick(120)

pygame.quit()