import sys
import pygame
import controller
from view.scores import Scores


def game_over():

    controller.LEVEL = 1
    controller.NEW_PLAYER = True
    pygame.mixer.music.stop()

    font1 = pygame.font.SysFont('comicsans', 200)
    title = font1.render("Game over!", 1, controller.RED)
    controller.win.blit(title, ((controller.screenWidth - title.get_width()) / 2, controller.screenHeight / 3.5))

    font2 = pygame.font.SysFont('comicsans', 100)
    description = font2.render("Your score: " + str(controller.SCORE), 1, controller.WHITE)
    controller.win.blit(description, ((controller.screenWidth - description.get_width()) / 2, controller.screenHeight / 2))

    font3 = pygame.font.SysFont('comicsans', 80)
    description = font3.render("Press space to continue", 1, controller.GREEN)
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
        if keys[pygame.K_SPACE]:
            return
