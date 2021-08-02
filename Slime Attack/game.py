import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 799, 469

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("EPIC Fighting Game")

BG = pygame.image.load('bg.jpg')

# Images for the animations of the player
idle = [pygame.image.load('Sprites/adventurer-idle-00.png'), pygame.image.load('Sprites/adventurer-idle-01.png'),
        pygame.image.load('Sprites/adventurer-idle-02.png'), pygame.image.load('Sprites/adventurer-idle-03.png')]
# idle = [pygame.image.load('Sprites/adventurer-idle-2-00.png'), pygame.image.load('Sprites/adventurer-idle-2-01.png'),
#         pygame.image.load('Sprites/adventurer-idle-2-02.png'), pygame.image.load('Sprites/adventurer-idle-2-03.png')]
runRight = [pygame.image.load('Sprites/adventurer-run-00.png'), pygame.image.load('Sprites/adventurer-run-01.png'),
            pygame.image.load('Sprites/adventurer-run-02.png'), pygame.image.load('Sprites/adventurer-run-03.png'),
            pygame.image.load('Sprites/adventurer-run-04.png'), pygame.image.load('Sprites/adventurer-run-05.png')]
runLeft = [pygame.image.load('Sprites/adventurer-run-left-00.png'), pygame.image.load('Sprites/adventurer-run-left-01.png'),
           pygame.image.load('Sprites/adventurer-run-left-02.png'), pygame.image.load('Sprites/adventurer-run-left-03.png'),
           pygame.image.load('Sprites/adventurer-run-left-04.png'), pygame.image.load('Sprites/adventurer-run-left-05.png')]
slideRight = [pygame.image.load('Sprites/adventurer-slide-00.png'), pygame.image.load('Sprites/adventurer-slide-01.png')]
slideLeft = [pygame.image.load('Sprites/adventurer-slide-left-00.png'), pygame.image.load('Sprites/adventurer-slide-left-01.png')]
attack1Right = [pygame.image.load('Sprites/adventurer-attack1-00.png'), pygame.image.load('Sprites/adventurer-attack1-01.png'),
                pygame.image.load('Sprites/adventurer-attack1-02.png'), pygame.image.load('Sprites/adventurer-attack1-03.png'),
                pygame.image.load('Sprites/adventurer-attack1-04.png')]
attack1Left = [pygame.image.load('Sprites/adventurer-attack1-left-00.png'), pygame.image.load('Sprites/adventurer-attack1-left-01.png'),
               pygame.image.load('Sprites/adventurer-attack1-left-02.png'), pygame.image.load('Sprites/adventurer-attack1-left-03.png'),
               pygame.image.load('Sprites/adventurer-attack1-left-04.png')]
dieRight = [pygame.image.load('Sprites/adventurer-die-00.png'), pygame.image.load('Sprites/adventurer-die-01.png'), 
            pygame.image.load('Sprites/adventurer-die-02.png'), pygame.image.load('Sprites/adventurer-die-03.png'), 
            pygame.image.load('Sprites/adventurer-die-04.png'), pygame.image.load('Sprites/adventurer-die-05.png'), 
            pygame.image.load('Sprites/adventurer-die-06.png')]

# Images for the animations of the slime
slimeMoveRight = [pygame.image.load('Sprites/slime-move-00.png'), pygame.image.load('Sprites/slime-move-01.png'),
                  pygame.image.load('Sprites/slime-move-02.png'), pygame.image.load('Sprites/slime-move-03.png')]
slimeMoveLeft = [pygame.image.load('Sprites/slime-move-left-00.png'), pygame.image.load('Sprites/slime-move-left-01.png'),
                 pygame.image.load('Sprites/slime-move-left-02.png'), pygame.image.load('Sprites/slime-move-left-03.png')]
slimeDieRight = [pygame.image.load('Sprites/slime-die-00.png'), pygame.image.load('Sprites/slime-die-01.png'),
                 pygame.image.load('Sprites/slime-die-02.png'), pygame.image.load('Sprites/slime-die-03.png')]
slimeDieLeft = [pygame.image.load('Sprites/slime-die-left-00.png'), pygame.image.load('Sprites/slime-die-left-01.png'),
                pygame.image.load('Sprites/slime-die-left-02.png'), pygame.image.load('Sprites/slime-die-left-03.png')]
slimeAttackRight = [pygame.image.load('Sprites/slime-attack-00.png'), pygame.image.load('Sprites/slime-attack-01.png'), 
                    pygame.image.load('Sprites/slime-attack-02.png'), pygame.image.load('Sprites/slime-attack-03.png'), 
                    pygame.image.load('Sprites/slime-attack-04.png')]
