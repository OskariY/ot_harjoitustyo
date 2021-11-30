"""
Northlands: unspaghettified

This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import pygame
import sys

# import constants/settings
from settings import *
# intialize pygame and set up display
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: unspaghettified")
# import functions, classes and resources (images, sound etc.) needed
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
    inv_surf = pygame.Surface((300, 32*6+2))
    invx = CENTER[0] - inv_surf.get_width() // 2
    invy = CENTER[1] - inv_surf.get_height() // 2
    inv_open = False
    inv_select1 = None
    inv_select2 = None
    equipped = ""

    inventory = [] # format: [ [rect, item, amount, equipped] ]
    x = 2
    y = 2
    for i in range(30):
        inventory.append([pygame.Rect(x, y, 30, 30), "", 0, False])
        x += 32
        if x > 150:
            x = 2
            y += 32
    # add some basic items to the inventory
    inventory = add_to_inventory(inventory, "axe", 1)
    inventory = add_to_inventory(inventory, "pickaxe", 1)
    inventory = add_to_inventory(inventory, "shovel", 1)
    inventory = add_to_inventory(inventory, "plank", 100)

    # hotbar
    hotbar_surf = pygame.Surface((32*5+4, 34))
    hotbar_x = CENTER[0] - hotbar_surf.get_width() // 2

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
                    # BROKEN CODE, FIX!!
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
                    inventory, equipped = equip_item(inventory, equipped, 0)
                if event.key == pygame.K_2:
                    inventory, equipped = equip_item(inventory, equipped, 1)
                if event.key == pygame.K_3:
                    inventory, equipped = equip_item(inventory, equipped, 2)
                if event.key == pygame.K_4:
                    inventory, equipped = equip_item(inventory, equipped, 3)
                if event.key == pygame.K_5:
                    inventory, equipped = equip_item(inventory, equipped, 4)
                
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
                        for i, item in enumerate(inventory):
                            testrect = item[0].copy()
                            testrect.x += invx
                            testrect.y += invy
                            if testrect.collidepoint(mousepos):
                                if inventory[i][1] != "":
                                    inv_select1 = i
                                    break
                # regular mouse countrols
                else:
                    if event.button == 1:
                        if equipped != "" and equipped != None:
                            # if item is food, heal player
                            if ITEMS[equipped]["food"] and player.health < player.max_health:
                                if player.health + ITEMS[equipped]["heal"] > player.max_health:
                                    player.health = player.max_health
                                else:
                                    player.health += ITEMS[equipped]["heal"]
                                inventory, equipped = remove_inventory_item(equipped, 1)
                                popups.append(FadingText(player.rect.centerx, player.rect.top, "+{} HP".format(str(items[equipped]["heal"])), GRASSGREEN))
                            # tool logic
                            if ITEMS[equipped]["tool"] and in_inventory(inventory, equipped):
                                #player.hit(equipped, mobs, worms, mousex, mousey)
                                breaking_tile = get_tile(mousepos, game_map, scrollx, scrolly)
                                if selected_tile != breaking_tile:
                                    selected_tile = breaking_tile
                                    tile_hits_left = 10
                                if breaking_tile != None:
                                    # reduce tile_hits_left based on the tool and the tile
                                    if equipped == "pickaxe" and breaking_tile[1] in ["stone", "coal block"]:
                                        if breaking_tile[1] == "stone":
                                            tile_hits_left -= 5
                                        if breaking_tile[1] == "coal block":
                                            tile_hits_left -= 2
                                    elif equipped == "shovel" and breaking_tile[1] in ["dirt", "grass", "snowy grass"]:
                                        tile_hits_left -= 5
                                    elif equipped == "axe" and breaking_tile[1] in ["tree1", "tree2", "tree3", "tree4"]:
                                            tile_hits_left -= 2
                                    elif equipped == "axe" and breaking_tile[1] in ["plank", "plank wall", "slab"]:
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
                                    #player.chop(items[equipped]["image"])

                                    if tile_hits_left <= 0:
                                        selected_tile = None
                                        tile_hits_left = 10
                                        remove_tile(mousepos, game_map, particles, drops, tiles, scrollx, scrolly, player)

                    if event.button == 3:
                        if equipped != "":
                            # place tiles
                            if ITEMS[equipped]["build"] and in_inventory(inventory, equipped):
                                if get_next_tiles(mousepos, buildables, scrollx, scrolly) == True:
                                    game_map = place_tile(mousepos, equipped, equipped, 
                                                          game_map, inventory, player, 
                                                          scrollx, scrolly)
                            # elif equipped == "hoe" and get_tile(mousepos)[1] == "dirt":
                            #     remove_tile(mousepos, True)
                            #     place_tile(mousepos, "grass", False)
            if event.type == pygame.MOUSEBUTTONUP:
                # inventory mouse controls
                if inv_open:
                    if event.button == 1:
                       # loop through the inventory grid and test for collisions
                       # if mouse collides with an inventory slot call the inventory drag function
                       for i, item in enumerate(inventory):
                            testrect = item[0].copy()
                            testrect.x += invx
                            testrect.y += invy
                            if testrect.collidepoint(mousepos):
                                inv_select2 = i
                                inventory = inventory_drag(inv_select1, inv_select2, inventory)
                                inv_select1 = None
                                inv_select2 = None

        # drawing and updating game entities like the player
        player.draw(display, scrollx, scrolly)
        player.update(scrollx, scrolly, inventory, tiles, mobs, drops, popups, slabs)

        for drop in drops:
            drop.update(tiles, scrollx, scrolly)
            drop.draw(display, scrollx, scrolly)

        for popup in popups:
            popup.update(popups)
            popup.draw(display,scrollx, scrolly)

        for particle in particles:
            particle.update(display, particles, scrollx, scrolly)

        # draw inventory
        if inv_open:
            inv_surf.fill(GRAY)
            x = 2
            y = 2
            # draw inventory grid
            for i in range(30):
                # draw hotbar with a different color
                if i < 5:
                    pygame.draw.rect(inv_surf, BLACK, inventory[i][0], 1)
                # draw other inventory slots
                else:
                    pygame.draw.rect(inv_surf, WHITE, inventory[i][0], 1)
                # if the slot contains an item, draw it along with text
                if inventory[i][1]:
                    inv_surf.blit(pygame.transform.scale(ITEMS[inventory[i][1]]["image"], (TILE_SIZE, TILE_SIZE)), (x + 2, y + 2))
                    print_text(str(inventory[i][2]), x + 29, y, inv_surf, 2, 8)
                    print_text(str(inventory[i][1][:8]), x + 16, y + 19, inv_surf, 1, 8)

                x += 32
                if x > 150:
                    x = 2
                    y += 32
            # draw the inventory surface to the display
            display.blit(inv_surf, (invx, invy))
            # draw dragging items in inventory
            if inv_select1 != '' and inv_select1 != None and inventory[inv_select1][1] != None:
                display.blit(ITEMS[inventory[inv_select1][1]]["image"], mousepos)
        # draw hotbar if inventory isn't open
        else:
            hotbar_surf.fill(GRAY)
            x = 2
            y = 2
            for i in range(5):
                if inventory[i][3]:
                    pygame.draw.rect(hotbar_surf, BLACK, pygame.Rect(x, y, 30, 30), 1)
                else:
                    pygame.draw.rect(hotbar_surf, WHITE, pygame.Rect(x, y, 30, 30), 1)
                if inventory[i][1]:
                    hotbar_surf.blit(ITEMS[inventory[i][1]]["image"], (x + 8, y + 8))
                    print_text(str(inventory[i][2]), x + 29, y, hotbar_surf, 2, 8, WHITE)

                x += 32

            # draw tile outlines
            draw_tile_outline(mousepos, equipped, game_map, buildables, display, player, scrollx, scrolly)
            display.blit(hotbar_surf, (hotbar_x, 0))


        # draw display surface onto screen, update it and clock the fps
        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    main()
