import pygame
from pygame.locals import *
import math
import random



class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('cookie.png')
        self.image = pygame.transform.scale(self.image, (140, 140))
        self.position = 200, 450
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.running = 2
        self.jumpingV = 20
        self.jumping = False
        self.slideCheck = False

    def afterSlideShape(self):
        self.image = pygame.image.load('cookie.png')
        self.image = pygame.transform.scale(self.image, (140, 140))
        self.position = 200, 450
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def playing(self):
        if not self. jumping and not self.slideCheck:
            #print('playing')
            self.position = self.position[0], self.position[1] - self.running
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if self.position[1] == 440 or self.position[1] == 460:
                self.running = -self.running
            #print(self.running)

    def jump(self):
        if self.jumping:
            self.position = self.position[0], self.position[1] - self.jumpingV
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            if 200 <= self.position[1] <= 220:
                self.jumpingV = - self.jumpingV
            if self.position[1] >= 450:
                self.position = self.position[0], 450
                self.jumpingV = 20
                self.jumping = False


    def slide(self):
        if self.slideCheck:
            self.image = pygame.image.load('cookieslide.png')
            self.image = pygame.transform.scale(self.image, (140,70))
            self.position = self.position[0], 485
            self.rect = self.image.get_rect()
            self.rect.center = self.position


    def update(self):
        self.jump()
        self.playing()
        self.slide()

class Jelly(pygame.sprite.Sprite):
    number = 0
    sin = False
    def __init__(self, positionY):
        super().__init__()
        Jelly.number +=1
        self.image = pygame.image.load('jelly.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.position = 1100, positionY
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.running = 20

    def move(self):
        self.position = self.position[0] - self.running, self.position[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class ObstacleBottom(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image = pygame.image.load('obstacle1.png')
        self.image = pygame.transform.scale(self.image, (70, 100))
        self.position = 975, 475
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.running = 20
        self.checkCollid = 0

    def move(self):
        self.position = self.position[0] - self.running, self.position[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

class ObstacleTop(ObstacleBottom):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('obstacle2.png')
        self.image = pygame.transform.scale(self.image, (70, 150))
        self.position = 975, -75
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.downV = 15


    def move(self):
        super().move()
        self.down()

    def down(self):
        if self.position[1] <= 75:
            self.position = self.position[0], self.position[1] + self.downV
            self.rect = self.image.get_rect()
            self.rect.center = self.position


pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()
controlTime = 0

player = Cookie()
#playerRect = pygame.Rect(player.rect)

jellys = [Jelly(500)]
obstacles_bottom = []
obstacles_top = []


#게임 배경
backgroundImg = pygame.image.load('background.png')
backgroundImg = pygame.transform.scale(backgroundImg, (1200, 600))
background = 0
background2 = 1200


while True:
    deltat = clock.tick(60)
    #controlTime += 1
    #이벤트 처리
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit(0)
        if hasattr(event, 'key'):
            down = event.type == KEYDOWN
            up = event.type == KEYUP
            if event.key == K_UP:
                player.jumping = True
            if down and event.key == K_DOWN:
                player.slideCheck = True
            if up and event.key == K_DOWN:
                player.slideCheck = False
                player.afterSlideShape()

    #배경 그리기
    background -= 5
    background2 -= 5
    if background == - 1200:
        background = 1200
    if background2 == -1200:
        background2 = 1200
    screen.blit(backgroundImg, (background, 0))
    screen.blit(backgroundImg, (background2, 0))

    #게임 캐릭터 그리기
    player.update()
    screen.blit(player.image, player.rect)

    for jelly in jellys:
        print(jelly.position[1])
        playerRect = pygame.Rect(player.rect)
        jelly.move()
        jellyRect = pygame.Rect(jelly.rect)
        if jellyRect.colliderect(playerRect):
            jellys.remove(jelly)
        if jelly.position[0] < 10:
            jellys.remove(jelly)
        if jelly.position[0] == 1000:
            if not jelly.sin:
                jellys.append(Jelly(500))
            else:
                jellys.append(Jelly(jelly.position[1] - 100*math.sin((jelly.number % 13))))
                if jelly.position[1] < 311:
                    obstacles_bottom.append(ObstacleBottom())
                if jelly.position[1] < 500:
                    print('돼?')
                    obstacles_top.append(ObstacleTop())
            if jelly.number % 13 == 0:
                if not Jelly.sin:
                    Jelly.sin = True
                else:
                    Jelly.sin = False

        screen.blit(jelly.image, jelly.rect)

    for obstacle in obstacles_bottom:
        playerRect = pygame.Rect(player.rect)
        obstacle.move()
        obstacleRect = pygame.Rect(obstacle.rect)
        if playerRect.colliderect(obstacleRect):
            obstacle.checkCollid += 1
            if obstacle.checkCollid >= 6:
                print('충돌')
        if obstacle.position[0] < 10:
            obstacles_bottom.remove(obstacle)

        screen.blit(obstacle.image, obstacle.rect)

    for obstacle in obstacles_top:
        obstacle.move()
        screen.blit(obstacle.image, obstacle.rect)

    pygame.display.flip()