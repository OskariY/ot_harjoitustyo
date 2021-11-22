import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))

from settings import *
from functions import *
from entities import *
from resources import *

def main():

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
        scrollx += round((player.rect.centerx-scrollx-W//2) / 20)
        scrolly += round((player.rect.centery-scrolly-H//2) / 20)

        # clear lists affected by the world generation loop
        tiles = []
        buildables = []
        glows = []
        slabs = []
        entities = []


        # world generation
        for x in range(6):
            for y in range(5):
                # define the target chunk and check if it exists in the game map
                # if so get it else generate it
                target_x = x - 1 + int(round(scrollx/(CHUNK_SIZE*TILE_SIZE)))
                target_y = y - 1 + int(round(scrolly/(CHUNK_SIZE*TILE_SIZE)))
                target_chunk = str(target_x) + ';' + str(target_y)
                if target_chunk not in game_map:
                    if singleplayer:
                        game_map[target_chunk] = generate_chunk(target_x, target_y, seed)
                    else:
                        game_map[target_chunk] = send_data("get_chunk", (target_x, target_y), network)

                if MOB_SPAWNS == True:
                    # in the future mobs will be spawned here
                    pass
                for tile in game_map[target_chunk][0]:
                    if tile[1] == "torch":
                        glows.append((tile[0][0]*TILE_SIZE-scrollx-glowradius+TILE_SIZE//2,tile[0][1]*TILE_SIZE-scrolly-glowradius+TILE_SIZE//2))

                    if tile[1] == "slab":
                        slabs.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

                    if tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                        # drawing trees
                        display.blit(items[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx-tree_image.get_width() // 2 + 8,tile[0][1]*TILE_SIZE-scrolly-tree_image.get_height()+TILE_SIZE))
                    else:
                        # drawing everything else
                        display.blit(items[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx,tile[0][1]*TILE_SIZE-scrolly))
                    if mob_spawns:
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


if __name__ == "__main__":
    main()
