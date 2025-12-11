import pygame
import random
from src.config import *

class Bird:
    IMG = None
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tick_count = 0
        self.tilt = 0
        self.height = self.y
        self.rect = pygame.Rect(x, y, 34, 24)
        self.alive = True
        self.brain = None
        self.fitness = 0
        if Bird.IMG:
            self.rect = pygame.Rect(x, y, 34, 24)
        
    def jump(self):
        self.vel = FORC_PULO
        self.tick_count = 0
        self.height = self.y
        
    def move(self):
        self.tick_count += 1
        self.vel += GRAVIDADE
        if self.vel > 10:
            self.vel = 10    
        self.y += self.vel

        if self.vel < 0 or self.y < (self.height + 50):
            if self.tilt < 25:
                self.tilt = 25
        else:
            if self.tilt > -90:
                self.tilt -= 3
                
        self.rect.y = int(self.y)
        
        if self.y > ALTURA_TELA - 20 or self.y < 0:
            self.alive = False
            
    def draw(self, win):
        if Bird.IMG:
            rotated_image = pygame.transform.rotate(Bird.IMG, self.tilt)
            new_rect = rotated_image.get_rect(center=self.rect.center)
            win.blit(rotated_image, new_rect.topleft)
        else:
            pygame.draw.rect(win, (255, 0, 0), self.rect)
        
class Pipe:
    IMG_TOP = None
    IMG_BOTTOM = None

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.passed = False
        self.set_height()
        
    def set_height(self):
        self.height = random.randrange(50, ALTURA_TELA - DIST_CANOS - 50)
        self.top = self.height - DIST_CANOS
        self.bottom = self.height
        
        self.top_rect = pygame.Rect(self.x, 0, 70, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + DIST_CANOS, 70, ALTURA_TELA)
        
    def move(self, vel):
        self.x -= vel
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
        
    def collide(self, bird):
        bird_hitbox = bird.rect.inflate(-14, -10)
        
        if bird_hitbox.colliderect(self.top_rect) or bird_hitbox.colliderect(self.bottom_rect):
            return True
            
        return False
    
    def draw(self, win):
        if Pipe.IMG_TOP and Pipe.IMG_BOTTOM:
            win.blit(Pipe.IMG_TOP, (self.x, self.height - Pipe.IMG_TOP.get_height()))

            win.blit(Pipe.IMG_BOTTOM, (self.x, self.height + DIST_CANOS))
        else:
            pygame.draw.rect(win, (0, 200, 0), self.top_rect)
            pygame.draw.rect(win, (0, 200, 0), self.bottom_rect)
            pygame.draw.rect(win, (0, 70, 0), self.top_rect, 3)
            pygame.draw.rect(win, (0, 70, 0), self.bottom_rect, 3)
