"""
###Warning: old spaghetti code###

viewer discretion is advised
"""

import os
import sys
import pygame
from world import World
from settings import DISPLAY_WIDTH, DISPLAY_HEIGHT, WHITE, BLACK, GRAY, CENTER
from functions import print_text
from resources import background_image
from save_functions import create_world

class MenuWorldSave():
    def __init__(self, name, x, y):
        self.name = name
        self.rect = pygame.Rect(x, y, 112, 18)
        self.selected = False

    def draw(self, surf):
        if self.selected == True:
            color = WHITE
        else:
            color = BLACK
        pygame.draw.rect(surf, GRAY, self.rect)
        pygame.draw.rect(surf, color, self.rect, 1)
        print_text(self.name, self.rect.centerx, self.rect.y, surf, 1, 16, color)

def startmenu(display, screen, clock):
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    world = World()
    # main menu buttons
    start_game = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 - 32, 128, 32)
    exit_game = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 + 8, 128, 32)
    particles = []

    # world screen buttons
    back_to_menu = pygame.Rect(64, DISPLAY_HEIGHT - 64, 128, 32)
    create_new_world = pygame.Rect(DISPLAY_WIDTH - 128 - 64, 32, 128, 32)
    remove_world = pygame.Rect(DISPLAY_WIDTH - 128 - 64, 80, 128, 32)
    world_surf = pygame.Surface((128, DISPLAY_HEIGHT // 1.5))
    world_surf.fill(GRAY)
    world_surf_rect = world_surf.get_rect()
    world_surf_rect.x = 64
    world_surf_rect.y = 32
    selected_world = None
    play_button = pygame.Rect(DISPLAY_WIDTH - 128 - 64, DISPLAY_HEIGHT - 64, 128, 32)

    # new world screen buttons
    new_world_name = ""
    new_world_rect = pygame.Rect(DISPLAY_WIDTH//2 - 128, DISPLAY_HEIGHT//2 - 32, 256, 64)
    new_world_back = pygame.Rect(DISPLAY_WIDTH//2 - 128, DISPLAY_HEIGHT//2 + 40, 120, 32)
    new_world_create = pygame.Rect(DISPLAY_WIDTH//2 + 8, DISPLAY_HEIGHT//2 + 40, 120, 32)

    create_world_screen = 0
    saved_worlds = []
    if not os.path.exists("saves/"):
        os.mkdir("saves/")
    for i, file in enumerate(os.listdir("saves/")):
        saved_worlds.append(MenuWorldSave(file, 8, 8 + 20*i))

    running = True
    while running:
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex/(WINDOW_WIDTH/DISPLAY_WIDTH)
        mousey = mousey/(WINDOW_HEIGHT/DISPLAY_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if create_world_screen == 2:
                    if event.key == pygame.K_BACKSPACE:
                        new_world_name = new_world_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(new_world_name) > 0:
                            create_world(new_world_name)
                            if len(saved_worlds) > 0:
                                y = saved_worlds[-1].rect.y + 20
                            else:
                                y = 8
                            saved_worlds.append(MenuWorldSave(new_world_name, 8, y))
                            create_world_screen = 1
                    else:
                        new_world_name += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if create_world_screen == 1:
                        if back_to_menu.collidepoint((mousex, mousey)):
                            create_world_screen = 0
                        if create_new_world.collidepoint((mousex, mousey)):
                            # create world
                            create_world_screen = 2

                        if selected_world != None:
                            if play_button.collidepoint((mousex, mousey)):
                                return selected_world
                            if remove_world.collidepoint((mousex, mousey)):
                                os.remove("saves/{}".format(selected_world))
                                for saved_world in list(saved_worlds):
                                    if saved_world.name == selected_world:
                                        saved_worlds.remove(saved_world)
                                selected_world = None

                        for save in saved_worlds:
                            if save.rect.collidepoint((mousex-world_surf_rect.x, mousey-world_surf_rect.y)):
                                if save.selected == True:
                                    save.selected = False
                                    selected_world = None
                                else:
                                    save.selected = True
                                    selected_world = save.name
                                    for other_save in saved_worlds:
                                        if other_save != save:
                                            other_save.selected = False
                    elif create_world_screen == 2:
                        if new_world_back.collidepoint((mousex, mousey)):
                            create_world_screen = 1
                        if new_world_create.collidepoint((mousex, mousey)):
                            if len(new_world_name) > 0:
                                create_world(new_world_name)
                                if len(saved_worlds) > 0:
                                    y = saved_worlds[-1].rect.y + 20
                                else:
                                    y = 8
                                saved_worlds.append(MenuWorldSave(new_world_name, 8, y))
                                create_world_screen = 1

                    else:
                        if start_game.collidepoint((mousex, mousey)):
                            create_world_screen = 1
                        if exit_game.collidepoint((mousex, mousey)):
                            pygame.quit()
                            sys.exit()
            if create_world_screen == 1 and event.type == pygame.MOUSEWHEEL:
                for save in saved_worlds:
                    save.rect.y += event.y * 3

        display.blit(pygame.transform.scale(background_image, (DISPLAY_WIDTH, DISPLAY_HEIGHT)), (0, 0))
        # for particle in particles:
        #     particle.update(display, particles)

        # create world screen
        if create_world_screen == 1:
            display.blit(world_surf, (64, 32))
            world_surf.fill(GRAY)
            pygame.draw.rect(display, BLACK, world_surf_rect, 1)
            pygame.draw.rect(display, GRAY, back_to_menu)
            pygame.draw.rect(display, GRAY, create_new_world)

            if back_to_menu.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, back_to_menu, 1)
                back_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, back_to_menu, 1)
                back_text = BLACK

            if create_new_world.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, create_new_world, 1)
                new_world_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, create_new_world, 1)
                new_world_text = BLACK

            if selected_world:
                pygame.draw.rect(display, GRAY, play_button)
                if play_button.collidepoint((mousex, mousey)):
                    pygame.draw.rect(display, WHITE, play_button, 1)
                    play_button_text = WHITE
                else:
                    pygame.draw.rect(display, BLACK, play_button, 1)
                    play_button_text = BLACK
                print_text("Play", play_button.centerx, play_button.centery-8, display, 1, 16, play_button_text)

                pygame.draw.rect(display, GRAY, remove_world)
                if remove_world.collidepoint((mousex, mousey)):
                    pygame.draw.rect(display, WHITE, remove_world, 1)
                    remove_world_text = WHITE
                else:
                    pygame.draw.rect(display, BLACK, remove_world, 1)
                    remove_world_text = BLACK
                print_text("Remove World", remove_world.centerx, remove_world.centery-8, display, 1, 16, remove_world_text)

            for save in saved_worlds:
                save.draw(world_surf)
            print_text("Back to Menu", back_to_menu.centerx, back_to_menu.centery-8, display, 1, 16, back_text)
            print_text("Create New World", create_new_world.centerx, create_new_world.centery-8, display, 1, 16, new_world_text)
            print_text("Worlds", world_surf_rect.centerx, world_surf_rect.y-16, display, 1, 16, BLACK)

        elif create_world_screen == 2:
            pygame.draw.rect(display, GRAY, new_world_rect)
            pygame.draw.rect(display, GRAY, new_world_back)
            pygame.draw.rect(display, GRAY, new_world_create)

            if new_world_back.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, new_world_back, 1)
                back_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, new_world_back, 1)
                back_text = BLACK
            if new_world_create.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, new_world_create, 1)
                create_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, new_world_create, 1)
                create_text = BLACK


            print_text("Type world name:", new_world_rect.centerx, new_world_rect.y, display, 1, 16, BLACK)
            print_text(new_world_name, new_world_rect.centerx, new_world_rect.centery-8, display, 1, 16, BLACK)
            print_text("Back", new_world_back.centerx, new_world_back.centery-8, display, 1, 16, back_text)
            print_text("Create", new_world_create.centerx, new_world_create.centery-8, display, 1, 16, create_text)

        # main menu
        else:

            pygame.draw.rect(display, GRAY, start_game)
            pygame.draw.rect(display, GRAY, exit_game)
            if start_game.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, start_game, 1)
                start_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, start_game, 1)
                start_text = BLACK

            if exit_game.collidepoint((mousex, mousey)):
                pygame.draw.rect(display, WHITE, exit_game, 1)
                exit_text = WHITE
            else:
                pygame.draw.rect(display, BLACK, exit_game, 1)
                exit_text = BLACK

            print_text("The Northlands", CENTER[0], 32, display, 1, 48, BLACK)
            print_text("The Northlands", CENTER[0]+2, 32, display, 1, 48, WHITE)
            print_text("Start Game", start_game.centerx, start_game.centery-8, display, 1, 16, start_text)
            print_text("Exit Game", exit_game.centerx, exit_game.centery-8, display, 1, 16, exit_text)
            print_text("By: Oskari Ylönen", 0, DISPLAY_HEIGHT-16, display, 0, 16, BLACK)

        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(60)


