"""
This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import pygame
import sys

from settings import *
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: anti-spaghetti version")
from resources import *
from functions import *
from entities import *


def main():
    # pygame clock
    clock = pygame.time.Clock()

    # object lists for updating and drawing
    mobs = []
    worms = []
    entities = []
    particles = []
    popups = []
    drops = []

    # inventory related variables
    equipped = ""

    # world variables
    game_map = {}
    spawn_x = -100
    spawn_y = 0
    seed = random.randint(-999999, 999999)
    current_biome = 1

    # player object and scroll variables
    player = Player(spawn_x, spawn_y)
    scrollx = 0
    scrolly = 0

    # game loop
    while True:
        # get mouse position and divide it to get
        # true position since the game surface is stretched to the screen
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex/(WINDOW_WIDTH/DISPLAY_WIDTH)
        mousey = mousey/(WINDOW_HEIGHT/DISPLAY_HEIGHT)
        mousepos = (mousex, mousey)

        # smoothly scroll "camera" towards the player
        scrollx += round((player.rect.centerx-scrollx-DISPLAY_WIDTH//2) / 20)
        scrolly += round((player.rect.centery-scrolly-DISPLAY_HEIGHT//2) / 20)

        # clear lists affected by the world generation loop
        tiles = []
        buildables = []
        glows = []
        slabs = []
        entities = []

        # draw background image
        display.blit(background_image, (0, 0))


        # world generation
        for x in range(6):
            for y in range(5):
                # define the target chunk and check if it exists in the game map
                # if so get it else generate it
                target_x = x - 1 + int(round(scrollx/(CHUNK_SIZE*TILE_SIZE)))
                target_y = y - 1 + int(round(scrolly/(CHUNK_SIZE*TILE_SIZE)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in game_map:
                    game_map[target_chunk] = generate_chunk(target_x, target_y, seed)

                for tile in game_map[target_chunk][0]:
                    if tile[1] == "torch":
                        glows.append((tile[0][0]*TILE_SIZE-scrollx-glowradius+TILE_SIZE//2,tile[0][1]*TILE_SIZE-scrolly-glowradius+TILE_SIZE//2))

                    if tile[1] == "slab":
                        slabs.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

                    if tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                        # drawing trees
                        display.blit(ITEMS[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx-tree_image.get_width() // 2 + 8,tile[0][1]*TILE_SIZE-scrolly-tree_image.get_height()+TILE_SIZE))
                    else:
                        # drawing everything else
                        display.blit(ITEMS[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx,tile[0][1]*TILE_SIZE-scrolly))

                    # mob spawns, when I get around to adding the mob classes
                    if MOB_SPAWNS:
                        if tile[1] == "snowy grass":
                            if random.randint(1, 30000) == 1:
                                if tile[0][0]*TILE_SIZE < player.rect.x - 100 or tile[0][0]*TILE_SIZE > player.rect.x + 100:
                                    print("bear spawned, mobs: {}".format(len(mobs)))
                                    mobs.append(WalkingMob(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE-48, 1))
                        if is_night == True:
                            if tile[1] in ["snowy grass", "grass"]:
                                if random.randint(1, 10000) == 1:
                                    if tile[0][0]*TILE_SIZE < player.rect.x - 100 or tile[0][0]*TILE_SIZE > player.rect.x + 100:
                                        print("skeleton spawned, mobs: {}".format(len(mobs)))
                                        mobs.append(WalkingMob(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE-48, 2))

                    # physics
                    if tile[1] in ["stone","dirt","grass","snowy grass","plank","rock","coal block","slab"]:
                        tiles.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

                    if tile[1] in ["oak sapling"]:
                        sapling_exists = False
                        for sapling in saplings:
                            if sapling[0] == [tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE]:
                                sapling_exists = True
                        if not sapling_exists:
                            saplings.append([[tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE], 1000])

                    buildables.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                if event.key == pygame.K_d: # move right
                    player.moving_right = True
                    player.invert = 0
                if event.key == pygame.K_a: # move left
                    player.moving_left = True
                    player.invert = 1
                if event.key == pygame.K_s:
                    player.falling = True
                if event.key == pygame.K_w and player.jumps > 0: # jump
                    player.dy = -player.jump_power
                    player.jumps -= 1
                    jump_sound.play()
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        player.moving_right = False
                    if event.key == pygame.K_a:
                        player.moving_left = False


        # drawing and updating game entities like the player
        player.draw(display, scrollx, scrolly)
        player.update(scrollx, scrolly, tiles, mobs, drops, popups, slabs)

        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    main()