slimeAttackLeft = [pygame.image.load('Sprites/slime-attack-left-00.png'), pygame.image.load('Sprites/slime-attack-left-01.png'), 
                   pygame.image.load('Sprites/slime-attack-left-02.png'), pygame.image.load('Sprites/slime-attack-left-03.png'), 
                   pygame.image.load('Sprites/slime-attack-left-04.png')]

# Images for the potions
potionImageGreen = pygame.image.load('Sprites/potion-green.png')
potionImageRed = pygame.image.load('Sprites/potion-red.png')

# File for the Background Music
music = pygame.mixer.music.load('Sounds/BGMusic.mp3')
pygame.mixer.music.play(-1)


class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.idle = True
        self.idleCount = 0
        self.right = False
        self.left = False
        self.walkCount = 0
        self.jump = False
        self.jumpCount = 9
        self.slide = False
        self.slideCount = 0
        self.attack = False
        self.attackCount = 0
        self.attackSpeed = 10
        self.hitbox = (self.x + 40, self.y + 17, 70, 94)
        self.attackHitbox = (-10, -10, 0, 0)
        self.showHitbox = False
        self.strength = 2
        self.LP = 50
        self.kill = False
        self.killCount = 0
        self.killSpeed = 35

    def draw(self, window):
        if self.walkCount + 1 == speed:
            self.walkCount = 0
        if self.slideCount + 1 == speed:
            self.slideCount = 0
        if self.idleCount + 1 == speed:
            self.idleCount = 0
        if self.attackCount + 1 == self.attackSpeed:
            self.attackCount = 0
            self.attack = False

        if self.attack and (self.right or self.idle):
            window.blit(attack1Right[self.attackCount // (self.attackSpeed // len(attack1Right))], (int(self.x), int(self.y)))
            if self.attackCount // (self.attackSpeed // len(attack1Right)) == 2:
                charDamageEnemyRight()
            self.attackCount += 1
            self.hitbox = (self.x + 42, self.y + 25, 60, 85)
        elif self.attack and self.left:
            window.blit(attack1Left[self.attackCount // (self.attackSpeed // len(attack1Left))], (int(self.x), int(self.y)))
            if self.attackCount // (self.attackSpeed // len(attack1Right)) == 2:
                charDamageEnemyLeft()
            self.attackCount += 1
            self.hitbox = (self.x + 44, self.y + 25, 61, 85)
        elif self.idle:
            window.blit(idle[self.idleCount // (speed // len(idle))], (int(self.x), int(self.y)))
            self.idleCount += 1
            self.hitbox = (self.x + 45, self.y + 17, 56, 94)
        elif self.slide and self.right:
            window.blit(slideRight[self.slideCount // (speed // len(slideRight))], (int(self.x), int(self.y)))
            self.slideCount += 1
            self.hitbox = (self.x + 41, self.y + 62, 78, 50)
        elif self.slide and self.left:
            window.blit(slideLeft[self.slideCount // (speed // len(slideLeft))], (int(self.x), int(self.y)))
            self.slideCount += 1
            self.hitbox = (self.x + 31, self.y + 62, 78, 50)
        elif self.right:
            window.blit(runRight[self.walkCount // (speed // len(runRight))], (int(self.x), int(self.y)))
            self.walkCount += 1
            self.hitbox = (self.x + 58, self.y + 24, 56, 86)
        elif self.left:
            window.blit(runLeft[self.walkCount // (speed // len(runLeft))], (int(self.x), int(self.y)))
            self.walkCount += 1
            self.hitbox = (self.x + 34, self.y + 22, 56, 88)

        if self.attack and (self.right or self.idle):
            self.attackHitbox = (self.x + 62, self.y, 88, 111)
        elif self.attack and self.left:
            self.attackHitbox = (self.x, self.y, 90, 111)
        else:
            self.attackHitbox = (-10, -10, 0, 0)

        if self.showHitbox:
            pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
            pygame.draw.rect(window, (0, 128, 0), self.attackHitbox, 2)

        pygame.draw.rect(window, (255, 0, 0), (int(self.hitbox[0] + 5), int(self.hitbox[1] - 15), 50, 10))
        pygame.draw.rect(window, (0, 128, 0), (int(self.hitbox[0] + 5), int(self.hitbox[1] - 15), self.LP, 10))


def charMovement():
    keys = pygame.key.get_pressed()
    leftBorder = -35
    rightBorder = WIDTH - player.width + 40

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.right = True
        player.left = player.idle = False
        if player.x < rightBorder:
            player.x += player.vel
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.left = True
        player.right = player.idle = False
        if player.x > leftBorder:
            player.x -= player.vel
    else:
        player.idle = True
        player.right = player.left = False


def charSlide():
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and (player.right or player.left):
        player.slide = True
        player.vel = 7
    elif not keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.slide = False
        player.vel = 5


def charJump():
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jump:
        player.jump = True
    elif player.jump:
        if player.jumpCount >= -9:
            neg = 1
            if player.jumpCount < 0:
                neg = -1
            player.y -= (player.jumpCount ** 2) * 0.5 * neg
            player.jumpCount -= 1
        else:
            player.jump = False
            player.jumpCount = 9


def charAttack1():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        player.attack = True


def charDamageEnemyRight():
    for slime in slimes:
        if not slime.kill:
            if player.attack and slime.hitbox[0] + slime.hitbox[2] >= player.hitbox[0] + player.hitbox[2] >= slime.hitbox[0] and player.hitbox[1] + player.hitbox[3] >= slime.hitbox[1]:
                slime.LP -= player.strength

        if slime.LP <= 0:
            slime.kill = True


def charDamageEnemyLeft():
    for slime in slimes:
        if not slime.kill:
            if player.attack and slime.hitbox[0] <= player.hitbox[0] <= slime.hitbox[0] + slime.hitbox[2] and player.hitbox[1] + player.hitbox[3] >= slime.hitbox[1]:
                slime.LP -= player.strength

        if slime.LP <= 0:
            slime.kill = True


def charDeathAnimation(window):
    if player.killCount + 1 < player.killSpeed:
        player.x = 310
        window.blit(dieRight[player.killCount // (player.killSpeed // len(dieRight))], (int(player.x), int(player.y)))
        player.killCount += 1


def charDeath(window):
    global countdown

    if player.kill and player.killCount + 1 >= player.killSpeed:
        font = pygame.font.SysFont('agencyfb', 60)
        text = font.render('Game Over', 1, (0, 0, 0))
        window.blit(text, (300, 110))
        countdown -= 1

    if countdown == 0:
        time.sleep(1)
        pygame.quit()
        quit()


class Enemy:
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3
        if direction == 1:
            self.right = True
            self.left = False
        else:
            self.right = False
            self.left = True
        self.moveCount = 0
        self.hitbox = (self.x + 3, self.y + 34, 83, 41)
        self.showHitbox = False
        self.strength = 2
        self.attack = False
        self.attackCount = 0
        self.attackSpeed = 10
        self.LP = 10
        self.kill = False
        self.killCount = 0
        self.visible = True

    def draw(self, window):
        global score

        if self.killCount + 1 == speed:
            self.killCount = 0

        if not self.kill:
            if self.moveCount + 1 == speed:
                self.moveCount = 0
            if self.attackCount + 1 == self.attackSpeed:
                self.attack = False
                self.attackCount = 0

            if self.right and self.attack:
                window.blit(slimeAttackRight[self.attackCount // (self.attackSpeed // len(slimeAttackRight))], (self.x, self.y))
                self.attackCount += 1
            elif self.left and self.attack:
                window.blit(slimeAttackLeft[self.attackCount // (self.attackSpeed // len(slimeAttackLeft))], (self.x, self.y))
                self.attackCount += 1
            elif self.right:
                window.blit(slimeMoveRight[self.moveCount // (speed // len(slimeMoveRight))], (self.x, self.y))
            elif self.left:
                window.blit(slimeMoveLeft[self.moveCount // (speed // len(slimeMoveLeft))], (self.x, self.y))

            self.moveCount += 1

            self.hitbox = (self.x + 3, self.y + 34, 83, 41)
            if self.showHitbox:
                pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        elif self.kill and self.right:
            window.blit(slimeDieRight[self.killCount // (speed // len(slimeDieRight))], (self.x, self.y))
            self.killCount += 1
            if self.killCount // (speed // len(slimeDieRight)) == 3:
                self.visible = False
                score += 1
        elif self.kill and self.left:
            window.blit(slimeDieLeft[self.killCount // (speed // len(slimeDieLeft))], (self.x, self.y))
            self.killCount += 1
            if self.killCount // (speed // len(slimeDieLeft)) == 3:
                self.visible = False
                score += 1


def enemyMovement():
    for slime in slimes:
        rightBorder = WIDTH - slime.width + 30
        leftBorder = -20

        if slime.x + slime.width >= WIDTH or slime.x > player.x + player.width:
            slime.left = True
            slime.right = False
        elif slime.x <= 0 or slime.x + slime.width < player.x:
            slime.right = True
            slime.left = False

        if slime.right and slime.x < rightBorder:
            slime.x += slime.vel
        elif slime.left and slime.x > leftBorder:
            slime.x -= slime.vel


def enemyAttack():
    for slime in slimes:
        if slime.visible:
            if slime.hitbox[1] <= player.hitbox[1] + player.hitbox[3]:
                if slime.right and player.hitbox[0] - slime.vel <= slime.hitbox[0] + slime.hitbox[2] < player.hitbox[0]:
                    slime.attack = True
                    player.LP -= slime.strength
                elif slime.left and player.hitbox[0] + player.hitbox[2] + slime.vel >= slime.hitbox[0] > player.hitbox[0] + player.hitbox[2]:
                    slime.attack = True
                    player.LP -= slime.strength

    if player.LP <= 0:
        player.kill = True


def spawnEnemy():
    if roundsPassed < 750:
        frequency = 50
    elif 750 <= roundsPassed < 1500:
        frequency = 40
    else:
        frequency = 30

    if roundsPassed % frequency == 0:
        slimes.append(Enemy(random.randrange(0, WIDTH - 96), 306, 96, 75, random.randrange(1, 3)))


class Potion:
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.showHitbox = False
        self.healthBoost = 10

    def draw(self, window):
        if self.colour == 'green':
            window.blit(potionImageGreen, (self.x, self.y))
        elif self.colour == 'red':
            window.blit(potionImageRed, (self.x, self.y))

        if self.showHitbox:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)


def spawnPotion():
    if roundsPassed % 800 == 0 and roundsPassed > 0:
        potions.append(Potion(random.randrange(0, WIDTH - 30), random.randrange(180, 228), 28, 28, 'green'))
    if roundsPassed % 1600 == 0 and roundsPassed > 0:
        potions.append(Potion(random.randrange(0, WIDTH - 30), random.randrange(180, 228), 28, 28, 'red'))


def drinkPotion():
    for potion in potions:
        if player.right:
            if potion.x + potion.width >= player.hitbox[0] + player.hitbox[2] >= potion.x and player.hitbox[1] < potion.y + potion.height:
                if potion.colour == 'green':
                    boostHealth(potion)
                else:
                    startingRound = roundsPassed
                    boostStrength(startingRound)
                potions.remove(potion)
        elif player.left:
            if potion.x + potion.width >= player.hitbox[0] >= potion.x and player.hitbox[1] < potion.y + potion.height:
                if potion.colour == 'green':
                    boostHealth(potion)
                else:
                    startingRound = roundsPassed
                    boostStrength(startingRound)
                potions.remove(potion)
        else:
            if (potion.x + potion.width >= player.hitbox[0] >= potion.x and player.hitbox[1] < potion.y + potion.height) or (potion.x + potion.width >= player.hitbox[0] + player.hitbox[2] >= potion.x and player.hitbox[1] < potion.y + potion.height):
                if potion.colour == 'green':
                    boostHealth(potion)
                else:
                    startingRound = roundsPassed
                    boostStrength(startingRound)
                potions.remove(potion)


def boostHealth(potion):
    if player.LP <= 50 - potion.healthBoost:
        player.LP += potion.healthBoost
    else:
        player.LP += 50 - player.LP


def boostStrength(start):
    if roundsPassed <= start + 300:
        player.strength = 4


def drawScore(window):
    font = pygame.font.SysFont('agencyfb', 30)
    text = font.render('Score: ' + str(score), 1, (0, 0, 0))
    window.blit(text, (700, 10))


def drawHighScore(window):
    highscore = open('highscore.txt')
    font = pygame.font.SysFont('agencyfb', 30)
    text = font.render('Highscore: ' + highscore.read(), 1, (0, 0, 0))
    window.blit(text, (550, 10))
    highscore.close()


def changeHighScore():
    highscore = open('highscore.txt')
    if score > int(highscore.read()):
        highscore = open('highscore.txt', 'w')
        highscore.write(str(score))
    highscore.close()


def redrawWindow():
    WINDOW.blit(BG, (0, 0))
    drawScore(WINDOW)
    changeHighScore()
    drawHighScore(WINDOW)
    for slime in slimes:
        if slime.visible:
            slime.draw(WINDOW)

    if not player.kill:
        for regenPotion in potions:
            regenPotion.draw(WINDOW)
        player.draw(WINDOW)
    else:
        charDeathAnimation(WINDOW)
        charDeath(WINDOW)
    pygame.display.update()


player = Character(310, 270, 150, 111)              # Change x co-ordinate to 310 for player to be in the centre.
slimes = [Enemy(random.randrange(0, WIDTH - 96), 306, 96, 75, random.randrange(1, 3))]
potions = []
speed = 24
score = 0
roundsPassed = 0
countdown = 20

while True:
    CLOCK.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    if not player.kill:
        charMovement()
        charSlide()
        charJump()
        drinkPotion()
        charAttack1()

    spawnEnemy()
    enemyMovement()
    enemyAttack()

    spawnPotion()

    redrawWindow()
    roundsPassed += 1
