import pygame, sys
from pygame.locals import *
from random import randint

WIDTH = 1280
HEIGHT= 720

MAX_X = 640   

SCREEN = 1

MAX_SCORE = 4
LIMIT_JUMPED = 150.0

bg_coords = [0, 0]

player_sprite_multiplier = 5
entity_sprite_multiplier = 6

pygame.init()
pygame.font.init()
click = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH,HEIGHT))

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
        self.posX = 0
        self.current_sprite = 0
        self.old_status = 0
        self.walking_left = False
        self.dead = False
        self.time = 0
        self.sprites_limit = [17 * player_sprite_multiplier, 11 * player_sprite_multiplier, 11 * player_sprite_multiplier, 9 * player_sprite_multiplier, 5 * player_sprite_multiplier, 14 * player_sprite_multiplier] # We multiply by 8 to make sprite changing better, n/8 is amount of sprites used

    def calculate_sprite(self, status):
        if self.dead == False:
            if self.old_status != status:
                self.old_status = status
                self.current_sprite = 0

            if self.current_sprite % player_sprite_multiplier == 0:
                if status == 0:
                    self.image = pygame.image.load("assets/sprites/Player/Idle/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 1:
                    self.image = pygame.image.load("assets/sprites/Player/Running/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
                elif status == 2:
                    self.image = pygame.image.load("assets/sprites/Player/Running/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 3:
                    self.image = pygame.image.load("assets/sprites/Player/Jumping/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                elif status == 4:
                    self.image = pygame.image.load("assets/sprites/Player/FallingDown/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
                    self.image = pygame.transform.flip(self.image, self.walking_left, False)
                

            self.current_sprite += 1
            if self.current_sprite == self.sprites_limit[status]:
                self.current_sprite = 0

    def die(self):
        global SCREEN

        if self.current_sprite % player_sprite_multiplier == 0:
            self.image = pygame.image.load("assets/sprites/Player/Dying/" + str(int(self.current_sprite / player_sprite_multiplier)) + ".png")
            self.image = pygame.transform.flip(self.image, self.walking_left, False)
        
        if self.current_sprite == self.sprites_limit[5]:
            SCREEN = 3
        else:
            self.current_sprite += 1

    def update(self):
        global SCREEN
        keys = pygame.key.get_pressed()

        if keys[K_SPACE]:
            if SCREEN == 1 or SCREEN == 3:
                SCREEN = 0
            else:
                if self.is_jumping == False and self.is_descending == False and self.dead == False:
                    self.is_jumping = True

        if SCREEN == 2:
            if keys[K_d] and self.dead == False:
                self.rect.x += int(self.vel)
                if self.rect.right > WIDTH:
                    self.rect.right = WIDTH

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

                if self.distance_jumped > LIMIT_JUMPED or self.rect.top < 0:
                    self.is_jumping = False
                    self.is_descending = True
                    self.distance_jumped = 0.0
                    if self.rect.top < 0:
                        self.rect.top = 0

                self.calculate_sprite(3)

            if self.is_descending == True:
                self.rect.y += int(self.vel + self.time_descending)
                self.time_descending += 0.05

                if self.rect.bottom > HEIGHT:
                    self.rect.bottom = HEIGHT
                    self.time_descending = 0.0
                    self.is_descending = False

                self.calculate_sprite(4)

            # Idle animation
            if self.is_descending == False and self.is_jumping == False and keys[K_a] == False and keys[K_d] == False:
                self.calculate_sprite(0)

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

        if self.current_sprite % entity_sprite_multiplier == 0:
            if self.type == 'Coin':
                self.image = pygame.image.load("assets/sprites/Coins/" + str(int(self.current_sprite / entity_sprite_multiplier)) + ".png")  
            elif self.type == 'Wraith':    
                self.image = pygame.image.load("assets/sprites/Wraith/Taunt/" + str(int(self.current_sprite / entity_sprite_multiplier)) + ".png")  
                self.image = pygame.transform.flip(self.image, True, False)    

        self.current_sprite += 1
        if self.current_sprite == self.sprites_limit * entity_sprite_multiplier:
            self.current_sprite = 0

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()
players = pygame.sprite.Group()
coins = pygame.sprite.Group()

def Game():
    global platforms, players, coins, spikes, all_sprites, SCREEN, bg_coords

    pygame.display.set_caption("Platformer v0.1")
    pygame.mixer.music.load("assets/sounds/frigost-cuna-de-alma.mp3")
    pygame.mixer.music.play(-1)
    bg = pygame.image.load("assets/sprites/bg-1.jpg")
    player = Player()
    players.add(player)
    all_sprites.add(player)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # We add all elements in this state in order to restart the game easier
        if SCREEN == 0:
            # Restart sprite groups
            coins = pygame.sprite.Group()
            platforms = pygame.sprite.Group()
            spikes = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            bg_coords = [0, 0]

            platforms_coords = [
                (350, 600),
                (600, 500),
                (370, 370),
                (600, 250),
                (1020, 200),
                (1250, 600),
                (1400, 500),
                (1650, 400)
            ]
            for i in range(0, 8):
                platform = Entity('Platform', platforms_coords[i][0], platforms_coords[i][1])
                platforms.add(platform)
                all_sprites.add(platform)

            spikes_coords = [
                (1000, 555),
                (700, 670),
                (800, 670),
                (900, 670),
                (1100, 670),
                (1200, 670),
                (1500, 670),
                (1650, 670),
                (1750, 670)
            ]
            for i in range(0, 9):
                sp = 'Spikes'
                if i >= 6: 
                    sp = 'Spikes2'
                spike = Entity(sp, spikes_coords[i][0], spikes_coords[i][1])
                spikes.add(spike)
                all_sprites.add(spike)

            platform = Entity('Platform2', 1920, 660)
            platforms.add(platform)
            all_sprites.add(platform)

            coins_coords = [
                (540, 200),
                (1000, 420),
                (1600, 350),
                (1900, 300),
                (1900, 350),
                (1900, 400),
                (1900, 450),
                (1900, 500),
                (1900, 550),
                (1850, 300),
                (1850, 350),
                (1850, 400),
                (1850, 450),
                (1850, 500),
                (1850, 550),
            ]
            for i in range(0, 15):
                coin = Entity('Coin', coins_coords[i][0], coins_coords[i][1])
                coins.add(coin)
                all_sprites.add(coin)

            wraith = Entity('Wraith', 1500, 300)
            spikes.add(wraith)
            all_sprites.add(wraith)

            player.score = 0
            player.rect.centerx = 80
            player.rect.centery = 500
            player.dead = False
            player.current_sprite = 0
            player.time = 6000
            player.posX = 0
            SCREEN = 2
            all_sprites.add(player)

        # Main menu
        elif SCREEN == 1:
            intro = pygame.font.SysFont('Comic Sans MS', 60)
            font2 = pygame.font.SysFont('Courier', 25)
            font3 = pygame.font.SysFont('Courier', 18)
            screen.blit(bg, (0,0))
            intro_text = intro.render('Platformer v0.1', False, (220, 178, 234))
            screen.blit(intro_text,(283,100))
            intro_text = font2.render('Utiliza las teclas izquierda y derecha para moverte', False, (255, 255, 255))
            screen.blit(intro_text,(100,250))
            intro_text = font2.render('y la barra ESPACIADORA para saltar.', False, (255, 255, 255))
            screen.blit(intro_text,(100,280))
            intro_text = font2.render('___________________________________________________', False, (255, 255, 255))
            screen.blit(intro_text,(100,310))
            intro_text = font2.render('Debes recoger todos los hongos para ganar.', False, (255, 255, 255))
            screen.blit(intro_text,(100,350))
            intro_text = font2.render('¡Ten cuidado con los pinchos!', False, (255, 255, 255))
            screen.blit(intro_text,(100,380))
            intro_text = font2.render('Presiona ESPACIO para jugar.', False, (255, 255, 255))
            screen.blit(intro_text,(290,500))

            intro_text = font3.render('Desarrollado por Sergio Alejandro Ortega y Jeferson David Meneses.', False, (255, 255, 255))
            screen.blit(intro_text,(5,605))

        # The game itself
        elif SCREEN == 2:
            platforms_collider = pygame.sprite.groupcollide(players, platforms, False, False)
            for playerC, platformC in platforms_collider.items():
                # Detect if player is in final platform
                if platformC[0].type == 'Platform2':
                    SCREEN = 4
                # platformC[0] is the first sprite player is colliding with
                # If player is colliding with a platform's top surface, avoid its descending
                if platformC[0].rect.top < playerC.rect.bottom - 20 and platformC[0].rect.top > playerC.rect.bottom - 30:
                    if playerC.is_descending == True:
                        playerC.is_descending = False
                        playerC.time_descending = 0.0
                    break
                
            else:
                if player.rect.bottom < HEIGHT and not player.is_jumping:
                    player.is_descending = True

            spikes_collider = pygame.sprite.groupcollide(players, spikes, False, False)
            for playerC, spikeC in spikes_collider.items():
                if playerC.dead == False:
                    playerC.current_sprite = 0
                    playerC.dead = True
                playerC.die()

            coins_collider = pygame.sprite.groupcollide(players, coins, False, False)
            for playerC, powerC in coins_collider.items():
                powerC[0].kill()
                playerC.score += 1

            key = pygame.key.get_pressed()
            if player.rect.right == WIDTH and player.posX < MAX_X and key[K_d]:
                player.posX += 640
                for element in all_sprites:
                    element.rect.x -= 640
                bg_coords[0] -= 640
            elif player.rect.left == 0 and player.posX > 1 and key[K_a]:
                player.posX -= 640
                for element in all_sprites:
                    element.rect.x += 640
                bg_coords[0] += 640

            for coin in coins:
                coin.calculate_sprite()

            wraith.calculate_sprite()
            if wraith.is_descending == False:
                wraith.rect.y -= 3
                if wraith.rect.top < 100:
                    wraith.is_descending = True
            else:
                wraith.rect.y += 3
                if wraith.rect.bottom > HEIGHT - 100:
                    wraith.is_descending = False
                
            player.time -= 1

        # Game Over
        elif SCREEN == 3:
            intro = pygame.font.SysFont('Comic Sans MS', 60)
            font2 = pygame.font.SysFont('Courier', 25)
            font3 = pygame.font.SysFont('Courier', 18)
            screen.blit(bg, (0,0))
            intro_text = intro.render('GAME OVER', False, (220, 178, 234))
            screen.blit(intro_text,(322,100))
            intro_text = font2.render(f'Recolectaste {player.score} hongos', False, (255, 255, 255))
            screen.blit(intro_text,(335,250))
            intro_text = font2.render('Presiona ESPACIO para reintentar.', False, (255, 255, 255))
            screen.blit(intro_text,(250,500))

            intro_text = font3.render('Desarrollado por Sergio Alejandro Ortega y Jeferson David Meneses.', False, (255, 255, 255))
            screen.blit(intro_text,(5,605))

        # End game
        elif SCREEN == 4:
            intro = pygame.font.SysFont('Comic Sans MS', 60)
            font2 = pygame.font.SysFont('Courier', 25)
            font3 = pygame.font.SysFont('Courier', 18)
            screen.blit(bg, (0,0))
            intro_text = intro.render('¡GANASTE!', False, (220, 178, 234))
            screen.blit(intro_text,(340,100))
            intro_text = font2.render(f'¡Recolectaste todos los hongos!', False, (255, 255, 255))
            screen.blit(intro_text,(265,250))
            intro_text = font2.render('Gracias por jugar.', False, (255, 255, 255))
            screen.blit(intro_text,(367,400))

        pygame.display.flip()
        click.tick(120)
        all_sprites.update()
        screen.blit(bg, (bg_coords[0], bg_coords[1]))
        all_sprites.draw(screen)


        intro_text = font3.render(f'Monedas: {player.score} | Tiempo restante: {int(player.time / 60)}', False, (255, 255, 255))
        screen.blit(intro_text,(500,10))

Game()