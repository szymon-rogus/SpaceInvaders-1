import sys
import pygame
import Main
from view.scores import Scores


def you_win():

    win = True
    Main.LEVEL += 1

    font1 = pygame.font.SysFont('comicsans', 150)
    title = font1.render("Victory!", 1, Main.RED)
    Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press enter to move to level " + str(Main.LEVEL), 1, Main.GREEN)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    # Main.SCORE = 0
    pygame.display.update()

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            win = False
            from Main.main import main_loop
            main_loop()


def victory():

    win = True
    Main.NEW_PLAYER = True
    Main.LEVEL = 1

    font1 = pygame.font.SysFont('comicsans', 150)
    title = font1.render("You have won the game!", 1, Main.RED)
    Main.win.blit(title, ((Main.screenWidth - title.get_width()) / 2, Main.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(Main.SCORE), 1, Main.WHITE)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press enter to move back to menu! " + str(Main.LEVEL), 1, Main.GREEN)
    Main.win.blit(description, ((Main.screenWidth - description.get_width()) / 2, Main.screenHeight / 1.5))

    scores = Scores()
    scores.save_score([Main.PLAYER_NAME, str(Main.SCORE)])

    Main.SCORE = 0
    pygame.display.update()

    while win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # should actually show credits or final score and go back to menu then
            win = False
            from Main.main import menu
            menu()
