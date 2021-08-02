from tkinter import messagebox
from random import choice
import pygame
import random
import tkinter

root = tkinter.Tk()
root.withdraw()

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake")

headImages = [pygame.image.load("snake_up.jpg"),
              pygame.image.load("snake_down.jpg"),
              pygame.image.load("snake_left.jpg"),
              pygame.image.load("snake_right.jpg")]


class head:
    def __init__(self, x, y):
        self.height = 20
        self.vel = 20
        self.width = 20
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(headImages[direction], (self.x, self.y))


class body:
    def __init__(self, x, y):
        self.height = 20
        self.vel = 20
        self.width = 20
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (199, 6, 7), (self.x, self.y, self.height, self.width))


class snack:
    def __init__(self, x, y):
        self.height = 20
        self.width = 20
        self.x = x
        self.y = y

    def draw(self, win):
        pygame.draw.rect(win, (51, 204, 51), (self.x, self.y, self.height, self.width))


def checkHighScore():
    highscore = open("highscore.txt")

    if score > int(highscore.read()):
        highscore = open("highscore.txt", "w")
        highscore.write(str(score))


def outputHighScore():
    highscore = open("highscore.txt")
    return highscore.read()


def redrawGameWindow():
    win.fill((22, 22, 24))
    snakeHead.draw(win)
    for snakeBody in bodies:
        snakeBody.draw(win)
    if len(foods) > 0:
        food.draw(win)
    pygame.display.update()


