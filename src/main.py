"""
Northlands: unspaghettified

This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import pygame
import sys
import random

# import constants/settings
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, BLACK, WHITE, FPS, CHUNK_SIZE, TILE_SIZE, GRAY, BROWN, GRASSGREEN, MUSIC, CENTER, FULLSCREEN

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
if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
else:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: unspaghettified")
# import functions, classes and resources (images, sound etc.) needed
from resources import ITEMS, CRAFTING_REQUIREMENTS, tree_image, jump_sound, break_sound, hurt_sound
from entities import Player, Particle, FadingText, WalkingMob
from inventory import Inventory
from functions import print_text, chunk_debug
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
    inventory.add_to_inventory("meat", 10)
    
    inventory.equip_item(0)

    # tile breaking related variables
    selected_tile = None
    tile_hits_left = 10
    
    # if MUSIC setting is True, play music indefinately
    if MUSIC:
        pygame.mixer.music.play(-1)
    
    chunk_debug_enabled = False
    help_dismissed = False 
    help_text = ["WASD: move and jump", 
                 "Mouse1: break block with tools",  
                 "Mouse2: place block", 
                 "1-6: select hotbar items",
                 "TAB: open/close inventory",
                 "",
                 "press h to open/close help"]

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
        world.generate_world(display, player)

        # event loop
        for event in pygame.event.get():
            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    mob = WalkingMob(player.rect.x + 50, player.rect.y - 100)
                    world.mobs.append(mob)
                    world.entities.append(mob)
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
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_h:
                    if help_dismissed:
                        help_dismissed = False
                    else:
                        help_dismissed = True
                if event.key == pygame.K_o:
                    if chunk_debug_enabled:
                        chunk_debug_enabled = False
                    else:
                        chunk_debug_enabled = True
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
                        
                        # crafting selections
                        for i, selectbutton in enumerate(inventory.crafting_selection_rects):
                            if selectbutton.collidepoint((mousepos[0] - inventory.invx, 
                                                          mousepos[1] - inventory.invy)):
                                inventory.crafting_item_selected = i
                                inventory.crafting_item_rect = selectbutton
                                break

                        # crafting pagination
                        if inventory.crafting_back_button.collidepoint((mousepos[0] - inventory.invx, 
                                                                        mousepos[1] - inventory.invy)):
                            if inventory.crafting_index_1 > 0:
                                if inventory.crafting_index_1 - 6 > 0:
                                    inventory.crafting_index_1 -= 6
                                    inventory.crafting_index_2 -= 6
                                else:
                                    inventory.crafting_index_1 = 0
                                    inventory.crafting_index_2 = 6
                        if inventory.crafting_next_button.collidepoint((mousepos[0] - inventory.invx, 
                                                                        mousepos[1] - inventory.invy)):
                            craftables = len(list(CRAFTING_REQUIREMENTS.keys()))
                            if inventory.crafting_index_2 < craftables:
                                if inventory.crafting_index_2 + 6 < craftables:
                                    inventory.crafting_index_1 += 6
                                    inventory.crafting_index_2 += 6
                                else:
                                    inventory.crafting_index_2 = craftables
                                    inventory.crafting_index_1 = craftables - 6

                        # crafting button
                        if inventory.crafting_item_selected != None:
                            if inventory.crafting_item_selected < len(inventory.visible_crafting_items):
                                if inventory.crafting_button.collidepoint((mousepos[0] - inventory.invx, 
                                                                           mousepos[1] - inventory.invy)):
                                    have_requirements = True
                                    for requirement in CRAFTING_REQUIREMENTS[inventory.visible_crafting_items[inventory.crafting_item_selected]]:
                                        if not inventory.in_inventory(requirement[0], requirement[1]):
                                            have_requirements = False
                                    if have_requirements:
                                        inventory.add_to_inventory(inventory.visible_crafting_items[inventory.crafting_item_selected], 1)
                                        for requirement in CRAFTING_REQUIREMENTS[inventory.visible_crafting_items[inventory.crafting_item_selected]]:
                                            inventory.remove_item(requirement[0], requirement[1])


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
                                                    world.current_biome,
                                                    GRASSGREEN
                                                    ))
                            # tool logic
                            if ITEMS[inventory.equipped]["tool"] and inventory.in_inventory(inventory.equipped):
                                player.hit(inventory.equipped, world, mousex, mousey)
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

        for mob in world.mobs:
            mob.update(player, world)
            mob.draw(display, world)
            # check for collisions with the player
            if mob.rect.colliderect(player.rect):
                player.health -= 1
                if player.sound_cooldown <= 0:
                    hurt_sound.play()
                    player.sound_cooldown = 10 
        
        for worm in world.worms:
            worm.update(player, world)
            worm.draw(display, world.scrollx, world.scrolly)

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
        
        if not help_dismissed:
            help_x = CENTER[0] - 96 
            help_y = CENTER[1] - 64
            print_text("Controls:", CENTER[0], help_y - 20, display, 1, 18)
            for t in help_text:
                print_text(t, help_x, help_y, display, 0, 18)
                help_y += 18
        else:
            if world.current_biome == 3:
                fps_color = WHITE
            else:
                fps_color = BLACK
            print_text(f"biome: {biomename}", 0, 0, display, 0, 10, fps_color)
            print_text(f"FPS: {int(clock.get_fps())}", DISPLAY_WIDTH, 0, display, 2, 10, fps_color)
        
        if chunk_debug_enabled:
            chunk_debug(truemousepos, display, world)

        # draw display surface onto screen, update it and clock the fps
        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
