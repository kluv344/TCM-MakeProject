# Person movement + coronas; No timer
## Coronavirus Fight
import sys
import pygame
import random
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from pygame.sprite import RenderUpdates

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50,50,50)
RED = (255, 0, 0)
GREEN = (87, 189, 36)
BLUE = (36, 189, 176)
YELLOW = (255, 248, 122)

pygame.font.init()

# Initialize the game screen
pygame.init()
width, height = 1200, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rona Rambo")

# Load images
background = pygame.image.load("virusback.PNG")
background = pygame.transform.scale(background, (width, height))
player = pygame.image.load("maledoc2.png")
player = pygame.transform.scale(player, (80, 250))
virus = pygame.image.load("rona.png")
virus = pygame.transform.scale(virus, (100, 75))
coin = pygame.image.load("coin.png")
coin = pygame.transform.scale(coin, (100, 75))
tizer = pygame.image.load("sanitizer.png")
tizer = pygame.transform.scale(tizer, (25, 35))
#Load Music
music = pygame.mixer.music.load('UpbeatFunk.wav')
pygame.mixer.music.play(-1)
punchSound = pygame.mixer.Sound('Thwack.wav')

def surface_and_text(text, font_size, text_color, background_color):
    font = pygame.freetype.SysFont("comicsans", font_size, bold = True)
    surface, _ = font.render(text = text, fgcolor = text_color, bgcolor = background_color)
    return surface.convert_alpha()

class ChangingButtons(Sprite):

    def __init__(self, center_position, text, font_size, text_color, background_color, action=None):
        """
        Args:
            center_position - tuple (x, y)
            text - string of text to write
            font_size - int
            background_color (background colour) - tuple (r, g, b)
            text_color (text colour) - tuple (r, g, b)
        """
        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = surface_and_text(text=text, font_size=font_size, text_color = text_color, background_color = background_color)

        # create the image that shows when mouse is over the element
        highlighted_image = surface_and_text(text=text, font_size=font_size * 1.5, text_color = text_color, background_color = background_color)

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]

        self.rects = [
            default_image.get_rect(center = center_position),
            highlighted_image.get_rect(center = center_position)]

        self.action = action

        # calls the init method of the parent sprite class
        super().__init__()

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)


def state_changes():
    pygame.init()

    screen = pygame.display.set_mode((width, height))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            main()

        if game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()

def title_screen(screen):
    start_btn = ChangingButtons(
        center_position = (width/2, 350),
        font_size=30,
        text_color=WHITE,
        background_color=BLUE,
        text="Start",
        action = GameState.NEWGAME)

    quit_btn = ChangingButtons(
        center_position=(width/2, 400),
        font_size=30,
        text_color=WHITE,
        background_color=BLUE,
        text="Quit",
        action=GameState.QUIT)

    buttons = RenderUpdates(start_btn, quit_btn)
    return game_loop(screen, buttons)

