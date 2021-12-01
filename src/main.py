"""
Northlands: unspaghettified

This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import pygame
import sys
import random

# import constants/settings
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, CENTER, WHITE, FPS, CHUNK_SIZE, TILE_SIZE, GRAY, BLACK, BROWN, GRASSGREEN
# intialize pygame and set up display
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: unspaghettified")
# import functions, classes and resources (images, sound etc.) needed
from resources import ITEMS, background_image, tree_image, jump_sound, break_sound
from functions import print_text, generate_chunk, remove_tile, get_tile, place_tile, get_next_tiles, draw_tile_outline
from entities import Player, Particle, FadingText
from inventory import Inventory

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

    # inventory related variables
    inventory = Inventory()
    inv_open = False
    
    # add some basic items to the inventory
    inventory.add_to_inventory("axe", 1)
    inventory.add_to_inventory("pickaxe", 1)
    inventory.add_to_inventory("shovel", 1)
    inventory.add_to_inventory("plank", 100)

    # tile breaking related variables
    selected_tile = None
    tile_hits_left = 10

    # game loop
    while True:
        # get mouse position and divide it to get
        # true position since the game surface is stretched to the screen
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex/(WINDOW_WIDTH/DISPLAY_WIDTH)
        mousey = mousey/(WINDOW_HEIGHT/DISPLAY_HEIGHT)
        mousepos = (mousex, mousey)

        # smoothly scroll camera towards the player
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
                # go through all tiles in the target chunk
                for tile in game_map[target_chunk][0]:
#                    if tile[1] == "torch":
#                        glows.append((tile[0][0]*TILE_SIZE-scrollx-glowradius+TILE_SIZE//2,tile[0][1]*TILE_SIZE-scrolly-glowradius+TILE_SIZE//2))

                    if tile[1] == "slab":
                        slabs.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

                    if tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                        # drawing trees
                        display.blit(ITEMS[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx-tree_image.get_width() // 2 + 8,tile[0][1]*TILE_SIZE-scrolly-tree_image.get_height()+TILE_SIZE))
                    else:
                        # drawing everything else
                        display.blit(ITEMS[tile[1]]["image"],(tile[0][0]*TILE_SIZE-scrollx,tile[0][1]*TILE_SIZE-scrolly))

                    # mob spawns, when I get around to adding the mob classes
                    # BROKEN CODE, FIX!!
#                    if MOB_SPAWNS:
#                        if tile[1] == "snowy grass":
#                            if random.randint(1, 30000) == 1:
#                                if tile[0][0]*TILE_SIZE < player.rect.x - 100 or tile[0][0]*TILE_SIZE > player.rect.x + 100:
#                                    print("bear spawned, mobs: {}".format(len(mobs)))
#                                    mobs.append(WalkingMob(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE-48, 1))
#                        if is_night == True:
#                            if tile[1] in ["snowy grass", "grass"]:
#                                if random.randint(1, 10000) == 1:
#                                    if tile[0][0]*TILE_SIZE < player.rect.x - 100 or tile[0][0]*TILE_SIZE > player.rect.x + 100:
#                                        print("skeleton spawned, mobs: {}".format(len(mobs)))
#                                        mobs.append(WalkingMob(tile[0][0]*TILE_SIZE, tile[0][1]*TILE_SIZE-48, 2))
#
                    # physics
                    if tile[1] in ["stone","dirt","grass","snowy grass","plank","rock","coal block","slab"]:
                        tiles.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

                    buildables.append(pygame.Rect(tile[0][0]*TILE_SIZE,tile[0][1]*TILE_SIZE,TILE_SIZE,TILE_SIZE))

        # event loop
        for event in pygame.event.get():
            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:                
            # movement
                # move right
                if event.key == pygame.K_d:
                    player.moving_right = True
                    player.invert = 0
                # move left
                if event.key == pygame.K_a:
                    player.moving_left = True
                    player.invert = 1
                # fall (used for slabs)
                if event.key == pygame.K_s:
                    player.falling = True
                # jump
                if event.key == pygame.K_w and player.jumps > 0: # jump
                    player.dy = -player.jump_power
                    player.jumps -= 1
                    jump_sound.play()
            # open inventory
                if event.key == pygame.K_TAB:
                    if inv_open == False:
                        inv_open = True
                    else:
                        inv_open = False
                # equip items in the hotbar
                if event.key == pygame.K_1:
                    inventory.equip_item(0)
                if event.key == pygame.K_2:
                    inventory.equip_item(1)
                if event.key == pygame.K_3:
                    inventory.equip_item(2)
                if event.key == pygame.K_4:
                    inventory.equip_item(3)
                if event.key == pygame.K_5:
                    inventory.equip_item(4)
                
            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        player.moving_right = False
                    if event.key == pygame.K_a:
                        player.moving_left = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # inventory mouse controls
                if inv_open:
                    if event.button == 1:
                        # moving items in the inventory
                        for i, item in enumerate(inventory.inventory):
                            testrect = item[0].copy()
                            testrect.x += inventory.invx
                            testrect.y += inventory.invy
                            if testrect.collidepoint(mousepos):
                                if inventory.inventory[i][1] != "":
                                    inventory.inv_select1 = i
                                    break
                # regular mouse countrols
                else:
                    if event.button == 1:
                        if inventory.equipped != "" and inventory.equipped != None:
                            # if item is food, heal player
                            if ITEMS[inventory.equipped]["food"] and player.health < player.max_health:
                                if player.health + ITEMS[inventory.equipped]["heal"] > player.max_health:
                                    player.health = player.max_health
                                else:
                                    player.health += ITEMS[inventory.equipped]["heal"]
                                inventory.remove_item(inventory.equipped, 1)
                                popups.append(FadingText(player.rect.centerx, player.rect.top, "+{} HP".format(str(ITEMS[inventory.equipped]["heal"])), GRASSGREEN))
                            # tool logic
                            if ITEMS[inventory.equipped]["tool"] and inventory.in_inventory(inventory.equipped):
                                #player.hit(inventory.equipped, mobs, worms, mousex, mousey)
                                breaking_tile = get_tile(mousepos, game_map, scrollx, scrolly)
                                if selected_tile != breaking_tile:
                                    selected_tile = breaking_tile
                                    tile_hits_left = 10
                                if breaking_tile != None:
                                    # reduce tile_hits_left based on the tool and the tile
                                    if inventory.equipped == "pickaxe" and breaking_tile[1] in ["stone", "coal block"]:
                                        if breaking_tile[1] == "stone":
                                            tile_hits_left -= 5
                                        if breaking_tile[1] == "coal block":
                                            tile_hits_left -= 2
                                    elif inventory.equipped == "shovel" and breaking_tile[1] in ["dirt", "grass", "snowy grass"]:
                                        tile_hits_left -= 5
                                    elif inventory.equipped == "axe" and breaking_tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                                            tile_hits_left -= 2
                                    elif inventory.equipped == "axe" and breaking_tile[1] in ["plank", "plank wall", "slab"]:
                                        tile_hits_left -= 5
                                    elif breaking_tile[1] in ["plant", "torch"]:
                                        tile_hits_left = 0
                                    elif not breaking_tile[1] in ["stone", "coal block"]:
                                        tile_hits_left -= 1

                                    # play breaking sound
                                    break_sound.play()
                                    # spawn particles
                                    if breaking_tile[1] in ["stone", "rock", "coal block"]:
                                        particle_color = GRAY
                                    elif breaking_tile[1] in ["grass", "plant"]:
                                        particle_color = GRASSGREEN
                                    elif breaking_tile[1] in ["snowy grass"]:
                                        particle_color = WHITE
                                    else:
                                        particle_color = BROWN

                                    for i in range(10):
                                        particles.append(Particle(breaking_tile[0][0]*TILE_SIZE+8, breaking_tile[0][1]*TILE_SIZE+8, particle_color))
                                    #player.chop(items[inventory.equipped]["image"])

                                    if tile_hits_left <= 0:
                                        selected_tile = None
                                        tile_hits_left = 10
                                        remove_tile(mousepos, game_map, particles, drops, tiles, scrollx, scrolly, player)

                    if event.button == 3:
                        if inventory.equipped != "":
                            # place tiles
                            if ITEMS[inventory.equipped]["build"] and inventory.in_inventory(inventory.equipped):
                                if get_next_tiles(mousepos, buildables, scrollx, scrolly) == True:
                                    game_map = place_tile(mousepos, inventory.equipped, inventory.equipped, 
                                                          game_map, inventory, player, 
                                                          scrollx, scrolly)
                            # elif inventory.equipped == "hoe" and get_tile(mousepos)[1] == "dirt":
                            #     remove_tile(mousepos, True)
                            #     place_tile(mousepos, "grass", False)
            if event.type == pygame.MOUSEBUTTONUP:
                # inventory mouse controls
                if inv_open:
                    if event.button == 1:
                       # loop through the inventory grid and test for collisions
                       # if mouse collides with an inventory slot call the inventory drag function
                       for i, item in enumerate(inventory.inventory):
                            testrect = item[0].copy()
                            testrect.x += inventory.invx
                            testrect.y += inventory.invy
                            if testrect.collidepoint(mousepos):
                                inventory.inv_select2 = i
                                inventory.inventory_drag()
                                inventory.inv_select1 = -1
                                inventory.inv_select2 = -1

        # drawing and updating game entities like the player
        player.draw(display, scrollx, scrolly)
        player.update(inventory, tiles, mobs, drops, popups, slabs)

        for drop in drops:
            drop.update(tiles, scrollx, scrolly)
            drop.draw(display, scrollx, scrolly)

        for popup in popups:
            popup.update(popups)
            popup.draw(display,scrollx, scrolly)

        for particle in particles:
            particle.update(display, particles, scrollx, scrolly)


        # draw inventory
        inventory.draw(inv_open, display, mousepos)

        # draw tile outlines
        if not inv_open:
            draw_tile_outline(mousepos, inventory.equipped, game_map, buildables, display, player, scrollx, scrolly)


        # draw display surface onto screen, update it and clock the fps
        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    main()
