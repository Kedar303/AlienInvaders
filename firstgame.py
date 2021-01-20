import pygame as py
import random as r
import math
from pygame import mixer

# intialize
k = py.init()
# window
win = py.display.set_mode((800, 700))  # width,height of window
# bg = py.image.load('1.jpg')
# title and icon
tit = py.display.set_caption("My first game")
# icon = py.image.load('name.png')
# py.display.set_icon(icon)
# Game loop
# PLAYER
# background music
mixer.music.load('background.wav')
mixer.music.play(-1)

player_img = py.image.load('space-invaders (1).png')
playerX = 360
playerY = 600
playerX_change = 0

# ENEMY
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_img.append(py.image.load('alien.png'))
    enemyX.append(r.randint(0, 700))
    enemyY.append(r.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(50)

# BULLET
bullet_img = py.image.load('bullet.png')
bulletX = 0
bulletY = 600
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

# SCORE
score_value = 0
font = py.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
#f = py.font.Font('freesansbold.ttf', 300)


def game_over():
    s = font.render("GAME OVER", True, (255, 255, 255))
    win.blit(s, (300, 350))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def player(x, y):
    win.blit(player_img, (x, y))  # to draw image on the screen


def enemy(x, y, i):
    win.blit(enemy_img[i], (x, y))  # to draw image on the screen


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    win.blit(bullet_img, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):  # (x1,x2,y1,y2)
    distance = math.sqrt((math.pow(enemyX - bulletX, 2))) + (
    (math.pow(enemyY - bulletY, 2)))  # formula whole sqrt of (x2-x1) the whole sq  + (y2-y1) whole sq
    if distance < 27:
        return True
    return False


running = True
while running:
    win.fill((0, 255, 255))  # background color i.e cyan

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

        # for keyboard controls
        if event.type == py.KEYDOWN:  # checks if any key is pressed
            if event.key == py.K_LEFT:
                playerX_change = -0.5  # to move to left

            if event.key == py.K_RIGHT:
                playerX_change = 0.5  # to move right

            if event.key == py.K_SPACE:
                if bullet_state == "ready":
                    k = mixer.Sound('laser.wav')
                    k.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == py.KEYUP:
            if event.key == py.K_LEFT or event.key == py.K_RIGHT:
                playerX_change = 0  # to stop when key is not pressed

    # player movement
    playerX += playerX_change
    # not allowed to go out of the boundary
    if playerX <= 0:  # for left boundary
        playerX = 0
    if playerX > 736:  # for right boundary
        playerX = 736

    # enemy movement
    for i in range(no_of_enemies):
        if enemyY[i] > 550: #pixel limit ,after this pixel get hit by enemy game will be over
            for j in range(no_of_enemies):# for all the enemy that's why for loop is used
                enemyY[j] = 2000 #after hitting all the enemies will go to 2000th pixel that means it will disappera from screen
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        # not allowed to go out of the boundary
        if enemyX[i] <= 0:  # for left boundary
            enemyX_change[i] = 0.5  # when hit left boundary, enemy will be travel back towards right direction
            enemyY[i] += enemyY_change[i] # when hit enemy comes down
        elif enemyX[i] >= 736:  # for right boundary
            enemyX_change[i] = -0.5  # when hit right boundary, enemy will be travel back towards left direction
            enemyY[i] += enemyY_change[i]# when hit enemy comes down

        # COLLISION
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            w = mixer.Sound('explosion.wav')
            w.play()
            bulletY = 600  # after collision bullet will again return to its original place
            bullet_state = "ready"
            score_value += 1



            enemyX[i] = r.randint(0, 636)  # to again respawn the enemy after getting hit
            enemyY[i] = r.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # BULLET movement
    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"
    if bullet_state is "fire":
        bulletY -= bulletY_change  # to travel bullet in upwards direction bullet
        fire_bullet(bulletX, bulletY)

    player(playerX, playerY)
    show_score(textX, textY)

    py.display.update()  # to update our game screen