# main loop
up = down = left = False
right = True
run = True
score = pos = oneLoop = 0
foods = []
bodies = []
mem = []
xy = []
snakeHead = head(20, 20)
while run:
    pygame.time.delay(80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    exception_x = []
    exception_y = []

    if len(foods) < 1:
        food_x = 500 - random.randrange(0, 25) * 20 - 20
        food_y = 500 - random.randrange(0, 25) * 20 - 20

        for snakeBody in bodies:
            xy[bodies.index(snakeBody)].append(snakeBody.x)
            xy[bodies.index(snakeBody)].append(snakeBody.y)
            if len(xy[bodies.index(snakeBody)]) == 4:
                del xy[bodies.index(snakeBody)][:2]

        for i in range(len(xy)):
            if xy[i][0] == food_x and xy[i][1] == food_y:
                ex_x = 24 - (xy[i][0] // 20)
                ex_y = 24 - (xy[i][1] // 20)

                exception_x.append(ex_x)
                exception_y.append(ex_y)

        if len(exception_x) > 0 and len(exception_y) > 0:
            a = choice([i for i in range(0, 25) if i not in exception_x])
            b = choice([i for i in range(0, 25) if i not in exception_y])

            food_x = 500 - a * 20 - 20
            food_y = 500 - b * 20 - 20

        food = snack(food_x, food_y)
        foods.append(food)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and not down:
        up = True
        down = left = right = False
    elif keys[pygame.K_DOWN] and not up:
        down = True
        up = left = right = False
    elif keys[pygame.K_LEFT] and not right:
        left = True
        up = down = right = False
    elif keys[pygame.K_RIGHT] and not left:
        right = True
        up = down = left = False

    if up:
        direction = 0
        snakeHead.y -= snakeHead.vel
        if snakeHead.y < 0:
            snakeHead.y += 500
    elif down:
        direction = 1
        snakeHead.y += snakeHead.vel
        if snakeHead.y == 500:
            snakeHead.y -= 500
    elif left:
        direction = 2
        snakeHead.x -= snakeHead.vel
        if snakeHead.x < 0:
            snakeHead.x += 500
    elif right:
        direction = 3
        snakeHead.x += snakeHead.vel
        if snakeHead.x == 500:
            snakeHead.x -= 500

    if snakeHead.x == food.x and snakeHead.y == food.y and food in foods and len(bodies) == 0:
        if len(bodies) == 0:
            foods.remove(food)
            score += 1
            mem.append([])
            xy.append([])
            if up:
                bodies.append(body(snakeHead.x, snakeHead.y + 20))
            elif down:
                bodies.append(body(snakeHead.x, snakeHead.y - 20))
            elif left:
                bodies.append(body(snakeHead.x + 20, snakeHead.y))
            elif right:
                bodies.append(body(snakeHead.x - 20, snakeHead.y))

    for snakeBody in bodies:
        if oneLoop == 1:
            if up:
                mem[0].append(0)
            elif down:
                mem[0].append(1)
            elif left:
                mem[0].append(2)
            elif right:
                mem[0].append(3)
            oneLoop += 1
        else:
            if mem[bodies.index(snakeBody) - 1][0] == 0:
                mem[bodies.index(snakeBody)].append(0)
            elif mem[bodies.index(snakeBody) - 1][0] == 1:
                mem[bodies.index(snakeBody)].append(1)
            elif mem[bodies.index(snakeBody) - 1][0] == 2:
                mem[bodies.index(snakeBody)].append(2)
            elif mem[bodies.index(snakeBody) - 1][0] == 3:
                mem[bodies.index(snakeBody)].append(3)

    oneLoop = 1

    if len(mem) > 0:
        if len(mem[0]) == 2:
            for snakeBody in bodies:
                if oneLoop == 1:
                    if mem[0][0] == 0:
                        snakeBody.y -= snakeBody.vel
                        if snakeBody.y < 0:
                            snakeBody.y += 500
                    elif mem[0][0] == 1:
                        snakeBody.y += snakeBody.vel
                        if snakeBody.y == 500:
                            snakeBody.y -= 500
                    elif mem[0][0] == 2:
                        snakeBody.x -= snakeBody.vel
                        if snakeBody.x < 0:
                            snakeBody.x += 500
                    elif mem[0][0] == 3:
                        snakeBody.x += snakeBody.vel
                        if snakeBody.x == 500:
                            snakeBody.x -= 500

                    oneLoop += 1

                    if snakeHead.x == food.x and snakeHead.y == food.y and food in foods:
                        if len(bodies) < 2:
                            foods.remove(food)
                            score += 1
                            mem.append([])
                            xy.append([])
                            if mem[pos][0] == 0 or mem[pos][0] == 1 or mem[pos][0] == 2 or mem[pos][0] == 3:
                                bodies.append(body(bodies[-1].x, bodies[-1].y))
                                pos += 1
                    mem[0].pop(0)

        oneLoop = 1

        for snakeBody in bodies:
            if len(mem[bodies.index(snakeBody)]) == 2:
                if mem[bodies.index(snakeBody)][0] == 0:
                    snakeBody.y -= snakeBody.vel
                    if snakeBody.y < 0:
                        snakeBody.y += 500
                elif mem[bodies.index(snakeBody)][0] == 1:
                    snakeBody.y += snakeBody.vel
                    if snakeBody.y == 500:
                        snakeBody.y -= 500
                elif mem[bodies.index(snakeBody)][0] == 2:
                    snakeBody.x -= snakeBody.vel
                    if snakeBody.x < 0:
                        snakeBody.x += 500
                elif mem[bodies.index(snakeBody)][0] == 3:
                    snakeBody.x += snakeBody.vel
                    if snakeBody.x == 500:
                        snakeBody.x -= 500

                if snakeHead.x == food.x and snakeHead.y == food.y and food in foods and len(bodies) >= 3:
                    foods.remove(food)
                    score += 1
                    mem.append([])
                    xy.append([])
                    if mem[pos][0] == 0:
                        bodies.append(body(bodies[-1].x, bodies[-1].y - 20))
                    if mem[pos][0] == 1:
                        bodies.append(body(bodies[-1].x, bodies[-1].y + 20))
                    if mem[pos][0] == 2:
                        bodies.append(body(bodies[-1].x - 20, bodies[-1].y))
                    if mem[pos][0] == 3:
                        bodies.append(body(bodies[-1].x + 20, bodies[-1].y))
                    pos += 1

                if snakeHead.x == food.x and snakeHead.y == food.y and food in foods:
                    foods.remove(food)
                    score += 1
                    mem.append([])
                    xy.append([])
                    if mem[pos][0] == 0 or mem[pos][0] == 1 or mem[pos][0] == 2 or mem[pos][0] == 3:
                        bodies.append(body(bodies[-1].x, bodies[-1].y))
                        pos += 1

                mem[bodies.index(snakeBody)].pop(0)

            if snakeBody.x == snakeHead.x and snakeBody.y == snakeHead.y:
                run = False

    redrawGameWindow()

checkHighScore()
pygame.quit()
messagebox.showinfo("Game Over", f"Score: {score} \nHigh Score: {outputHighScore()}")
