"""
Northlands: unspaghettified

This project is an attempt to clean up my previous game which was full on
spaghetti code.

"""

import sys
import pygame

# import constants/settings
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT, \
                     BLACK, WHITE, FPS, TILE_SIZE, GRAY, BROWN, GRASSGREEN, MUSIC, \
                     CENTER, FULLSCREEN

# intialize pygame and set up display
pygame.init()
if FULLSCREEN:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
else:
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("Northlands: unspaghettified")
# pygame clock
clock = pygame.time.Clock()

# import functions, classes and resources (images, sound etc.) needed
from resources import ITEMS, CRAFTING_REQUIREMENTS, jump_sound, break_sound, hurt_sound, songs, \
                      evening, morning, night, darkness, glow
from entities.player import Player
from entities.particle import Particle
from entities.fadingtext import FadingText
from entities.walkingmob import WalkingMob
from entities.flyingmob import FlyingMob
from entities.caveworm import Worm
from inventory import Inventory
from functions import print_text, chunk_debug
from world import World
from menus.pause import pause
from menus.startmenu import startmenu
from save_functions import load_game, create_world
from console import Console

def main(world_name):
    console = Console(WINDOW_WIDTH // 4, 0, WINDOW_WIDTH // 2,
                      WINDOW_HEIGHT // 3, 24)
    console.log("Logger started")

    # load game data from save file
    game_data = load_game(world_name)

    # player object
    player = Player(game_data["player_x"], game_data["player_y"])

    # inventory related variables
    inventory = Inventory()
    inv_open = False
    if game_data["inventory"] == []:
        # add some basic items to the inventory
        inventory.add_to_inventory("axe", 1)
        inventory.add_to_inventory("pickaxe", 1)
        inventory.add_to_inventory("shovel", 1)
    else:
        inventory.inventory = game_data["inventory"]

    # world object
    world = World(console)

    # load world related variables from the save
    world.game_map = game_data["game_map"]
    world.scrollx = game_data["scrollx"]
    world.scrolly = game_data["scrolly"]
    world.seed = game_data["seed"]
    world.tod = game_data["tod"]
    for x, y, mobtype in game_data["mob_coords"]:
        if mobtype == "bear":
            mob = WalkingMob(x, y)
        elif mobtype == "bird":
            mob = FlyingMob(x, y)
        world.mobs.append(mob)
        world.entities.append(mob)

    for x, y in game_data["worm_coords"]:
        worm = Worm(x, y)
        world.worms.append(worm)

    inventory.equip_item(0)

    # tile breaking related variables
    selected_tile = None
    tile_hits_left = 10

    chunk_debug_enabled = False

    song_playing = 0 # index of the current song

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
        world.update(player)
        # generate world
        world.generate_world(display, player)

        # event loop
        for event in pygame.event.get():
            # quitting game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.constants.USEREVENT:
                song_playing += 1
                if song_playing >= len(songs):
                    song_playing = 0
                pygame.mixer.music.load(songs[song_playing])
                pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
                pygame.mixer.music.play()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    console.show = not console.show
                    if console.show == True:
                        console.focused = True
                    else:
                        console.focused = False
                    console.offset = 0

                if console.focused:
                    if event.key == pygame.K_RETURN:
                        console.command(inventory, world, player)
                    elif event.key == pygame.K_BACKSPACE:
                        console.cmdbuffer = console.cmdbuffer[:-1]
                    else:
                        console.cmdbuffer += event.unicode

                else:
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
                        if inv_open is False:
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
                    if event.key == pygame.K_F8:
                        player.rect.y += 1000
                    if event.key == pygame.K_F9:
                        create_world("test")
                        main("test")
                    if event.key == pygame.K_F5:
                        player.chop()
                    if event.key == pygame.K_F3:
                        if chunk_debug_enabled:
                            chunk_debug_enabled = False
                        else:
                            chunk_debug_enabled = True
                    if console.show:
                        if event.key == pygame.K_k:
                            console.offset -= 50
                        if event.key == pygame.K_j:
                            console.offset += 50
                    if event.key == pygame.K_ESCAPE:
                        world_name = pause(display, screen, clock, world, inventory, player, world_name)
                        if world_name:
                            main(world_name)
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
                        if inventory.crafting_item_selected is not None:
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
                        if inventory.equipped != "" and inventory.equipped is not None:
                            # if item is food, heal player
                            if ITEMS[inventory.equipped]["food"] and player.health < player.max_health:
                                if player.health + ITEMS[inventory.equipped]["heal"] > player.max_health:
                                    player.health = player.max_health
                                else:
                                    player.health += ITEMS[inventory.equipped]["heal"]
                                world.popups.append(FadingText(player.rect.centerx,
                                                    player.rect.top,
                                                    "+{} HP".format(str(ITEMS[inventory.equipped]["heal"])),
                                                    world.current_biome,
                                                    GRASSGREEN
                                                    ))
                                inventory.remove_item(inventory.equipped, 1)

                            # tool logic
                            if ITEMS[inventory.equipped]["tool"] and inventory.in_inventory(inventory.equipped):
                                player.hit(inventory.equipped, world, mousex, mousey)
                                breaking_tile = world.get_tile(truemousepos)
                                if selected_tile != breaking_tile:
                                    selected_tile = breaking_tile
                                    tile_hits_left = 10
                                if breaking_tile is not None:
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
                                    elif breaking_tile[1] in ["plant", "torch", "sapling"]:
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

                                    if tile_hits_left <= 0:
                                        selected_tile = None
                                        tile_hits_left = 10
                                        world.remove_tile(truemousepos, player)

                    if event.button == 3:
                        if inventory.equipped != "":
                            # place tiles
                            if ITEMS[inventory.equipped]["build"] and inventory.in_inventory(inventory.equipped):
                                if world.get_next_tiles(truemousepos) is True:
                                    player.chop()
                                    world.place_tile(truemousepos,
                                                     inventory.equipped,
                                                     inventory,
                                                     player)
                            # elif inventory.equipped == "hoe" and get_tile(mousepos)[1] == "dirt":
                            #     remove_tile(mousepos, True)
                            #     place_tile(mousepos, "grass", False)
                    if event.button in [4, 5]:
                        if event.button == 4:
                            inventory.index_equipped += 1
                        elif event.button == 5:
                            inventory.index_equipped -= 1

                        if inventory.index_equipped < 0:
                            inventory.index_equipped = 4
                        if inventory.index_equipped > 4:
                            inventory.index_equipped = 0
                        inventory.equip_item(inventory.index_equipped)
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
            if event.type == pygame.MOUSEMOTION:
                console.update()
        # drawing and updating game entities like the player
        player.draw(display, world, inventory)
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

        # set time of day and draw appropriate lighting
        # 0-40000 = day, 40000-50000 = evening, 50000-90000 = night, 90000-100000
        world.tod += 10
        if world.current_biome != 3:
            if world.tod < 40000:
                world.is_night = False
            elif 40000 < world.tod < 50000:
                display.blit(evening, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                world.is_night = False
            elif 90000 < world.tod < 100000:
                display.blit(morning, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                world.is_night = False
            elif 50000 < world.tod < 90000:
                display.blit(night, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                world.is_night = True
        else:
            display.blit(darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        if world.tod >= 100000:
            world.tod = 0
        if world.tod > 40000:
            for glowpos in world.glows:
                display.blit(glow, glowpos, special_flags=pygame.BLEND_RGBA_ADD)

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

        if world.current_biome == 3:
            fps_color = WHITE
        else:
            fps_color = BLACK

        print_text(f"FPS: {int(clock.get_fps())}", 1, 0, display, 0, 10, fps_color)
        if chunk_debug_enabled:
            chunk_debug(truemousepos, display, world)
            print_text(f"Current biome: {biomename}", 1, 10, display, 0, 10, fps_color)
            print_text(f"X: {player.rect.x} Y: {player.rect.y}", 1, 20, display, 0, 10, fps_color)
            print_text(f"Seed: {world.seed}", 1, 30, display, 0, 10, fps_color)
            print_text(f"tod: {world.tod}", 1, 40, display, 0, 10, fps_color)


        # draw display surface onto screen, update it and clock the fps
        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        console.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    world_name = startmenu(display, screen, clock)
    main(world_name)
