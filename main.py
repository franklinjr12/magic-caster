# Example file showing a basic pygame "game loop"
import pygame
import random
import math


class GameEnvironment:
    # constants
    WIDTH = 1280
    HEIGHT = 720
    DEFAULTSPEED = 5
    DEFAULTRECTSIZE = 15
    FACINGRIGHT = 1
    FACINGLEFT = -1
    DEFAULTGRAVITY = 1
    DEFAULTPLAYERMOVEDELAY = 50
    DEFAULTPROJECTILESPEED = 3
    DEFAULTPROJECTILESIZE = 3
    FIRSTSPELL = 1
    SECONDSPELL = 2
    DEFAULTSPELLCOOLDOWN = 1000
    DEFAULTLIFE = 100
    DEFAULTSPELLDAMAGE = 10
    # globals
    global_projectiles = []
    game_paused = False
    player = None
    enemies = []
    surfaces = []
    screen = None
    clock = None
    running = True


# class Game


class Spell:
    SLOWMODIFIER = "slow"

    def __init__(
        self,
        shape=None,
        effect=None,
        element=None,
        modifiers=None,
        description=None,
        is_projectile=True,
        cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
    ):
        self.shape = shape
        self.effect = effect
        self.element = element
        self.modifiers = modifiers
        self.description = description
        self.is_projectile = is_projectile
        self.cooldown = cooldown
        self.cooldown_ticks = 0
        self.damage = GameEnvironment.DEFAULTSPELLDAMAGE

    def is_on_cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown_ticks > self.cooldown:
            return False
        return True

    def cast(self, game_environment, x, y, angle):
        if self.is_on_cooldown():
            return
        self.cooldown_ticks = pygame.time.get_ticks()
        if self.description == "simple energy projectile":
            speed_x = game_environment.DEFAULTPROJECTILESPEED * math.cos(
                math.radians(angle)
            )
            speed_y = -(
                game_environment.DEFAULTPROJECTILESPEED * math.sin(math.radians(angle))
            )
            if self.is_projectile:
                game_environment.global_projectiles.append(
                    Projectile(
                        self,
                        x + game_environment.DEFAULTRECTSIZE,
                        y + game_environment.DEFAULTRECTSIZE / 2,
                        speed_x,
                        speed_y,
                        self.shape["size"],
                        self.shape["color"],
                        game_environment,
                    )
                )
        elif self.description == "3 shot energy projectile":
            speed_x = game_environment.DEFAULTPROJECTILESPEED * math.cos(
                math.radians(angle)
            )
            speed_y = -(
                game_environment.DEFAULTPROJECTILESPEED * math.sin(math.radians(angle))
            )
            if self.is_projectile:
                game_environment.global_projectiles.append(
                    Projectile(
                        self,
                        x + game_environment.DEFAULTRECTSIZE,
                        y + game_environment.DEFAULTRECTSIZE / 2,
                        speed_x,
                        speed_y,
                        self.shape["size"],
                        self.shape["color"],
                        game_environment,
                    )
                )
                game_environment.global_projectiles.append(
                    Projectile(
                        self,
                        x + game_environment.DEFAULTRECTSIZE,
                        y + game_environment.DEFAULTRECTSIZE / 2,
                        speed_x,
                        speed_y + math.sin(math.pi / 6),
                        self.shape["size"],
                        self.shape["color"],
                        game_environment,
                    )
                )
                game_environment.global_projectiles.append(
                    Projectile(
                        self,
                        x + game_environment.DEFAULTRECTSIZE,
                        y + game_environment.DEFAULTRECTSIZE / 2,
                        speed_x,
                        speed_y - math.sin(math.pi / 6),
                        self.shape["size"],
                        self.shape["color"],
                        game_environment,
                    )
                )


# class Spell


class GameSpells:
    spells = {}


class Projectile:
    def __init__(self, spell, xpos, ypos, xvel, yvel, size, color, game_environment):
        self.game_environment = game_environment
        self.spell = spell
        self.pos = pygame.Vector2(xpos, ypos)
        self.vel = pygame.Vector2(xvel, yvel)
        self.size = size
        # will create a circle
        self.body = pygame.draw.circle(
            self.game_environment.screen, color, (self.pos.x, self.pos.y), self.size
        )
        self.bodycolor = color

    def draw(self):
        pygame.draw.circle(
            self.game_environment.screen,
            self.bodycolor,
            (self.pos.x, self.pos.y),
            self.size,
        )

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.body.x = self.pos.x
        self.body.y = self.pos.y


