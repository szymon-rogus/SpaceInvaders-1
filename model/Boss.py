import pygame
import Main
import random
from view import next_level


class Boss(object):
    boss_picture = pygame.image.load('../model/img/boss.png')

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 10
        self.start = start
        self.end = end
        self.path = [self.start, self.end, 100, Main.screenHeight - 350]  # where our enemy starts and finishes his path
        self.vel_x = 5
        self.vel_y = 5
        self.time_to_recovery = 0
        self.protected = False
        self.counter_x = random.randint(60, 300)
        self.counter_y = random.randint(60, 300)

    def draw(self, win):
        self.move()
        self.counter_x -= 1
        self.counter_y -= 1
        if self.counter_x == 0:
            self.counter_x = random.randint(90, 270)
            if self.vel_x > 0:
                self.vel_x = random.randint(4, 10)
            else:
                self.vel_x = random.randint(-10, -4)

        if self.counter_y == 0:
            self.counter_y = random.randint(90, 270)
            if self.vel_y > 0:
                self.vel_y = random.randint(4, 10)
            else:
                self.vel_y = random.randint(-10, -4)

        win.blit(self.boss_picture, (self.x, self.y))
        pygame.draw.rect(win, (255, 0, 0), (self.x + 50, self.y - 30, 200, 20))
        pygame.draw.rect(win, (0, 128, 0), (self.x + 50, self.y - 30, 200 - 20 * (10 - self.health), 20))

    # move in loop from left border to right and then from right to left
    def move(self):
        if self.vel_x > 0:
            if self.x + self.vel_x < self.path[1]:
                self.x += self.vel_x
            else:
                self.vel_x *= -1
        else:
            if self.x - self.vel_x > self.path[0]:
                self.x += self.vel_x
            else:
                self.vel_x *= -1

        if self.counter_x % random.randint(60, 180) == 0:
            self.vel_x *= -1

        if self.vel_y > 0:
            if self.y + self.vel_y < self.path[3]:
                self.y += self.vel_y
            else:
                self.vel_y *= -1
        else:
            if self.y - self.vel_y > self.path[2]:
                self.y += self.vel_y
            else:
                self.vel_y *= -1

        if self.counter_y % random.randint(60, 180) == 0:
            self.vel_y *= -1

    def check_collision(self, projectiles, win):
        for projectile in projectiles:
            if self.health >= 1:
                if self.x <= projectile.x <= self.x + self.width:
                    if self.y <= projectile.y <= self.y + self.height:
                        projectiles.pop(projectiles.index(projectile))
                        if not self.protected:
                            Main.SCORE += 10
                            self.health -= 1
                            self.protected = True
                            self.time_to_recovery = 30
            if self.health <= 0:
                self.draw(win)
                pygame.display.update()
                Main.SCORE += 1000
                explosion = pygame.mixer.Sound('../Main/sounds/explosion.wav')
                explosion.play()
                next_level.victory()

