"""
Northlands: unspaghettified

This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import pygame
import sys
import random

# import constants/settings
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, WHITE, FPS, CHUNK_SIZE, TILE_SIZE, GRAY, BROWN, GRASSGREEN, MUSIC, CENTER

# handle arguments
for arg in sys.argv:
    if "--nomusic" in arg:
        MUSIC = False
    if "--resolution" in arg:
        resolution = arg.split("=")[1].split("x")
        WINDOW_WIDTH = int(resolution[0])
        WINDOW_HEIGHT = int(resolution[1])

# intialize pygame and set up display
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: unspaghettified")
# import functions, classes and resources (images, sound etc.) needed
from resources import ITEMS, tree_image, jump_sound, break_sound
from entities import Player, Particle, FadingText
from inventory import Inventory
from functions import print_text
from world import World

def main():
    # pygame clock
    clock = pygame.time.Clock()

    # world object
    world = World()

    # player object
    player = Player(world.spawn_x, world.spawn_y)

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
    
    # if MUSIC setting is True, play music indefinately
    if MUSIC:
        pygame.mixer.music.play(-1)

    help_dismissed = 250 
    help_text = ["WASD: move and jump", 
                 "Mouse1: break block with tools",  
                 "Mouse2: place block", 
                 "1-6: select hotbar items"]

    # game loop
    while True:
        # get mouse position and divide it to get
        # true position since the game surface is stretched to the screen
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex/(WINDOW_WIDTH/DISPLAY_WIDTH)
        mousey = mousey/(WINDOW_HEIGHT/DISPLAY_HEIGHT)
        mousepos = (mousex, mousey)
        truemousepos = (mousex + world.scrollx, mousey + world.scrolly)

        # update world variables (e.g. scroll)
        world.update(mousepos, player)  
        # generate world
        world.generate_world(display)

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
                                world.popups.append(FadingText(player.rect.centerx, 
                                                    player.rect.top, 
                                                    "+{} HP".format(str(ITEMS[inventory.equipped]["heal"])), 
                                                    GRASSGREEN,
                                                    world.current_biome))
                            # tool logic
                            if ITEMS[inventory.equipped]["tool"] and inventory.in_inventory(inventory.equipped):
                                #player.hit(inventory.equipped, mobs, worms, mousex, mousey)
                                breaking_tile = world.get_tile(truemousepos)
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
                                        world.particles.append(Particle(breaking_tile[0][0]*TILE_SIZE+8, breaking_tile[0][1]*TILE_SIZE+8, particle_color))
                                    #player.chop(items[inventory.equipped]["image"])

                                    if tile_hits_left <= 0:
                                        selected_tile = None
                                        tile_hits_left = 10
                                        world.remove_tile(truemousepos, player)

                    if event.button == 3:
                        if inventory.equipped != "":
                            # place tiles
                            if ITEMS[inventory.equipped]["build"] and inventory.in_inventory(inventory.equipped):
                                if world.get_next_tiles(truemousepos) == True:
                                    world.place_tile(truemousepos, 
                                                     inventory.equipped,
                                                     inventory,
                                                     player)
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
        player.draw(display, world.scrollx, world.scrolly)
        player.update(inventory, world)

        for drop in world.drops:
            drop.update(world)
            drop.draw(display, world.scrollx, world.scrolly)

        for popup in world.popups:
            popup.update(world.popups)
            popup.draw(display,world.scrollx, world.scrolly)

        for particle in world.particles:
            particle.update(display, world.particles, world.scrollx, world.scrolly)


        # draw inventory
        inventory.draw(inv_open, display, mousepos)

        # draw tile outlines
        if not inv_open:
            world.draw_tile_outline(truemousepos, inventory.equipped, display, player)
       
        if world.current_biome == 1:
            biomename = "Forest"
        elif world.current_biome == 2:
            biomename = "Tundra"
        elif world.current_biome == 3:
            biomename = "Cave"
        else:
            biomename = world.current_biome
        
        if help_dismissed > 0:
            help_dismissed -= 1
            help_x = CENTER[0] - 96 
            help_y = CENTER[1] - 64
            print_text("Controls:", CENTER[0], help_y - 20, display, 1, 18)
            for t in help_text:
                print_text(t, help_x, help_y, display, 0, 18)
                help_y += 18
        else:
            print_text(f"biome: {biomename}", 0, 0, display, 0, 16)
            print_text(f"FPS: {int(clock.get_fps())}", 400, 0, display, 2, 16)

        # draw display surface onto screen, update it and clock the fps
        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
