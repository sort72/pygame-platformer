import pygame, sys
from pygame.locals import *
from random import randint
from Entity import Entity
from Player import Player

import data

pygame.init()
pygame.font.init()
click = pygame.time.Clock()
screen = pygame.display.set_mode((data.WIDTH,data.HEIGHT))

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
spikes = pygame.sprite.Group()
players = pygame.sprite.Group()
coins = pygame.sprite.Group()
wraiths = pygame.sprite.Group()

def Game():
    global platforms, players, coins, spikes, wraiths, all_sprites

    pygame.display.set_caption("Platformer v0.1")
    pygame.mixer.music.load("assets/sounds/frigost-cuna-de-alma.mp3")
    pygame.mixer.music.play(-1)
    player = Player()
    players.add(player)
    all_sprites.add(player)
    bg = pygame.image.load("assets/sprites/bg-" + str(player.level) + ".jpg")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # We add all elements in this state in order to restart the game easier
        if data.SCREEN == 0:
            # Restart sprite groups
            coins = pygame.sprite.Group()
            platforms = pygame.sprite.Group()
            spikes = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            data.bg_coords = [0, 0]
            bg = pygame.image.load("assets/sprites/bg-" + str(player.level) + ".jpg")

            if player.level == 1:

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
                wraiths.add(wraith)
                spikes.add(wraith)
                all_sprites.add(wraith)
                player.time = 1800
            else:
                platforms_coords = [
                    (400, 580),
                    (700, 580),
                    (900, 500),
                    (1100, 400),
                    (780, 300),
                    (1050, 180),
                    (1400, 200),
                ]
                for i in range(0, 7):
                    platform = Entity('Platform', platforms_coords[i][0], platforms_coords[i][1])
                    platforms.add(platform)
                    all_sprites.add(platform)

                spikes_coords = [
                    (600, 670),
                    (700, 670),
                    (800, 670),
                    (900, 670),
                    (1100, 670),
                    (1200, 670),
                    (1500, 670),
                    (1900, 670),
                    (1600, 670)
                ]
                for i in range(0, 9):
                    spike = Entity('Spikes2', spikes_coords[i][0], spikes_coords[i][1])
                    spikes.add(spike)
                    all_sprites.add(spike)

                platform = Entity('Platform2', 1750, 660)
                platforms.add(platform)
                all_sprites.add(platform)

                coins_coords = [
                    (700, 250),
                    (1030, 350),
                    (1200, 130),
                    (1680, 400),
                    (1680, 450)
                ]
                for i in range(0, 5):
                    coin = Entity('Coin', coins_coords[i][0], coins_coords[i][1])
                    coins.add(coin)
                    all_sprites.add(coin)

                wraiths_coords = [
                    (500, 200),
                    (1200, 400),
                    (1300, 600),
                ]

                for i in range(0, 3):
                    wraith = Entity('Wraith', wraiths_coords[i][0], wraiths_coords[i][1])
                    spikes.add(wraith)
                    wraiths.add(wraith)
                    all_sprites.add(wraith)

                player.time = 3600

            player.score = player.score_1
            player.rect.centerx = 80
            player.rect.centery = 500
            player.dead = False
            player.current_sprite = 0
            player.posX = 0
            data.SCREEN = 2
            all_sprites.add(player)

        # Main menu
        elif data.SCREEN == 1:
            bg = pygame.image.load("assets/sprites/bg-start.jpg")
            font3 = pygame.font.SysFont('Courier', 18)
            screen.blit(bg, (-300,0))

        # The game itself
        elif data.SCREEN == 2:
            platforms_collider = pygame.sprite.groupcollide(players, platforms, False, False)
            for playerC, platformC in platforms_collider.items():
                # Detect if player is in final platform
                if platformC[0].type == 'Platform2':
                    if player.level == 1:
                        player.level = 2
                        player.score_1 = player.score
                        data.SCREEN = 0
                    else:
                        data.SCREEN = 5
                # platformC[0] is the first sprite player is colliding with
                # If player is colliding with a platform's top surface, avoid its descending
                if platformC[0].rect.top < playerC.rect.bottom - 20 and platformC[0].rect.top > playerC.rect.bottom - 30:
                    if playerC.is_descending == True:
                        playerC.is_descending = False
                        playerC.time_descending = 0.0
                    break
                
            else:
                if player.rect.bottom < data.HEIGHT and not player.is_jumping:
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
            if player.rect.right == data.WIDTH and player.posX < data.MAX_X and key[K_d]:
                player.posX += 640
                for element in all_sprites:
                    element.rect.x -= 640
                data.bg_coords[0] -= 640
            elif player.rect.left == 0 and player.posX > 1 and key[K_a]:
                player.posX -= 640
                for element in all_sprites:
                    element.rect.x += 640
                data.bg_coords[0] += 640

            for coin in coins:
                coin.calculate_sprite()

            for wraith in wraiths:
                wraith.calculate_sprite()
                if wraith.is_descending == False:
                    wraith.rect.y -= 3
                    if wraith.rect.top < 100:
                        wraith.is_descending = True
                else:
                    wraith.rect.y += 3
                    if wraith.rect.bottom > data.HEIGHT - 100:
                        wraith.is_descending = False
                
            player.time -= 1
            if player.time < 0:
                data.SCREEN = 4

        # Game Over
        elif data.SCREEN == 3:
            font2 = pygame.font.SysFont('IMPACT', 50)
            bg = pygame.image.load("assets/sprites/bg-gameover.jpg")
            screen.blit(bg, (-300,0))
            intro_text = font2.render(f'{player.score}', False, (255, 255, 255))
            screen.blit(intro_text,(650,320))

        # Time Out
        elif data.SCREEN == 4:
            font2 = pygame.font.SysFont('IMPACT', 50)
            bg = pygame.image.load("assets/sprites/bg-timeout.jpg")
            screen.blit(bg, (-300,0))
            intro_text = font2.render(f'{player.score}', False, (255, 255, 255))
            screen.blit(intro_text,(650,320))

        # End game
        elif data.SCREEN == 5:
            font2 = pygame.font.SysFont('IMPACT', 50)
            bg = pygame.image.load("assets/sprites/bg-won.jpg")
            screen.blit(bg, (-300,0))
            intro_text = font2.render(f'{player.score}', False, (255, 255, 255))
            screen.blit(intro_text,(650,300))
            intro_text = font2.render(f'{int(player.time/60)}', False, (255, 255, 255))
            screen.blit(intro_text,(640,450))

        pygame.display.flip()
        click.tick(120)
        all_sprites.update()
        
        screen.blit(bg, (data.bg_coords[0], data.bg_coords[1]))

        all_sprites.draw(screen)
        
        intro_text = font3.render(f'Nivel: {player.level} | Monedas: {player.score} | Tiempo restante: {int(player.time / 60)}', False, (255, 255, 255))
        screen.blit(intro_text,(400,10))
