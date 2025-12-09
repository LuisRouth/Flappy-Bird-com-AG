import pygame
import random
from src.config import *

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.rect = pygame.Rect(x, y, 34, 24)
        self.alive = True
        self.brain = None
        self.fitness = 0
        
    def jump(self):
        self.vel = FORC_PULO
        self.tick_count = 0
        
    def move(self):
        self.tick_count += 1
        displacement = self.vel * self.tick_count + GRAVIDADE * (self.tick_count ** 2)
        
        if displacement >= 16:
            displacement = 16
            
        self.y += displacement
        self.rect.y = int(self.y)
        
        if self.y > ALTURA_TELA - 50 or self.y < 0:
            self.alive = False
            
    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.rect)