def game_loop(screen, buttons):
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)
        title_font = pygame.font.SysFont("freesansbold", 120)
        instructions_font = pygame.font.SysFont("comicsans", 30)
        instructionskk_font = pygame.font.SysFont("italicbold", 24)
        title_label = title_font.render("Rona Rambo", 1, BLACK)
        instructions_label = instructions_font.render("You need to last 90 seconds amidst the COVID-19 battlefield.", 1, GRAY)
        instructions_label2 = instructions_font.render("You have 5 lives and your only ammunition is handsanitizer.", 1, GRAY)
        instructions_keysL = instructionskk_font.render("A or LEFT ARROW = Move Left", 1, BLACK)
        instructions_keysR = instructionskk_font.render("D or RIGHT ARROW = Move Right", 1, BLACK)
        instructions_keysU = instructionskk_font.render("W or UP ARROW = Move Up", 1, BLACK)
        instructions_keysD = instructionskk_font.render("S or DOWN ARROW = Move Down", 1, BLACK)
        instructions_keysS = instructionskk_font.render("'Z' = Shoot Left", 1, BLACK)
        instructions_keysH = instructionskk_font.render("'C' = Shoot Right", 1, BLACK)
        screen.blit(title_label, (350, 150))
        pygame.draw.line(screen, BLACK, (350,230), (860,230), 5)
        screen.blit(instructions_label, (310, 245))
        screen.blit(instructions_label2, (310, 275))
        screen.blit(instructions_keysL, (120, 500))
        screen.blit(instructions_keysR, (120, 550))
        screen.blit(instructions_keysU, (500, 500))
        screen.blit(instructions_keysD, (500, 550))
        screen.blit(instructions_keysS, (900, 500))
        screen.blit(instructions_keysH, (900, 550))

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1

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
        dist = 6
        if key[pygame.K_DOWN] or key[pygame.K_s]:  # down key
            if self.y<height-250:
                self.y += dist  # move down
        elif key[pygame.K_UP] or key[pygame.K_w]:  # up key
            if self.y> -12:
                self.y -= dist  # move up
        if key[pygame.K_RIGHT] or key[pygame.K_d]:  # right key
            if self.x< width -75:
                self.x = self.x + dist  # move right
        elif key[pygame.K_LEFT] or key[pygame.K_a]:  # left key
            if self.x> -10:
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
        self.vel = 8
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
        self.x = self.x + 4
        if self.x > width:
            self.x = -130
            self.y = random.randint(0, 500)

    def hit(self):
        print('hit')
        self.x = -130
        self.y = random.randint(0, 500)


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
        self.x = self.x - 4
        if self.x < 0:
            self.x = width + 50
            self.y = random.randint(0, 500)

    def hitleft(self):
        print('hit')
        self.x = width + 50
        self.y = random.randint(0, 500)


