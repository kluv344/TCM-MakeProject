import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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

clock = pygame.time.Clock() <<<
frame_rate = 60 <<<<
frame_count = 0 <<<<
start_time = 90 <<<<

pygame.display.set_caption("Rona Rambo")
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

    total_seconds = start_time - (frame_count // frame_rate) <<<<<<
    if total_seconds < 0:      <<<<<<
        total_seconds = 0      <<<<<<
    minutes = total_seconds // 60      <<<<<<
    seconds = total_seconds % 60       <<<<<<
    output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds) <<<<<<
    text = font.render(output_string, True, BLACK) <<<<<<
    screen.blit(text, [20, 50]) <<<<<<
    frame_count += 1  <<<<<<
    clock.tick(frame_rate) <<<<<<
    pygame.display.flip() <<<<<<


    pygame.display.update() # update the screen
