import pygame, os
import time

BLACK = (0, 0, 0)

class Nurse(object):  # represents the Nurse/player, not the game
    def __init__(self):
        """ The constructor of the class """
        self.image = pygame.image.load("female nurse.png")
        self.image = pygame.transform.scale(self.image, (75,250))
        # the nurse's position
        self.x = 75
        self.y = 300

    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 10
        #if key[pygame.K_DOWN]: # down key
            #self.y += dist # move down
        #elif key[pygame.K_UP]: # up key
            #self.y -= dist # move up
        if key[pygame.K_RIGHT]: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.x -= dist # move left

    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))

pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
hospitalbackground = pygame.image.load("background.png")
hospitalbackground = pygame.transform.scale(hospitalbackground, (1200, 600))

nurse = Nurse() # create an instance
clock = pygame.time.Clock()

pygame.display.set_caption("Rona Rambo")
time_left = 90 #duration of the timer in seconds
font = pygame.font.SysFont("comicsans", 30)

running = True
while running:
    # handle every event since the last frame.
    pygame.init()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit() # quit the screen
            running = False

    nurse.handle_keys() # handle the keys

    screen.blit(hospitalbackground, (0, 0))
    nurse.draw(screen) # draw the nurse to the screen
    pygame.display.update() # update the screen

    total_mins = time_left // 60  # minutes left
    total_sec = time_left - (60 * (total_mins))  # seconds left
    time_left -= 1
    if time_left > -1:
        text = font.render(("Time left: " + str(total_mins) + ":" + str(total_sec)), True, BLACK)
        screen.blit(text, (20, 25))
        pygame.display.flip()
        screen.fill((20, 20, 20))
        time.sleep(1)  # making the time interval of the loop 1sec
    else:
        text = font.render("Time Over!!", True, BLACK)
        screen.blit(text, (430, 261))
        pygame.display.flip()
        screen.fill((20, 20, 20))

