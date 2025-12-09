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
        
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - DIST_CANOS
        self.bottom = self.height
        
        self.top_rect = pygame.Rect(self.x, 0, 70, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + DIST_CANOS, 70, ALTURA_TELA)
        
    def move(self):
        self.x -= VEL_CANOS
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def collide(self, bird):
        if bird.rect.colliderect(self.top_rect) or bird.rect.colliderect(self.bottom_rect):
            return True
        return False
    
    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), self.top_rect)
        pygame.draw.rect(win, (0, 255, 0), self.bottom_rect)