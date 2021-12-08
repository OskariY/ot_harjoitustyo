import sys
import pygame
from functions import print_text
from settings import WHITE, BLACK, GRAY, DISPLAY_WIDTH, DISPLAY_HEIGHT, CENTER
from save_functions import save_game
from menus.startmenu import startmenu

def pause(display, screen, clock, world, inventory, player, world_name):
    WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
    resume_game = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 - 16 - 40, 128, 32)
    menu_button = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 - 16, 128, 32)
    save_button = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 - 16 + 40, 128, 32)
    exit_game = pygame.Rect(DISPLAY_WIDTH // 2 - 64, DISPLAY_HEIGHT // 2 - 16 + 80, 128, 32)

    paused = True
    while paused:
        mousex, mousey = pygame.mouse.get_pos()
        mousex = mousex/(WINDOW_WIDTH/DISPLAY_WIDTH)
        mousey = mousey/(WINDOW_HEIGHT/DISPLAY_HEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if resume_game.collidepoint((mousex, mousey)):
                        paused = False
                    if exit_game.collidepoint((mousex, mousey)):
                        save_game(world_name, world, inventory, player)
                        pygame.quit()
                        sys.exit()
                    if menu_button.collidepoint((mousex, mousey)):
                        paused = False
                        save_game(world_name, world, inventory, player)
                        startmenu(display, screen, clock)
                    if save_button.collidepoint((mousex, mousey)):
                        save_game(world_name, world, inventory, player)


        pygame.draw.rect(display, GRAY, resume_game)
        pygame.draw.rect(display, GRAY, menu_button)
        pygame.draw.rect(display, GRAY, exit_game)
        pygame.draw.rect(display, GRAY, save_button)
        if resume_game.collidepoint((mousex, mousey)):
            pygame.draw.rect(display, WHITE, resume_game, 1)
            resume_text = WHITE
        else:
            pygame.draw.rect(display, BLACK, resume_game, 1)
            resume_text = BLACK

        if menu_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(display, WHITE, menu_button, 1)
            menu_text = WHITE
        else:
            pygame.draw.rect(display, BLACK, menu_button, 1)
            menu_text = BLACK
        if save_button.collidepoint((mousex, mousey)):
            pygame.draw.rect(display, WHITE, save_button, 1)
            save_text = WHITE
        else:
            pygame.draw.rect(display, BLACK, save_button, 1)
            save_text = BLACK

        if exit_game.collidepoint((mousex, mousey)):
            pygame.draw.rect(display, WHITE, exit_game, 1)
            exit_text = WHITE
        else:
            pygame.draw.rect(display, BLACK, exit_game, 1)
            exit_text = BLACK

        print_text("[ Paused ]", CENTER[0], 0, display, 1, 32, WHITE)
        print_text("Resume game", resume_game.centerx, resume_game.centery-8, display, 1, 16, resume_text)
        print_text("Save game", save_button.centerx, save_button.centery-8, display, 1, 16, save_text)
        print_text("Return to menu", menu_button.centerx, menu_button.centery-8, display, 1, 16, menu_text)
        print_text("Exit game", exit_game.centerx, exit_game.centery-8, display, 1, 16, exit_text)

        screen.blit(pygame.transform.scale(display, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
        pygame.display.update()
        clock.tick(60)


