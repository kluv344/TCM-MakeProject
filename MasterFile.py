# Coronavirus Fight

import pygame
import os
import random
import time

# Initialize the game screen
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rona Rambo")

# Load images
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))
player = pygame.image.load("mdoctor.png")
virus = pygame.image.load("rona.png")
virus = pygame.transform.scale(virus, (100, 75))


#Right going Left Coronas
class Coronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health

    def draw(self, screen):
        screen.blit(virus, (self.x, self.y))

    def move(self):
        self.x = self.x + 3
        if self.x > width:
            self.x = -130
            self.y = random.randint(0, 500)

#Left going Right Coronas
class LeftCoronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health

    def drawleft(self, screen):
        screen.blit(virus, (self.x, self.y))

    def moveleft(self):
        self.x = self.x - 3
        if self.x < 0:
            self.x = width + 50
            self.y = random.randint(0, 500)



# Main Game
def main():
    running = True
    FPS = 50
    clock = pygame.time.Clock()
    enemies = []
    enemiesleft = []
    wave_length = 1

    # Update Screen
    def redraw_window():
        screen.blit(background, (0, 0))
        screen.blit(player, (width / 2, height / 2 - 20))

        for rona in enemies:
            rona.draw(screen)
        for ronaleft in enemiesleft:
            ronaleft.drawleft(screen)

        pygame.display.update()

    while running:
        clock.tick(FPS)
        redraw_window()
        rona = Coronavirus(0, 100)
        rona.draw(screen)
        leftrona= LeftCoronavirus(width,100)
        leftrona.drawleft(screen)
        for enemy in enemies:
            enemy.move()
        for leftenemy in enemiesleft:
            leftenemy.moveleft()


        if len(enemies) == 0:
            wave_length += 2
            for i in range(wave_length):
                rona2 = Coronavirus(random.randint(-800, -150),random.randint(10, 500)) #instance of Coronavirus class
                enemies.append(rona2)
        if len(enemiesleft) == 0:
            wave_length += 1
            for i in range(wave_length):
                rona3 = LeftCoronavirus(random.randint(width,1800),random.randint(10, 500)) #instance of Coronavirus class
                enemiesleft.append(rona3)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

main()
