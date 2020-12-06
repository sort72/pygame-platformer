import pygame
from pygame.locals import *
import data

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/sprites/Player/Running/0.png")
        self.rect = pygame.Rect(self.image.get_rect().left + 20  , self.image.get_rect().top, self.image.get_rect().width - 40 , self.image.get_rect().height)
        self.vel = 3
        self.is_jumping = False
        self.is_descending = False
        self.distance_jumped = 0.0
        self.time_descending = 0.0
        self.score = 0
        self.score_1 = 0
        self.posX = 0
        self.current_sprite = 0
        self.old_status = 0
        self.walking_left = False
        self.dead = False
        self.time = 0
        self.level = 1
        self.sprites_limit = [17 * data.player_sprite_multiplier, 11 * data.player_sprite_multiplier, 11 * data.player_sprite_multiplier, 9 * data.player_sprite_multiplier, 5 * data.player_sprite_multiplier, 14 * data.player_sprite_multiplier] # We multiply by 8 to make sprite changing better, n/8 is amount of sprites used

    def calculate_sprite(self, status):
        if self.dead == False:
            if self.old_status != status:
                self.old_status = status
                self.current_sprite = 0

            if self.current_sprite % data.player_sprite_multiplier == 0:
                if status == 0:
                    self.image = pygame.image.load("assets/sprites/Player/Idle/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 1:
                    self.image = pygame.image.load("assets/sprites/Player/Running/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
                elif status == 2:
                    self.image = pygame.image.load("assets/sprites/Player/Running/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 3:
                    self.image = pygame.image.load("assets/sprites/Player/Jumping/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 4:
                    self.image = pygame.image.load("assets/sprites/Player/FallingDown/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                

            self.current_sprite += 1
            if self.current_sprite == self.sprites_limit[status]:
                self.current_sprite = 0

    def die(self):

        if self.current_sprite % data.player_sprite_multiplier == 0:
            self.image = pygame.image.load("assets/sprites/Player/Dying/" + str(int(self.current_sprite / data.player_sprite_multiplier)) + ".png")
            self.image = pygame.transform.flip(self.image, self.walking_left, False)
        
        if self.current_sprite == self.sprites_limit[5]:
            data.SCREEN = 3
        else:
            self.current_sprite += 1

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            if data.SCREEN == 1 or data.SCREEN == 3:
                data.SCREEN = 0
            else:
                if self.is_jumping == False and self.is_descending == False and self.dead == False:
                    self.is_jumping = True

        if data.SCREEN == 2:
            if keys[K_d] and self.dead == False:
                self.rect.x += int(self.vel)
                if self.rect.right > data.WIDTH:
                    self.rect.right = data.WIDTH

                self.walking_left = False
                self.calculate_sprite(1)

            if keys[K_a] and self.dead == False:
                self.rect.x -= int(self.vel)
                if self.rect.left < 0:
                    self.rect.left = 0

                self.walking_left = True
                self.calculate_sprite(2)

            if self.is_jumping == True:
                distance_jump = self.vel * 1.1
                self.distance_jumped += distance_jump
                self.rect.y -= int(distance_jump)

                if self.distance_jumped > data.LIMIT_JUMPED or self.rect.top < 0:
                    self.is_jumping = False
                    self.is_descending = True
                    self.distance_jumped = 0.0
                    if self.rect.top < 0:
                        self.rect.top = 0

                self.calculate_sprite(3)

            if self.is_descending == True:
                self.rect.y += int(self.vel + self.time_descending)
                self.time_descending += 0.05

                if self.rect.bottom > data.HEIGHT:
                    self.rect.bottom = data.HEIGHT
                    self.time_descending = 0.0
                    self.is_descending = False

                self.calculate_sprite(4)

            # Idle animation
            if self.is_descending == False and self.is_jumping == False and keys[K_a] == False and keys[K_d] == False:
                self.calculate_sprite(0)

