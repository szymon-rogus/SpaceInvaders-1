from model.Life import Life
import controller


def life_draw(life):
    x = controller.screenWidth - 300
    y = 10
    for i in range(3):
        life[i] = Life(x, y, 100, 100)
        x -= 70
    return life