# class Projectile

# class GameSpells


class Actor:
    def __init__(
        self, xpos=0, ypos=0, show_name=False, actor_name="", game_environment=None
    ):
        self.game_environment = game_environment
        self.pos = pygame.Vector2(xpos, ypos)
        self.image = None
        self.body = pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.game_environment.DEFAULTRECTSIZE,
            self.game_environment.DEFAULTRECTSIZE,
        )
        self.head = pygame.Rect(
            self.pos.x + self.game_environment.DEFAULTRECTSIZE,
            self.pos.y,
            self.game_environment.DEFAULTRECTSIZE / 2,
            self.game_environment.DEFAULTRECTSIZE / 2,
        )
        self.bodycolor = "white"
        self.headcolor = "yellow"
        self.yspeed = 0
        self.facing = self.game_environment.FACINGRIGHT
        self.last_time = pygame.time.get_ticks()
        self.first_spell_last_time = pygame.time.get_ticks()
        self.show_name = show_name
        self.actor_name = actor_name
        self.second_spell_last_time = pygame.time.get_ticks()
        self.life = GameEnvironment.DEFAULTLIFE
        self.modifiers = []

    def draw(self):
        # draws body
        pygame.draw.rect(self.game_environment.screen, self.bodycolor, self.body)
        # draws health
        pygame.draw.rect(self.game_environment.screen, self.headcolor, self.head)
        # show actor name
        if self.show_name:
            font = pygame.font.Font("freesansbold.ttf", 12)
            text = font.render(self.actor_name, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (
                self.pos.x + self.game_environment.DEFAULTRECTSIZE / 2,
                self.pos.y - self.game_environment.DEFAULTRECTSIZE / 2,
            )
            self.game_environment.screen.blit(text, textRect)
        # draw health bar
        pygame.draw.rect(
            self.game_environment.screen,
            "green",
            (
                self.pos.x - self.game_environment.DEFAULTRECTSIZE / 2 - 6,
                self.pos.y - self.game_environment.DEFAULTRECTSIZE / 2 - 8,
                self.life / 2,
                3,
            ),
        )

    def update(self, newx=0, newy=0):
        if newx != 0:
            if newx > self.pos.x:
                self.facing = self.game_environment.FACINGRIGHT
                if self.modifiers.count(Spell.SLOWMODIFIER) > 0:
                    newx = newx - 1
            elif newx < self.pos.x:
                self.facing = self.game_environment.FACINGLEFT
                if self.modifiers.count(Spell.SLOWMODIFIER) > 0:
                    newx = newx + 1
            self.pos.x = newx
            # check for border
            if self.pos.x < 0:
                self.pos.x = 0
            if self.pos.x > self.game_environment.WIDTH:
                self.pos.x = self.game_environment.WIDTH
        self.pos.y = newy + self.yspeed
        # check for border
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > self.game_environment.HEIGHT:
            self.pos.y = self.game_environment.HEIGHT
        self.body.x = self.pos.x
        self.body.y = self.pos.y
        if self.facing == self.game_environment.FACINGRIGHT:
            self.head.x = self.pos.x + self.game_environment.DEFAULTRECTSIZE
        else:
            self.head.x = self.pos.x - self.game_environment.DEFAULTRECTSIZE / 2
        self.head.y = self.pos.y

    def can_update_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time > self.game_environment.DEFAULTPLAYERMOVEDELAY:
            self.last_time = pygame.time.get_ticks()
            return True
        return False

    def set_spell(self, spell_number):
        if spell_number == self.game_environment.FIRSTSPELL:
            self.first_spell = GameSpells.spells[spell_number]
        elif spell_number == self.game_environment.SECONDSPELL:
            self.second_spell = GameSpells.spells[spell_number]

    def cast_spell(self, spell):
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # get angle between player and mouse
        angle = pygame.math.Vector2(
            mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
        ).angle_to((1, 0))
        if spell == self.game_environment.FIRSTSPELL:
            self.first_spell.cast(self.game_environment, self.pos.x, self.pos.y, angle)
        if spell == self.game_environment.SECONDSPELL:
            self.second_spell.cast(self.game_environment, self.pos.x, self.pos.y, angle)

    def should_show_name(self, onoff):
        self.show_name = onoff

    def interact(self, projectile: Projectile):
        print(
            "Actor {} had {} life took {} damage and took {} modifiers".format(
                self.actor_name,
                self.life,
                projectile.spell.damage,
                projectile.spell.modifiers,
            )
        )
        if projectile.spell.modifiers is not None:
            for modifier in projectile.spell.modifiers:
                # check if modifier is already on actor
                if self.modifiers.count(modifier) == 0:
                    self.modifiers.append(modifier)
        self.life -= projectile.spell.damage
        if self.life <= 0:
            self.game_environment.enemies.remove(self)


# class Actor


class Surface:
    def __init__(self, xpos, ypos, width, height, game_environment):
        self.game_environment = game_environment
        self.pos = pygame.Vector2(xpos, ypos)
        self.image = None
        self.width = width
        self.height = height
        self.body = pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.width,
            self.height,
        )
        self.bodycolor = "green"

    def draw(self):
        pygame.draw.rect(self.game_environment.screen, self.bodycolor, self.body)

    def update(self):
        pass


