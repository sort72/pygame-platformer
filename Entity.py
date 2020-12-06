import pygame
import data

# Entities different to Player
class Entity(pygame.sprite.Sprite):
    def __init__(self, type, posX, posY):
        
        self.sprites_limit = 0

        if type == 'Spikes':
            img = "assets/sprites/spikes.png"
        elif type == 'Spikes2':
            img = "assets/sprites/spikes-2.png"
        elif type == 'Platform':
            img = "assets/sprites/platform-1.png"
        elif type == 'Platform2':
            img = "assets/sprites/platform-2.png"
        elif type == 'Coin':
            img = "assets/sprites/Coins/0.png"
            self.sprites_limit = 9
        elif type == 'Wraith':
            img = "assets/sprites/Wraith/Taunt/0.png"
            self.sprites_limit = 17
            self.is_descending = False

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.x = posX
        self.y = posY
        self.rect.top = self.y
        self.rect.right = self.x
        self.current_sprite = 0
        self.type = type

    def calculate_sprite(self):

        if self.current_sprite % data.entity_sprite_multiplier == 0:
            if self.type == 'Coin':
                self.image = pygame.image.load("assets/sprites/Coins/" + str(int(self.current_sprite / data.entity_sprite_multiplier)) + ".png")  
            elif self.type == 'Wraith':    
                self.image = pygame.image.load("assets/sprites/Wraith/Taunt/" + str(int(self.current_sprite / data.entity_sprite_multiplier)) + ".png")  
                self.image = pygame.transform.flip(self.image, True, False)    

        self.current_sprite += 1
        if self.current_sprite == self.sprites_limit * data.entity_sprite_multiplier:
            self.current_sprite = 0