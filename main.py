# Example file showing a basic pygame "game loop"
import pygame
import random

# constants
WIDTH = 1280
HEIGHT = 720
screen = None

DEFAULTSPEED = 5
DEFAULTRECTSIZE = 15
FACINGRIGHT = 1
FACINGLEFT = -1
DEFAULTGRAVITY = 1


class Actor:
    def __init__(self, xpos=0, ypos=0):
        self.pos = pygame.Vector2(xpos, ypos)
        self.image = None
        self.body = pygame.Rect(self.pos.x, self.pos.y,
                                DEFAULTRECTSIZE, DEFAULTRECTSIZE)
        self.head = pygame.Rect(
            self.pos.x+DEFAULTRECTSIZE, self.pos.y, DEFAULTRECTSIZE/2, DEFAULTRECTSIZE/2)
        self.bodycolor = "white"
        self.headcolor = "yellow"
        self.yspeed = 0
        self.facing = FACINGRIGHT

    def draw(self):
        pygame.draw.rect(screen, self.bodycolor, self.body)
        pygame.draw.rect(screen, self.headcolor, self.head)

    def update(self, newx=0, newy=0):
        if newx != 0:
            if newx > self.pos.x:
                self.facing = FACINGRIGHT
            elif newx < self.pos.x:
                self.facing = FACINGLEFT
            self.pos.x = newx
            # check for border
            if self.pos.x < 0:
                self.pos.x = 0
            if self.pos.x > WIDTH:
                self.pos.x = WIDTH
        self.pos.y = newy + self.yspeed
        # check for border
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        self.body.x = self.pos.x
        self.body.y = self.pos.y
        if self.facing == FACINGRIGHT:
            self.head.x = self.pos.x+DEFAULTRECTSIZE
        else:
            self.head.x = self.pos.x-DEFAULTRECTSIZE/2
        self.head.y = self.pos.y
# class Actor


class Surface:
    def __init__(self, xpos, ypos, width, height):
        self.pos = pygame.Vector2(xpos, ypos)
        self.image = None
        self.width = width
        self.height = height
        self.body = pygame.Rect(self.pos.x, self.pos.y,
                                self.width, self.height)
        self.bodycolor = "green"

    def draw(self):
        pygame.draw.rect(screen, self.bodycolor, self.body)

    def update(self):
        pass


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
player = Actor(WIDTH / 2, HEIGHT / 2)
floor = Surface(0, HEIGHT-HEIGHT*0.1, WIDTH, 4)
surfaces = [floor]

player_moving_left = False
player_moving_right = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # check if a key is pressed
        if event.type == pygame.KEYDOWN:
            # handles arrow keys
            if event.key == pygame.K_LEFT:
                player_moving_left = True
                #player.update(player.pos.x - DEFAULTSPEED, player.pos.y)
            if event.key == pygame.K_RIGHT:
                player_moving_right = True
                #player.update(player.pos.x + DEFAULTSPEED, player.pos.y)
            if event.key == pygame.K_UP:
                player.update(player.pos.x, player.pos.y - DEFAULTSPEED)
            if event.key == pygame.K_DOWN:
                player.update(player.pos.x, player.pos.y + DEFAULTSPEED)
        # check if key is still pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_moving_left = False
            if event.key == pygame.K_RIGHT:
                player_moving_right = False
    if player_moving_left:
        player.update(player.pos.x - DEFAULTSPEED, player.pos.y)
    if player_moving_right:
        player.update(player.pos.x + DEFAULTSPEED, player.pos.y)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # drawings
    for surface in surfaces:
        surface.draw()
    player.draw()

    # logics
    player.pos.y += DEFAULTGRAVITY
    # check if player collides with surfaces
    for surface in surfaces:
        if player.body.colliderect(surface.body):
            player.pos.y = surface.pos.y - DEFAULTRECTSIZE
            player.yspeed = 0

    # updates
    player.update(player.pos.x, player.pos.y)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()