# Main Game
def main():
    running = True
    FPS = 60
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
    frame_count = 0
    start_time =90
    font = pygame.font.SysFont("comicsans", 40)

    # Update Screen
    def redraw_window(minutes,seconds):
        screen.blit(background, (0, 0))
        playerimage.draw(screen)
        # draw labels
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        screen.blit(score_label, (850, 10))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        screen.blit(lives_label, (1030, 10))

        #Timer
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        text = font.render(output_string, True, (0,0,0))
        screen.blit(text, [20, 15])

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

        if lives <= 0:
            lost_label = lost_font.render(f"You lost! Score: {score} ", 1, RED)
            screen.blit(lost_label, (width/2-200, height/2-100))
            goback_main = main_font.render("Press Space to Return to Main Menu", 1, BLACK)
            screen.blit(goback_main, (width/2-300, height/2-20))
            keys = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                title_screen(screen)
            elif key[pygame.K_SPACE]:
                pygame.quit()
            # print("trigger title screen from no lives")
            # title_screen(screen)

        if pygame.time.get_ticks() >= 90000:
            lost_label = lost_font.render(f"You lost! Score: {score} ", 1, RED)
            screen.blit(lost_label, (width/2-200, height/2-100))
            goback_main = main_font.render("Press Space to Return to Main Menu", 1, BLACK)
            screen.blit(goback_main, (width/2-300, height/2-20))
            keys = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                title_screen(screen)
            elif key[pygame.K_SPACE]:
                pygame.quit()

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

        #Timer
        total_seconds = start_time - (frame_count // FPS)
        if total_seconds < 0:
            total_seconds = 0
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
        text = font.render(output_string, True, (0,0,0))
        screen.blit(text, [20, 30])
        frame_count += 2
        clock.tick(FPS)


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
                    punchSound.play()
                    lives = lives - 1
            if enemy.hitbox[1] + enemy.hitbox[3] < playerimage.phitbox[1] + playerimage.phitbox[3] and enemy.hitbox[1] > playerimage.phitbox[1]: # Can't pass through player
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    enemy.hit()
                    punchSound.play()
                    lives = lives - 1
            if enemy.hitbox[1] + enemy.hitbox[3] > playerimage.phitbox[1] + playerimage.phitbox[3] and enemy.hitbox[1] < playerimage.phitbox[1]+ playerimage.phitbox[3]: #Hit on Bottom
                if enemy.hitbox[0] + enemy.hitbox[2] > playerimage.phitbox[0] and enemy.hitbox[0] + enemy.hitbox[2] < playerimage.phitbox[0] + playerimage.phitbox[2]:
                    enemy.hit()
                    punchSound.play()
                    lives = lives - 1

        for leftenemy in enemiesleft:  # hitboxes: x,y,width,height
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > playerimage.phitbox[1] and leftenemy.hitboxleft[1]<playerimage.phitbox[1]: #Hit on Top
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    punchSound.play()
                    lives = lives - 1
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] < playerimage.phitbox[1] +playerimage.phitbox[3] and leftenemy.hitboxleft[1]>playerimage.phitbox[1]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    punchSound.play()
                    lives = lives - 1
            if leftenemy.hitboxleft[1] < playerimage.phitbox[1] +playerimage.phitbox[3] and leftenemy.hitboxleft[1]+ leftenemy.hitboxleft[3]>playerimage.phitbox[1]+playerimage.phitbox[3]:  # Can't pass through player
                if leftenemy.hitboxleft[0] < playerimage.phitbox[0] + playerimage.phitbox[2] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2]> playerimage.phitbox[0]+ playerimage.phitbox[2]:
                    leftenemy.hitleft()
                    punchSound.play()
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
            if len(sanits) < 3: #can't exceed this number shots on screen at one time
                sanits.append(sanit) #Include timestamp or increase number everytime run game loop
        if key[pygame.K_c]:
            if len(leftsanits) < 3:  # can't exceed this number shots on screen at one time
                leftsanits.append(leftsanit)

        # Sanitizer Shot Coronavirus Hits
        for enemy in enemies: #Hit from in Front # hitboxes: x,y,width,height
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
            #Hit from Behind
            if enemy.hitbox[1] + enemy.hitbox[3] > leftsanit.sanit_hitbox[1] and enemy.hitbox[1]<leftsanit.sanit_hitbox[1]: #Hit on Top
                if enemy.hitbox[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and enemy.hitbox[0] + enemy.hitbox[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
            if enemy.hitbox[1] + enemy.hitbox[3] < leftsanit.sanit_hitbox[1] +leftsanit.sanit_hitbox[3] and enemy.hitbox[1]>leftsanit.sanit_hitbox[1]:  # Can't pass through player
                if enemy.hitbox[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and enemy.hitbox[0] + enemy.hitbox[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
            if enemy.hitbox[1] < leftsanit.sanit_hitbox[1] +leftsanit.sanit_hitbox[3] and enemy.hitbox[1]+ enemy.hitbox[3]>leftsanit.sanit_hitbox[1]+leftsanit.sanit_hitbox[3]:  # Can't pass through player
                if enemy.hitbox[0] < leftsanit.sanit_hitbox[0] + leftsanit.sanit_hitbox[2] and enemy.hitbox[0] + enemy.hitbox[2]> leftsanit.sanit_hitbox[0]+ leftsanit.sanit_hitbox[2]:
                    enemy.hit()
                    score = score + 1
        #Other sided coronas #Hit from in Front
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
        #Hit from Behind
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > sanit.sanit_hitbox[1] and leftenemy.hitboxleft[1] < sanit.sanit_hitbox[1]:  # Hit on top
                if leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] > sanit.sanit_hitbox[0] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] <sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] < sanit.sanit_hitbox[1] + sanit.sanit_hitbox[3] and leftenemy.hitboxleft[1] > sanit.sanit_hitbox[1]:  # Can't pass through player
                if leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] > sanit.sanit_hitbox[0] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] < sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1
            if leftenemy.hitboxleft[1] + leftenemy.hitboxleft[3] > sanit.sanit_hitbox[1] + sanit.sanit_hitbox[3] and leftenemy.hitboxleft[1] < sanit.sanit_hitbox[1] + sanit.sanit_hitbox[3]:  # Hit on Bottom
                if leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] > sanit.sanit_hitbox[0] and leftenemy.hitboxleft[0] + leftenemy.hitboxleft[2] < sanit.sanit_hitbox[0] + sanit.sanit_hitbox[2]:
                    leftenemy.hitleft()
                    score = score + 1

        redraw_window(minutes,seconds)


        # To exit game screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

state_changes()
main()