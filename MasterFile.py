# Person movement + coronas + shooting 1 at a time; No timer
## Coronavirus Fight

import pygame
import os
import random
import time

pygame.font.init()

# Initialize the game screen
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rona Rambo")

# Load images
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))
player = pygame.image.load("mdoctor.png")
player = pygame.transform.scale(player, (80, 250))
virus = pygame.image.load("rona.png")
virus = pygame.transform.scale(virus, (100, 75))
coin = pygame.image.load("coin.png")
coin = pygame.transform.scale(coin, (100, 75))
tizer = pygame.image.load("sanitizer.png")
tizer = pygame.transform.scale(tizer, (25, 35))


# Player Class
class Player(pygame.sprite.Sprite):  # represents the Nurse/player, not the game
    def __init__(self, x, y):
        """ The constructor of the class """
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        # the nurse's position
        self.x = x
        self.y = y
        self.phitbox = (self.x +10, self.y +14, 62, 230)

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 4
        if key[pygame.K_DOWN] or key[pygame.K_s]:  # down key
            self.y += dist  # move down
        elif key[pygame.K_UP] or key[pygame.K_w]:  # up key
            self.y -= dist  # move up
        if key[pygame.K_RIGHT] or key[pygame.K_d]:  # right key
            self.x = self.x + dist  # move right
        elif key[pygame.K_LEFT] or key[pygame.K_a]:  # left key
            self.x = self.x - dist  # move left

    def draw(self, screen):
        # blit yourself at your current position
        screen.blit(player, (self.x, self.y))
        self.phitbox = (self.x +10, self.y +14, 62, 230)
        #pygame.draw.rect(screen, (255, 0, 0,), self.phitbox, 2)


# Shoot sanitizer
class Sanitizer(pygame.sprite.Sprite): #shoots to the left
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = tizer
        self.x = x + 20
        self.y = y +60
        self.vel = 5
        self.sanit_hitbox = (self.x, self.y, 25, 35)

    def sanitdraw(self, screen):
        screen.blit(tizer, (self.x, self.y))
        self.sanit_hitbox = (self.x, self.y, 25, 35)
        #pygame.draw.rect(screen, (255, 0, 0), self.sanit_hitbox, 2)


# Right going Left Coronas
class Coronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health
        self.hitbox = (self.x + 5, self.y, 90, 75)

    def draw(self, screen):
        screen.blit(virus, (self.x, self.y))
        self.hitbox = (self.x + 5, self.y, 90, 75)
        # pygame.draw.rect(screen,(255,0,0),self.hitbox,2)

    def move(self):
        self.x = self.x + 2.5
        if self.x > width:
            self.x = -130
            self.y = random.randint(0, 500)

    def hit(self):
        print('hit')
        self.x = -130


# Left going Right Coronas
class LeftCoronavirus(pygame.sprite.Sprite):
    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.image = virus
        self.x = x
        self.y = y
        self.health = health
        self.hitboxleft = (self.x + 5, self.y, 90, 75)

    def drawleft(self, screen):
        screen.blit(virus, (self.x, self.y))
        self.hitboxleft = (self.x + 5, self.y, 90, 75)
        # pygame.draw.rect(screen,(255,0,0),self.hitboxleft,2)

    def moveleft(self):
        self.x = self.x - 2.5
        if self.x < 0:
            self.x = width + 50
            self.y = random.randint(0, 500)

    def hitleft(self):
        print('hit')
        self.x = width + 50