# class Surface


class SpellCooldownDisplay:
    def __init__(self, key, spell: Spell, game_environment, xpos, ypos, size):
        self.key = key
        self.game_environment = game_environment
        self.spell = spell
        self.xpos = xpos
        self.ypos = ypos
        self.size = size

    def draw(self):
        color = "white"
        if self.spell.is_on_cooldown():
            color = "red"
        # make rectangle on xpos and ypox
        pygame.draw.rect(
            self.game_environment.screen,
            color,
            (self.xpos, self.ypos, self.size, self.size),
        )
        # draw key letter on rectangle
        font = pygame.font.Font("freesansbold.ttf", 12)
        text = font.render(self.key, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (
            self.xpos + self.size / 2,
            self.ypos + self.size / 2,
        )
        self.game_environment.screen.blit(text, textRect)


# class SpellCooldownDisplay


def setup(game_environment: GameEnvironment):
    # game setup
    pygame.init()
    game_environment.screen = pygame.display.set_mode(
        (game_environment.WIDTH, game_environment.HEIGHT)
    )
    game_environment.clock = pygame.time.Clock()
    game_environment.running = True
    game_environment.player = Actor(
        game_environment.WIDTH / 2,
        game_environment.HEIGHT / 2,
        True,
        "Player",
        game_environment,
    )
    GameSpells.spells[GameEnvironment.FIRSTSPELL] = Spell(
        shape={"type": "circle", "size": 2, "color": "red"},
        effect="damage",
        element="energy",
        modifiers=None,
        description="simple energy projectile",
        is_projectile=True,
        cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
    )
    GameSpells.spells[GameEnvironment.SECONDSPELL] = Spell(
        shape={"type": "circle", "size": 2, "color": "blue"},
        effect="damage",
        element="ice",
        modifiers=[Spell.SLOWMODIFIER],
        description="3 shot energy projectile",
        is_projectile=True,
        cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN * 2,
    )
    # put first spell on player.set_spell
    game_environment.player.set_spell(game_environment.FIRSTSPELL)
    game_environment.player.set_spell(game_environment.SECONDSPELL)
    floor = Surface(
        0,
        game_environment.HEIGHT - game_environment.HEIGHT * 0.1,
        game_environment.WIDTH,
        4,
        game_environment,
    )
    game_environment.surfaces.append(floor)
    game_environment.player_moving_left = False
    game_environment.player_moving_right = False
    game_environment.enemies.append(
        Actor(100, game_environment.HEIGHT / 2, True, "Enemy1", game_environment)
    )


def loop(game_environment: GameEnvironment):
    m1_spell_cooldown_display = SpellCooldownDisplay(
        "M1", game_environment.player.first_spell, game_environment, 10, 10, 30
    )
    m2_spell_cooldown_display = SpellCooldownDisplay(
        "M2", game_environment.player.second_spell, game_environment, 50, 10, 30
    )
    # game loop
    while game_environment.running:
        # logics
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_environment.running = False
            # check if a key is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check if left mouse clicked
                mouse_buttons = pygame.mouse.get_pressed()
                if mouse_buttons[0] == True:
                    game_environment.player.cast_spell(game_environment.FIRSTSPELL)
                if mouse_buttons[2] == True:
                    game_environment.player.cast_spell(game_environment.SECONDSPELL)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_environment.game_paused = not game_environment.game_paused
                # break key event check if game is paused
                if game_environment.game_paused == True:
                    break
                if event.key == pygame.K_a:
                    game_environment.player_moving_left = True
                    # player.update(player.pos.x - game_environment.DEFAULTSPEED, player.pos.y)
                if event.key == pygame.K_d:
                    game_environment.player_moving_right = True
                    # player.update(player.pos.x + game_environment.DEFAULTSPEED, player.pos.y)
                if event.key == pygame.K_w:
                    game_environment.player.update(
                        game_environment.player.pos.x,
                        game_environment.player.pos.y - game_environment.DEFAULTSPEED,
                    )
                if event.key == pygame.K_s:
                    game_environment.player.update(
                        game_environment.player.pos.x,
                        game_environment.player.pos.y + game_environment.DEFAULTSPEED,
                    )
                if event.key == pygame.K_q:
                    pass
            # check if key is still pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    game_environment.player_moving_left = False
                if event.key == pygame.K_d:
                    game_environment.player_moving_right = False
        if game_environment.game_paused == False:
            if game_environment.player.can_update_move():
                speed = game_environment.DEFAULTSPEED
                if game_environment.player_moving_left:
                    game_environment.player.update(
                        game_environment.player.pos.x - speed,
                        game_environment.player.pos.y,
                    )
                if game_environment.player_moving_right:
                    game_environment.player.update(
                        game_environment.player.pos.x + speed,
                        game_environment.player.pos.y,
                    )
            # check if player collides with projectiles
            for projectile in game_environment.global_projectiles:
                # if player.body.colliderect(projectile.body):
                #     global_projectiles.remove(projectile)
                # check if projectiles collide with enemies
                for enemy in game_environment.enemies:
                    if enemy.body.colliderect(projectile.body):
                        game_environment.global_projectiles.remove(projectile)
                        enemy.interact(projectile)
                # check if projectilles collide with surfaces
                for surface in game_environment.surfaces:
                    if surface.body.colliderect(projectile.body):
                        game_environment.global_projectiles.remove(projectile)
            # update gravity
            game_environment.player.pos.y += game_environment.DEFAULTGRAVITY
            for enemy in game_environment.enemies:
                enemy.pos.y += game_environment.DEFAULTGRAVITY
                enemy.update(enemy.pos.x + 2, enemy.pos.y)
            # check if player collides with surfaces
            for surface in game_environment.surfaces:
                if game_environment.player.body.colliderect(surface.body):
                    game_environment.player.pos.y = (
                        surface.pos.y - game_environment.DEFAULTRECTSIZE
                    )
                    game_environment.player.yspeed = 0
                for enemy in game_environment.enemies:
                    if enemy.body.colliderect(surface.body):
                        enemy.pos.y = surface.pos.y - game_environment.DEFAULTRECTSIZE
                        enemy.yspeed = 0

            # updates
            game_environment.player.update(
                game_environment.player.pos.x, game_environment.player.pos.y
            )
            for projectile in game_environment.global_projectiles:
                projectile.update()
            for enemy in game_environment.enemies:
                enemy.update(enemy.pos.x, enemy.pos.y)

        # fill the game_environment.screen with a color to wipe away anything from last frame
        game_environment.screen.fill("black")

        # drawings
        for surface in game_environment.surfaces:
            surface.draw()
        for projectile in game_environment.global_projectiles:
            projectile.draw()
        for enemy in game_environment.enemies:
            enemy.draw()
        game_environment.player.draw()
        m1_spell_cooldown_display.draw()
        m2_spell_cooldown_display.draw()

        # flip() the display to put your work on game_environment.screen
        pygame.display.flip()

        game_environment.clock.tick(60)  # limits FPS to 60
    pygame.quit()


def main():
    game_environment = GameEnvironment()
    setup(game_environment)
    loop(game_environment)


if __name__ == "__main__":
    main()
