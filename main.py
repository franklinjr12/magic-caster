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
DEFAULTPLAYERMOVEDELAY = 50
DEFAULTPROJECTILESPEED = 1
FIRSTSPELL = 1


global_projectiles = []


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
        self.last_time = pygame.time.get_ticks()

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

    def can_update_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time > DEFAULTPLAYERMOVEDELAY:
            self.last_time = pygame.time.get_ticks()
            return True
        return False

    def cast_spell(self, spell):
        if spell == FIRSTSPELL:
            if self.facing == FACINGRIGHT:
                global_projectiles.append(Projectile(self, self.pos.x+DEFAULTRECTSIZE,
                                                     self.pos.y+DEFAULTRECTSIZE/2, DEFAULTPROJECTILESPEED, 0, 5, "red"))
            else:
                global_projectiles.append(Projectile(self, self.pos.x+DEFAULTRECTSIZE,
                                                     self.pos.y+DEFAULTRECTSIZE/2, -DEFAULTPROJECTILESPEED, 0, 5, "red"))
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
# class Surface


class Projectile:
    def __init__(self, owner, xpos, ypos, xvel, yvel, size, color):
        self.owner = owner
        self.pos = pygame.Vector2(xpos, ypos)
        self.vel = pygame.Vector2(xvel, yvel)
        self.size = size
        # will create a circle
        self.body = pygame.draw.circle(
            screen, color, (self.pos.x, self.pos.y), self.size)
        self.bodycolor = color

    def draw(self):
        pygame.draw.circle(screen, self.bodycolor,
                           (self.pos.x, self.pos.y), self.size)

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.body.x = self.pos.x
        self.body.y = self.pos.y
# class Projectile


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
            if event.key == pygame.K_q:
                player.cast_spell(FIRSTSPELL)
        # check if key is still pressed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_moving_left = False
            if event.key == pygame.K_RIGHT:
                player_moving_right = False
    if player.can_update_move():
        if player_moving_left:
            player.update(player.pos.x - DEFAULTSPEED, player.pos.y)
        if player_moving_right:
            player.update(player.pos.x + DEFAULTSPEED, player.pos.y)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # drawings
    for surface in surfaces:
        surface.draw()
    for projectile in global_projectiles:
        projectile.draw()
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
    for projectile in global_projectiles:
        projectile.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
pygame.quit()
