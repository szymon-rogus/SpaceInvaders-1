import sys
import pygame
import controller
from view.scores import Scores


def you_win():

    controller.LEVEL += 1

    font1 = pygame.font.SysFont('comicsans', 150)
    title = font1.render("Victory", 1, controller.RED)
    controller.win.blit(title, ((controller.screenWidth - title.get_width()) / 2, controller.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(controller.SCORE), 1, controller.WHITE)
    controller.win.blit(description, ((controller.screenWidth - description.get_width()) / 2, controller.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press enter to move to level " + str(controller.LEVEL), 1, controller.GREEN)
    controller.win.blit(description, ((controller.screenWidth - description.get_width()) / 2, controller.screenHeight / 1.5))

    # controller.SCORE = 0
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return


def victory():

    controller.NEW_PLAYER = True
    controller.LEVEL = 1

    font1 = pygame.font.SysFont('comicsans', 150)
    title = font1.render("You have won the game", 1, controller.RED)
    controller.win.blit(title, ((controller.screenWidth - title.get_width()) / 2, controller.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(controller.SCORE), 1, controller.WHITE)
    controller.win.blit(description, ((controller.screenWidth - description.get_width()) / 2, controller.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press enter to move back to menu!", 1, controller.GREEN)
    controller.win.blit(description, ((controller.screenWidth - description.get_width()) / 2, controller.screenHeight / 1.5))

    scores = Scores()
    scores.save_score([controller.PLAYER_NAME, str(controller.SCORE)])

    controller.SCORE = 0
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # should actually show credits or final score and go back to menu then
            from controller.main import menu
            menu()
