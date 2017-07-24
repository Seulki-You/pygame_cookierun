import pygame
from pygame.locals import *
import math
import random

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width,height))
keys = [False, False, False, False]
playerPos = [100, 100]
acc = [0, 0]
arrows = []

badTimer = 100
badTimer1 = 0
badGuys = [[640, 100]]
healthValue = 194


player = pygame.image.load('resources/images/dude.png')
grass = pygame.image.load('resources/images/grass.png')
castle = pygame.image.load('resources/images/castle.png')
arrow = pygame.image.load('resources/images/bullet.png')
badGuyImg = pygame.image.load('resources/images/badguy.png')
healthBar = pygame.image.load('resources/images/healthbar.png')
health = pygame.image.load('resources/images/health.png')

while True:
    badTimer -= 1
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        if event.type == MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1] - (playerPos1[1]+32), position[0] - (playerPos1[0]+26)), playerPos1[0] + 32, playerPos1[1] + 32])
        if event.type == KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            if event.key == K_a:
                keys[1] = True
            if event.key == K_s:
                keys[2] = True
            if event.key == K_d:
                keys[3] = True
        if event.type == KEYUP:
            if event.key == K_w:
                keys[0] = False
            if event.key == K_a:
                keys[1] = False
            if event.key == K_s:
                keys[2] = False
            if event.key == K_d:
                keys[3] = False

    # 캐릭터 위치 조정
    if keys[0]:
        playerPos[1] -= 5
    elif keys[2]:
        playerPos[1] += 5
    if keys[1]:
        playerPos[0] -= 5
    elif keys[3]:
        playerPos[0] += 5

    # 배경을 검정색으로
    screen.fill((0, 0, 0))

    # 배경을 잡초로 채워주기
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass, (x*grass.get_width(), y*grass.get_height()))

    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    screen.blit(healthBar, (5, 5))
    for health1 in range(healthValue):
        screen.blit(health, (health1+8, 8))

    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerPos[1]+32), position[0] - (playerPos[0]+26))
    playerRot = pygame.transform.rotate(player, 360-angle*57.29)
    playerPos1 = (playerPos[0] - playerRot.get_rect().width/2, playerPos[1] - playerRot.get_rect().height/2)

    for bullet in arrows:
        arrow1 = pygame.transform.rotate(arrow, 360-bullet[0]*57.29)
        screen.blit(arrow1, (bullet[1], bullet[2]))

        velX = math.cos(bullet[0])*10
        velY = math.sin(bullet[0])*10
        bullet[1] += velX
        bullet[2] += velY

        # 화면에서 벗어나는 화살 제거
        if bullet[1] < -64 or bullet[1] > 640 or bullet[2] < -64 or bullet[2] > 480:
            arrows.remove(bullet)
        #arrow이미지의 정보가 저장되어 있다.
        bulletRect = pygame.Rect(arrow.get_rect())
        bulletRect.left = bullet[1]
        bulletRect.top = bullet[2]
        for badGuy in badGuys:
            badGuyRect = pygame.Rect(badGuyImg.get_rect())
            badGuyRect.left = badGuy[0]
            badGuyRect.top = badGuy[1]
            if badGuyRect.colliderect(bulletRect):
                acc[0] += 1
                badGuys.remove(badGuy)
                arrows.remove(bullet)

    # 적군 그리기
    for badGuy in badGuys:
        screen.blit(badGuyImg, badGuy)
        # x좌표 이동
        badGuy[0] -= 5
        if badGuy[0] < 64:
            badGuys.remove(badGuy)
            healthValue -= 8

    if badTimer == 0:
        badGuys.append([640, random.randint(50, 430)])
        badTimer = 100

    screen.blit(playerRot, playerPos1)

    pygame.display.flip()