# Main Game
def main():
    running = True
    FPS = 50
    lives = 5
    score = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 80)
    enemies = []
    enemiesleft = []
    sanits = []
    leftsanits = []
    wave_length = 1
    playerimage = Player(width / 2, height / 2 - 20)
    clock = pygame.time.Clock()

    # Update Screen
    def redraw_window():
        screen.blit(background, (0, 0))
        playerimage.draw(screen)
        # draw labels
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        screen.blit(score_label, (850, 10))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        screen.blit(lives_label, (1030, 10))
        if lives <= 0:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))
            screen.blit(lost_label, (width / 2.3, height / 2))

        # draw ronas
        for rona in enemies:
            rona.draw(screen)
        for ronaleft in enemiesleft:
            ronaleft.drawleft(screen)

        # draw sanits
        for sanit in sanits:
            sanit.sanitdraw(screen)
        for leftsanit in leftsanits:
            leftsanit.sanitdraw(screen)

        pygame.display.update()

    while running:
        # while loop setup
        clock.tick(FPS)
        rona = Coronavirus(0, 100)
        rona.draw(screen)
        playerimage.handle_keys()
        playerimage.draw(screen)
        leftrona = LeftCoronavirus(width, 100)
        leftrona.drawleft(screen)
        sanit = Sanitizer(playerimage.phitbox[0],playerimage.phitbox[1]+50)
        sanit.sanitdraw(screen)
        leftsanit = Sanitizer(playerimage.phitbox[0],playerimage.phitbox[1]+50)
        leftsanit.sanitdraw(screen)

        for enemy in enemies:
            enemy.move()
        for leftenemy in enemiesleft:
            leftenemy.moveleft()

        # Generate additional viruses
        if len(enemies) == 0:
            wave_length += 2
            for i in range(wave_length):
                rona2 = Coronavirus(random.randint(-800, -150),
                                    random.randint(10, 500))  # instance of Coronavirus class
                enemies.append(rona2)
        if len(enemiesleft) == 0:
            wave_length += 1
            for i in range(wave_length):
                rona3 = LeftCoronavirus(random.randint(width, 1800),
                                        random.randint(10, 500))  # instance of Coronavirus class
                enemiesleft.append(rona3)

        # Virus Collisions
        for enemy in enemies:  # hitboxes: x,y,width,height
            if enemy.hitbox[1] + enemy.hitbox[3] > playerimage.phitbox[1] and enemy.hitbox[1]<playerimage.phitbox[1]: #Hit on top
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    enemy.hit()
                    lives = lives - 1
            if enemy.hitbox[1] + enemy.hitbox[3] < playerimage.phitbox[1] + playerimage.phitbox[3] and enemy.hitbox[1] > playerimage.phitbox[1]: # Can't pass through player
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    enemy.hit()
                    lives = lives - 1
            if enemy.hitbox[1] + enemy.hitbox[3] > playerimage.phitbox[1] + playerimage.phitbox[3] and enemy.hitbox[1] < playerimage.phitbox[1]+ playerimage.phitbox[3]: #Hit on Bottom
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    enemy.hit()
                    lives = lives - 1

        for leftenemy in enemiesleft:  # hitboxes: x,y,width,height
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > playerimage.phitbox[1] and leftenemy.hitboxleft[1]<playerimage.phitbox[1]: #Hit on Top
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    lives = lives - 1
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] < playerimage.phitbox[1] +playerimage.phitbox[3] and leftenemy.hitboxleft[1]>playerimage.phitbox[1]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    lives = lives - 1
            if leftenemy.hitboxleft[1] < playerimage.phitbox[1] +playerimage.phitbox[3] and leftenemy.hitboxleft[1]+ leftenemy.hitboxleft[3]>playerimage.phitbox[1]+playerimage.phitbox[3]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    lives = lives - 1

        # Shoot Sanitizers
        for sanit in sanits: #to the left
            if sanit.x > -5:
                sanit.x -= sanit.vel
            else:
                sanits.pop(sanits.index(sanit))
        for leftsanit in leftsanits:
            if leftsanit.x < width+5: #to the right
                leftsanit.x += leftsanit.vel
            else:
                leftsanits.pop(leftsanits.index(leftsanit))
        key = pygame.key.get_pressed()
        if key[pygame.K_z]:
            if len(sanits) < 1: #can't exceed this number shots on screen at one time
                sanits.append(sanit)
        if key[pygame.K_c]:
            if len(leftsanits) < 1:  # can't exceed this number shots on screen at one time
                leftsanits.append(leftsanit)

        # Sanitizer Shot Coronavirus Hits
        for enemy in enemies:  # hitboxes: x,y,width,height
            if enemy.hitbox[1] + enemy.hitbox[3] > sanit.sanit_hitbox[1] and enemy.hitbox[1]<sanit.sanit_hitbox[1]: #Hit on top
                if enemy.hitbox[0] + enemy.hitbox[2] > sanit.sanit_hitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
            if enemy.hitbox[1] + enemy.hitbox[3] < sanit.sanit_hitbox[1] + sanit.sanit_hitbox[3] and enemy.hitbox[1] > sanit.sanit_hitbox[1]: # Can't pass through player
                if enemy.hitbox[0] + enemy.hitbox[2] > sanit.sanit_hitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
            if enemy.hitbox[1] + enemy.hitbox[3] > sanit.sanit_hitbox[1] + sanit.sanit_hitbox[3] and enemy.hitbox[1] < sanit.sanit_hitbox[1]+ sanit.sanit_hitbox[3]: #Hit on Bottom
                if enemy.hitbox[0] + enemy.hitbox[2] > sanit.sanit_hitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
        #to the right
        for leftenemy in enemiesleft:  # hitboxes: x,y,width,height
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > leftsanit.sanit_hitbox[1] and leftenemy.hitboxleft[1]<leftsanit.sanit_hitbox[1]: #Hit on Top
                if leftenemy.hitboxleft[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] < leftsanit.sanit_hitbox[1] +leftsanit.sanit_hitbox[3] and leftenemy.hitboxleft[1]>leftsanit.sanit_hitbox[1]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1
            if leftenemy.hitboxleft[1] < leftsanit.sanit_hitbox[1] +leftsanit.sanit_hitbox[3] and leftenemy.hitboxleft[1]+ leftenemy.hitboxleft[3]>leftsanit.sanit_hitbox[1]+leftsanit.sanit_hitbox[3]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1

        redraw_window()


        # To exit game screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


main()
