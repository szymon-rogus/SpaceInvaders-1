import sys
import pygame
import random
import controller
from model.Boss import Boss
from model.Cover import Cover
from model.Player import Player
from model.Projectile import Projectile
from model.SpecialEnemy import SpecialEnemy
from view.description import description_of_game
from view.game_over import game_over
from view.object_draw import draw_block_of_enemies
from view.life_draw import life_draw
from view.scores import Scores
from view.next_level import you_win

pygame.init()


def check_for_boss_level():
    if controller.LEVEL == 5:
        controller.BOSS = True
        pygame.mixer.music.load('../controller/sounds/boss.wav')
    else:
        controller.BOSS = False
        music = pygame.mixer.music.load('../controller/sounds/music1.wav')

    pygame.mixer.music.rewind()
    pygame.mixer.music.play()


# noinspection PyInterpreter
def button(message, x, y, w, h, color, mouse_hover, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    flag = True

    font = pygame.font.SysFont("comicsansms", 40)
    text = font.render(message, 1, color)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(controller.win, mouse_hover, (x, y, text.get_width(), h))
        if click[0] == 1 and action is not None:
            # noinspection PyInterpreter
            if action == "main_loop":
                main_loop()
            elif action == "quit_game":
                pygame.quit()
                sys.exit()
            elif action == "description":
                description_of_game()
            elif action == "high_scores":
                scores = Scores()
                scores.show_high_scores()

    if flag is True:
        controller.win.blit(text, (x, y))
    return flag


def menu():
    intro = True
    pygame.mixer.music.stop()
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        controller.win.blit(controller.bg, (0, 0))
        font1 = pygame.font.SysFont('comicsans', 100)
        title = font1.render("Space Invaders", 1, controller.YELLOW)
        controller.win.blit(title, ((controller.screenWidth - title.get_width()) / 2, controller.screenHeight / 5))

        button_width = 200
        button_height = 50
        button("Play", (controller.screenWidth - button_width) / 2, controller.screenHeight * 2 / 5, button_width, button_height, controller.WHITE, controller.GRAY, "main_loop")
        button("Description", (controller.screenWidth - button_width) / 2, controller.screenHeight * 2.5 / 5, button_width, button_height, controller.WHITE, controller.GRAY, "description")
        button("High scores", (controller.screenWidth - button_width) / 2, controller.screenHeight * 3 / 5, button_width, button_height, controller.WHITE, controller.GRAY, "high_scores")
        intro = button("Quit", (controller.screenWidth - button_width) / 2, controller.screenHeight * 3.5 / 5, button_width, button_height, controller.WHITE, controller.GRAY, "quit_game")

        pygame.display.update()


# in every frame display all objects on their current positions
def redraw_game_window(player, enemy, special_alien, projectiles, enemy_projectiles, lives, alive, covers, boss,
                       boss_projectiles_left, boss_projectiles_right, boss_projectiles_central):

    controller.win.blit(controller.bg, (0, 0))
    player.draw(controller.win)
    for bullet in projectiles:
        bullet.draw(controller.win)

    if not controller.BOSS:  # normal level without boss
        for enemy_bullet in enemy_projectiles:
            enemy_bullet.draw(controller.win)
            player.is_player_hit(enemy_projectiles)

        for i in range(len(enemy)):
            for j in range(len(enemy[i])):
                if enemy[i][j].check_collision(projectiles) is True and enemy[i][j].status is True:
                    enemy[i][j].draw(controller.win)
                else:
                    enemy[i][j].status = False
                    alive -= 1

        for cover in covers:
            cover.check_collision(projectiles)
            cover.check_collision(enemy_projectiles)
            cover.draw(controller.win)

        if special_alien.check_collision(projectiles) is True and special_alien.status is True:
            special_alien.draw(controller.win)
        else:
            special_alien.status = False

    else:  # boss level
        boss.draw(controller.win)
        boss.check_collision(projectiles, controller.win)
        for boss_bullet in boss_projectiles_left:
            boss_bullet.draw(controller.win)
            player.is_player_hit(boss_projectiles_left)
        for boss_bullet in boss_projectiles_right:
            boss_bullet.draw(controller.win)
            player.is_player_hit(boss_projectiles_right)
        for boss_bullet in boss_projectiles_central:
            boss_bullet.draw(controller.win)
            player.is_player_hit(boss_projectiles_central)

        if boss.time_to_recovery > 0:
            boss.time_to_recovery -= 1
            if boss.time_to_recovery == 0:
                boss.protected = False

    if alive >= 1:
        life_count = player.health
        for life in lives:
            life_count -= 1
            if life_count < 0:
                life.status = False
            life.draw(controller.win)
    else:
        you_win()
        main_loop()

    # display score
    score = pygame.font.SysFont('comicsans', 50)
    description = score.render("Score: " + str(controller.SCORE), 1, controller.WHITE)
    controller.win.blit(description, (controller.screenWidth - description.get_width() - 20, 20))

    # display level
    level = pygame.font.SysFont('comicsans', 50)
    lvl_description = level.render("Level: " + str(controller.LEVEL), 1, controller.WHITE)
    controller.win.blit(lvl_description, (20, 20))

    if player.health < 1:
        game_over()
        menu()

    pygame.display.update()


def main_loop():
    pygame.display.update()

    # Ship can shoot only if this variable is equal to 0. After every successful shoot this variable is incremented,
    # and if reaches 10, then is reduced again to 0. This feature prevent from shooting all projectiles at once
    # which can cause undesirable blurred trail on screen

    can_shoot = 0
    number = random.randint(1, 5)
    controller.bg = pygame.image.load('../model/img/big_sky' + str(number) + '.jpg')
    frequency_of_alien_shooting = 111 - controller.LEVEL * 10
    frequency_of_boss_shooting = 30
    frequency_of_boss_special_shooting = 70

    player = Player(20, controller.screenHeight - 100, 60, 60)
    enemy = [[None] * 10, [None] * 10, [None] * 10]
    alive = len(enemy) * len(enemy[0])
    enemy = draw_block_of_enemies(enemy)
    special_alien = SpecialEnemy(0, 60, controller.alien_size, controller.alien_size, 0, controller.screenWidth, False)
    boss = Boss(10, 100, 320, 100, 30, controller.screenWidth - 330)

    lives = [None, None, None]
    lives = life_draw(lives)

    projectiles = []
    enemy_projectiles = []
    boss_projectiles_central = []
    boss_projectiles_left = []
    boss_projectiles_right = []

    covers = []
    cover_number = 1
    while cover_number <= 3:
        cover = Cover(controller.screenWidth * ((2 * cover_number - 1) / 7), controller.screenHeight * (8 / 10))
        covers.append(cover)
        cover_number += 1

    check_for_boss_level()

    run = True
    paused = False
    while run:
        controller.clock.tick(30)  # fps
        # always possible to exit game at any time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        # normal level without a boss
        if not controller.BOSS:
            special = random.randint(1, 500)
            if special == 10 and controller.SPECIAL == 0:
                special_alien.status = True
                controller.SPECIAL += 1
            if special_alien.status is False and controller.SPECIAL == 1:
                controller.SPECIAL = 0
                special_alien = SpecialEnemy(0, 60, 60, 60, 0, controller.screenWidth, False)

            enemy_shot = random.randint(1, frequency_of_alien_shooting)
            enemy_x = random.randint(0, 9)
            enemy_y = random.randint(0, 2)

            for enemy_projectile in enemy_projectiles:
                if 0 < enemy_projectile.y > 0:
                    enemy_projectile.y += enemy_projectile.vel
                else:
                    enemy_projectiles.pop(enemy_projectiles.index(enemy_projectile))

            if enemy_shot == 2 and enemy[enemy_y][enemy_x].status is True:
                enemy_projectiles.append(
                    Projectile(round(enemy[enemy_y][enemy_x].x + enemy[enemy_y][enemy_x].width // 2),
                               round(enemy[enemy_y][enemy_x].y + enemy[enemy_y][enemy_x].height // 2),
                               4, controller.GREEN, 10))
            elif enemy[enemy_y][enemy_x].status is False and frequency_of_alien_shooting > 10:
                frequency_of_alien_shooting -= 1

        # boss level
        else:
            boss_shoot_central = random.randint(1, frequency_of_boss_special_shooting)
            boss_shoot_side = random.randint(1, frequency_of_boss_shooting)
            if boss_shoot_side == 10:
                boss_projectiles_left.append(Projectile(round(boss.x + boss.width * (1/4)),
                                                        round(boss.y + boss.height // 2, 10),
                                                        6, controller.GREEN, 10))
                boss_projectiles_right.append(Projectile(round(boss.x + boss.width * (3 / 4)),
                                                         round(boss.y + boss.height // 2),
                                                         6, controller.GREEN, 10))
                boss_projectiles_central.append(Projectile(round(boss.x + boss.width * (1 / 4)),
                                                           round(boss.y + boss.height // 2, 10),
                                                           6, controller.GREEN, 10))
                boss_projectiles_central.append(Projectile(round(boss.x + boss.width * (3 / 4)),
                                                           round(boss.y + boss.height // 2),
                                                           6, controller.GREEN, 10))
            if boss_shoot_central == 20:
                boss_projectiles_central.append(Projectile(round(boss.x + boss.width * (1/2)),
                                                           round(boss.y + boss.height * (3/4)),
                                                           20, controller.ORANGE, 20))
            for boss_projectile in boss_projectiles_left:
                if 0 < boss_projectile.y > 0:
                    boss_projectile.x -= boss_projectile.vel / 1.5
                    boss_projectile.y += boss_projectile.vel
                else:
                    enemy_projectiles.pop(enemy_projectiles.index(boss_projectile))
            for boss_projectile in boss_projectiles_right:
                if 0 < boss_projectile.y > 0:
                    boss_projectile.x += boss_projectile.vel / 1.5
                    boss_projectile.y += boss_projectile.vel
                else:
                    enemy_projectiles.pop(enemy_projectiles.index(boss_projectile))
            for boss_projectile in boss_projectiles_central:
                if 0 < boss_projectile.y > 0:
                    boss_projectile.y += boss_projectile.vel
                else:
                    enemy_projectiles.pop(enemy_projectiles.index(boss_projectile))

        # display projectiles until they reach top border of screen
        # if projectile reaches top border of screen remove it from array so that ship could shoot next ones
        for projectile in projectiles:
            if 0 < projectile.y > 0:
                projectile.y -= projectile.vel
            else:
                projectiles.pop(projectiles.index(projectile))
        if can_shoot > 0:
            can_shoot += 1
        if can_shoot >= 21 - controller.LEVEL:
            can_shoot = 0

        # handle keys pressed by player (left arrow, right arrow, space)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > player.vel and not player.killed:
            player.x -= player.vel
        elif keys[pygame.K_RIGHT] and player.x < controller.screenWidth - player.width - player.vel and not player.killed:
            player.x += player.vel
        if keys[pygame.K_SPACE] and can_shoot == 0 and not player.protection:
            pygame.mixer.music.stop()
            controller.shoot.play()
            pygame.mixer.music.play()
            if len(projectiles) < 12:  # up to 10 projectiles on screen at the same moment
                projectiles.append(Projectile(round(player.x + player.width // 2),
                                              round(player.y + player.height // 2), 4, (255, 128, 0), 10))
            can_shoot += 1
        if keys[pygame.K_ESCAPE]:
            run = False
            paused = True
            controller.SCORE = 0
            controller.LEVEL = 1
            Player.health = 3
            menu()
        if keys[pygame.K_p]:
            if paused is False:
                paused = True
            else:
                paused = False

        # refresh screen
        if paused is False:
            redraw_game_window(player, enemy, special_alien, projectiles, enemy_projectiles, lives, alive, covers, boss,
                               boss_projectiles_left, boss_projectiles_right, boss_projectiles_central)


menu()
