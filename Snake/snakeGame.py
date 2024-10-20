import pygame
import random


pygame.init()

# Width and height must be multiples of 20
WIDTH = 500
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

head_images = [pygame.image.load("snake_up.jpg"),
               pygame.image.load("snake_right.jpg"),
               pygame.image.load("snake_down.jpg"),
               pygame.image.load("snake_left.jpg")]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, direction):
        if direction == 0:
            self.y -= 20
            if self.y < 0:
                self.y += HEIGHT
        elif direction == 1:
            self.x += 20
            if self.x == WIDTH:
                self.x -= WIDTH
        elif direction == 2:
            self.y += 20
            if self.y == HEIGHT:
                self.y -= HEIGHT
        else:
            self.x -= 20
            if self.x < 0:
                self.x += WIDTH


class Head(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, window, direction):
        window.blit(head_images[direction], (self.x, self.y))


class Body(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, window):
        pygame.draw.rect(window, (199, 6, 7), (self.x, self.y, 20, 20))


class Snack(Point):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, window):
        pygame.draw.rect(window, (51, 204, 51), (self.x, self.y, 20, 20))


def readKeys(keys, direction):
    if keys[pygame.K_UP] and direction != 2:
        direction = 0
    elif keys[pygame.K_RIGHT] and direction != 3:
        direction = 1
    elif keys[pygame.K_DOWN] and direction != 0:
        direction = 2
    elif keys[pygame.K_LEFT] and direction != 1:
        direction = 3

    return direction


def createNextBody(prev_x, prev_y, direction):
    if direction == 0:
        return Body(prev_x, prev_y + 20)
    elif direction == 1:
        return Body(prev_x - 20, prev_y)
    elif direction == 2:
        return Body(prev_x, prev_y - 20)
    else:
        return Body(prev_x + 20, prev_y)


def checkDelay(length):
    if length < 10:
        return 100
    elif length < 30:
        return 80
    elif length < 50:
        return 70
    elif length < 70:
        return 60
    elif length < 100:
        return 55


def checkHighScore(score):
    file = open("highscore.txt")
    if score > int(file.read()):
        file = open("highscore.txt", "w")
        file.write(str(score))
    file.close()


def outputHighScore(score):
    from tkinter import messagebox
    file = open("highscore.txt")
    highscore = file.read()
    file.close()
    messagebox.showinfo("Game Over", f"Score: {score} \nHigh Score: {highscore}")


def main():
    head = Head(random.randint(1, WIDTH // 20 - 1) * 20, random.randint(1, HEIGHT // 20 - 1) * 20)
    food = Snack(random.choice([i for i in range(0, WIDTH, 20) if i != head.x]),
                 random.choice([i for i in range(0, HEIGHT, 20) if i != head.y]))
    direction = random.randint(0, 3)
    delay = 80
    score = 0
    bodies = []
    memory = [direction]
    exceptions_x = [head.x]
    exceptions_y = [head.y]
    ended_manually = False
    game_running = True

    while game_running:
        pygame.time.delay(delay)

        # Closes game if user clicks on close button (X) in top right corner of window or if user presses Q
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                game_running = False
                ended_manually = True

        # Check if food is eaten
        if food.x == head.x and food.y == head.y:
            score += 1
            del food

            # Update coordinate exceptions for food
            exceptions_x[0] = head.x
            exceptions_y[0] = head.y
            for i in range(len(bodies)):
                exceptions_x[i + 1] = bodies[i].x
                exceptions_y[i + 1] = bodies[i].y

            food = Snack(random.choice([i for i in range(0, WIDTH, 20) if i not in exceptions_x]),
                         random.choice([i for i in range(0, HEIGHT, 20) if i not in exceptions_y]))

            # Make snake longer
            if len(bodies) > 0:
                bodies.append(createNextBody(bodies[-1].x, bodies[-1].y, memory[-1]))
            else:
                bodies.append(createNextBody(head.x, head.y, memory[-1]))

            exceptions_x.append(bodies[-1].x)
            exceptions_y.append(bodies[-1].y)
            memory.append(memory[-1])

        # Set first index in memory of directions to direction of head
        memory[0] = direction

        # Read keys pressed by user and update direction
        direction = readKeys(pygame.key.get_pressed(), direction)

        # Move snake's head and body
        head.move(direction)
        for i in range(len(bodies)):
            # Check if snake hits itself
            if head.x == bodies[i].x and head.y == bodies[i].y:
                game_running = False

            # Move snake body
            bodies[i].move(memory[i])

        # Decrease delay of game (increase snake speed) as snake gets longer
        delay = checkDelay(len(bodies))

        # Update memory of directions
        for i in range(1, len(memory)):
            memory[-i] = memory[-i - 1]

        # Redraw window
        window.fill((22, 22, 24))
        food.draw(window)
        head.draw(window, direction)
        for body in bodies:
            body.draw(window)
        pygame.display.update()

    # Doesn't display score and highscore if user ends game manually
    if not ended_manually:
        checkHighScore(score)
        outputHighScore(score)

    pygame.quit()


if __name__ == "__main__":
    main()
