"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
import time
import constants
import random
#from pygame.locals import *

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
explosion_fx = pygame.mixer.Sound("sounds/explosion.wav")
explosion_fx.set_volume(0.05)


class Enemy(pygame.sprite.Sprite):

    # -- Attributes
    last_shot = pygame.time.get_ticks()
    # Set speed vector of player
    change_x = 0
    change_y = 0
    # List of sprites we can bump against
    level = None
    move_direction = 1
    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.images = []
        self.images.append(pygame.image.load('img/monokuma1.png'))
        self.images.append(pygame.image.load('img/monokuma2.png'))

        # Set the image for the enemy
        self.image = self.images[0]
        self.frame = 0
        self.last_update = pygame.time.get_ticks() ## time when the animation has to happen

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        #animate
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds to decide animation speed
            self.last_update = time_now
            if self.frame == 0:
                self.frame = 1
            else:
                self.frame = 0

        self.image = self.images[self.frame]

        self.rect.y +=1 * self.move_direction

        if self.rect.y == constants.SCREEN_HEIGHT-80:
            self.move_direction = -1

        if self.rect.y ==0:
            self.move_direction = 1

        #print(str(self.rect.y))

class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, pos, player):
        pygame.sprite.Sprite.__init__(self)
        
        self.images = []
        #self.images.append(pygame.image.load('img/bullet.png'))

        self.images.append(pygame.image.load('img/hammer1.png'))
        self.images.append(pygame.image.load('img/hammer2.png'))
        self.images.append(pygame.image.load('img/hammer3.png'))
        self.images.append(pygame.image.load('img/hammer4.png'))

        # Set the for the enemy
        self.image = self.images[0]
        self.frame = 0

        self.last_update = pygame.time.get_ticks() ## time when the animation has to happen

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(pos)

        last_shot = pygame.time.get_ticks()
        #self.direction = direction
        self.player = player

    def update(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # in milliseconds to decide animation speed
            self.last_update = time_now
            if self.frame >= 0 and self.frame<3:
                self.frame += 1
            else:
                self.frame = 0

        self.image = self.images[self.frame]
        self.rect = self.rect.move(-5,0)

        if self.rect.x<0:
            #print("KILL")
            self.kill()

#create Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 5):
            img = pygame.image.load(f"img/exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            #add the image to the list
            self.images.append(img)
            #print(str(img))
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_fx.play()
        explosion_speed = 3
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()