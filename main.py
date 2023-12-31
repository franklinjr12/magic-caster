# Example file showing a basic pygame "game loop"
import pygame
import random
import math
import copy


class GameEnvironment:
    # constants
    WIDTH = 1280
    HEIGHT = 720
    DEFAULTSPEED = 5
    DEFAULTRECTSIZE = 15
    FACINGRIGHT = 1
    FACINGLEFT = -1
    DEFAULTGRAVITY = 2
    DEFAULTPLAYERMOVEDELAY = 50
    DEFAULTPROJECTILESPEED = 3
    DEFAULTPROJECTILESIZE = 3
    FIRSTSPELL = 1
    SECONDSPELL = 2
    THIRDSPELL = 3
    FORTHSPELL = 4
    FIFTHSPELL = 5
    DEFAULTSPELLCOOLDOWN = 1000
    DEFAULTLIFE = 100
    DEFAULTSPELLDAMAGE = 10
    DEFAULTACTORSPEED = 1
    # globals
    global_projectiles = []
    game_paused = False
    player = None
    enemies = []
    surfaces = []
    screen = None
    clock = None
    running = True
    enemies_shoot_at_player = False
    m1_spell_cooldown = None
    m2_spell_cooldown = None
    enemies_ai = []
    background = None


# class Game


class Spell:
    # change these to ids
    SLOWMODIFIER = "slow"
    BURNMODIFIER = "burn"
    WETMODIFIER = "wet"
    POISONMODIFIER = "poison"
    LIGHTNINGMODIFIER = "lightning"
    RADIOACTIVEMODIFIER = "radioactive"
    TOXICMODIFIER = "toxic"

    # change these to ids
    FIREELEMENT = "fire"
    ICEELEMENT = "ice"
    WATERELEMENT = "water"
    EARTHELEMENT = "earth"
    ENERGYELEMENT = "energy"
    VENOMELEMENT = "venom"
    LIGHTNINGELEMENT = "lightning"
    RADIOACTIVEELEMENT = "radioactive"
    TOXICMISTELEMENT = "toxicmist"

    def __init__(
        self,
        shape=None,
        effect=None,
        element=None,
        modifiers=[],
        description=None,
        is_projectile=True,
        cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
        image=None,
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
        self.image = image

    def set_image(image):
        self.image = image

    def is_on_cooldown(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.cooldown_ticks > self.cooldown:
            return False
        return True

    def cast(self, game_environment, x, y, angle):
        if self.is_on_cooldown():
            return
        self.cooldown_ticks = pygame.time.get_ticks()
        if self.description == "simple projectile":
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
                        self.image,
                    )
                )
        elif self.description == "3 shot projectile":
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
                        self.image,
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
                        self.image,
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
                        self.image,
                    )
                )
        elif self.description == "arrow projectile":
            speed_x = game_environment.DEFAULTPROJECTILESPEED * math.cos(
                math.radians(angle)
            )
            speed_y = -(
                game_environment.DEFAULTPROJECTILESPEED * math.sin(math.radians(angle))
            )
            game_environment.global_projectiles.append(
                ArrowProjectile(
                    self,
                    x,
                    y,
                    speed_x,
                    speed_y,
                    self.shape["size"],
                    self.shape["color"],
                    game_environment,
                    self.image,
                )
            )

    def cast_failed_spell(xpos, ypos):
        # will cast some gray particles
        print("failed to cast spell")


# class Spell


class GameSpells:
    spells = []
    spells_square_size = 60
    spells_initial_x = GameEnvironment.WIDTH / 3
    spells_initial_y = GameEnvironment.HEIGHT / 4
    spells_square_spacing = spells_square_size + spells_square_size / 2

    # show all spells on screen when paused
    def show_all_spells(game_environment: GameEnvironment):
        xpos = GameSpells.spells_initial_x
        ypos = GameSpells.spells_initial_y
        size = GameSpells.spells_square_size
        for spell in GameSpells.spells:
            color = spell.shape["color"]
            pygame.draw.rect(
                game_environment.screen,
                color,
                (xpos, ypos, size, size),
            )
            spell_description = spell.description.split(" ")
            y = ypos
            for s in spell_description:
                font = pygame.font.Font("freesansbold.ttf", 12)
                text = font.render(s, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (
                    xpos + size / 2,
                    y + 10,
                )
                game_environment.screen.blit(text, textRect)
                y += 10
            xpos += GameSpells.spells_square_spacing
        # draw empty rectangle around all spells
        pygame.draw.rect(
            game_environment.screen,
            "white",
            (
                GameSpells.spells_initial_x,
                GameSpells.spells_initial_y,
                GameSpells.spells_square_spacing * len(GameSpells.spells),
                GameSpells.spells_square_size,
            ),
            2,
        )


# class GameSpells


class SpellCombination:
    def create_spell_combination(spell1: Spell, spell2: Spell):
        # always create a new instance of Spell class
        spellCombo = Spell()
        # check projectile
        if spell1.is_projectile == True and spell2.is_projectile == True:
            spellCombo.is_projectile = True
            spellCombo.shape = copy.deepcopy(spell1.shape)
            spellCombo.description = copy.deepcopy(spell1.description)
        # check elements
        if (
            spell1.element == Spell.FIREELEMENT and spell2.element == Spell.ICEELEMENT
        ) or (
            spell2.element == Spell.FIREELEMENT and spell1.element == Spell.ICEELEMENT
        ):
            spellCombo.element = Spell.WATERELEMENT
            spellCombo.shape["color"] = "blue"
            spellCombo.modifiers.append(Spell.WETMODIFIER)
        if (
            spell1.element == Spell.FIREELEMENT and spell2.element == Spell.VENOMELEMENT
        ) or (
            spell2.element == Spell.VENOMELEMENT and spell1.element == Spell.FIREELEMENT
        ):
            spellCombo.element = Spell.TOXICMISTELEMENT
            spellCombo.shape["color"] = "green"
            spellCombo.modifiers.append(Spell.TOXICMODIFIER)
            spellCombo.description = "mist projectile"
        if (
            spell1.element == Spell.ENERGYELEMENT and spell2.element == Spell.LIGHTNINGELEMENT
        ) or (
            spell2.element == Spell.LIGHTNINGELEMENT and spell1.element == Spell.ENERGYELEMENT
        ):
            spellCombo.element = Spell.PLASMAELEMENT
            spellCombo.shape["color"] = "white"
            spellCombo.modifiers.append(Spell.PLASMAMODIFIER)
        if (
            spell1.element == Spell.FIREELEMENT
            and spell2.element == Spell.LIGHTNINGELEMENT
        ) or (
            spell2.element == Spell.FIREELEMENT
            and spell1.element == Spell.LIGHTNINGELEMENT
        ):
            spellCombo.element = Spell.RADIOACTIVEELEMENT
            spellCombo.shape["color"] = "green"
            spellCombo.modifiers.append(Spell.RADIOACTIVEMODIFIER)
        # check shape
        if spellCombo.shape == None or spellCombo.element == None:
            return None
        return spellCombo


# class SpellCombination


class Projectile:
    def __init__(
        self, spell, xpos, ypos, xvel, yvel, size, color, game_environment, image=None
    ):
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
        if image != None:
            self.image = pygame.image.load(image)
            self.body = pygame.Rect(
                self.pos.x,
                self.pos.y,
                self.image.get_width(),
                self.image.get_height(),
            )
        else:
            self.image = None

    def draw(self):
        if self.image == None:
            pygame.draw.circle(
                self.game_environment.screen,
                self.bodycolor,
                (self.pos.x, self.pos.y),
                self.size,
            )
        else:
            self.game_environment.screen.blit(self.image, (self.pos.x, self.pos.y))

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.body.x = self.pos.x
        self.body.y = self.pos.y


# class Projectile


class ArrowProjectile(Projectile):
    flipped = None

    def draw(self):
        if self.image == None:
            endx = self.pos.x + self.size * (self.vel.x)
            endy = self.pos.y + self.size * (self.vel.y)
            pygame.draw.line(
                self.game_environment.screen,
                self.bodycolor,
                (self.pos.x, self.pos.y),
                (endx, endy),
            )
        else:
            if self.flipped == None:
                self.flipped = True
                if self.vel.x > 0:
                    self.image = pygame.transform.flip(self.image, True, False)
            self.game_environment.screen.blit(self.image, (self.pos.x, self.pos.y))


# class ArrowProjectile


class Actor:
    def __init__(
        self, xpos=0, ypos=0, show_name=False, actor_name="", game_environment=None
    ):
        self.game_environment = game_environment
        self.pos = pygame.Vector2(xpos, ypos)
        self.image = None
        self.body_size = self.game_environment.DEFAULTRECTSIZE
        self.head_size = self.game_environment.DEFAULTRECTSIZE / 2
        self.body = pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.body_size,
            self.body_size,
        )
        self.head = pygame.Rect(
            self.pos.x + self.game_environment.DEFAULTRECTSIZE,
            self.pos.y,
            self.head_size,
            self.head_size,
        )
        self.bodycolor = "white"
        self.headcolor = "yellow"
        self.facing = self.game_environment.FACINGRIGHT
        self.last_time = pygame.time.get_ticks()
        self.first_spell_last_time = pygame.time.get_ticks()
        self.show_name = show_name
        self.actor_name = actor_name
        self.second_spell_last_time = pygame.time.get_ticks()
        self.life = GameEnvironment.DEFAULTLIFE
        self.modifiers = []
        self.xspeed = 0
        self.yspeed = 0
        self.last_time_burn = 0
        self.first_spell = None
        self.second_spell = None
        self.image = None
        self.show_body_react_contour = False
        self.ShownRect = None

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        width, height = self.image.get_size()
        self.body = pygame.Rect(
            self.pos.x,
            self.pos.y,
            width,
            height,
        )

    def draw(self):
        if self.ShownRect == None:
            self.ShownRect = True
        if self.image != None:
            if self.show_body_react_contour:
                pygame.draw.rect(
                    self.game_environment.screen,
                    "white",
                    self.body,
                    2,
                )
            xsize, ysize = self.image.get_size()
            if self.facing == self.game_environment.FACINGRIGHT:
                self.game_environment.screen.blit(
                    self.image,
                    (self.pos.x, self.pos.y)
                    # self.image, (self.pos.x, self.pos.y - ysize / 1.5)
                )
            else:
                self.game_environment.screen.blit(
                    pygame.transform.flip(self.image, True, False),
                    (self.pos.x, self.pos.y),
                    # (self.pos.x, self.pos.y - ysize / 1.5),
                )
            # show actor name
            if self.show_name:
                font = pygame.font.Font("freesansbold.ttf", 12)
                text = font.render(self.actor_name, True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (
                    self.pos.x + xsize / 2,
                    self.pos.y - 1,
                )
                self.game_environment.screen.blit(text, textRect)
            # draw health bar
            pygame.draw.rect(
                self.game_environment.screen,
                "green",
                (
                    self.pos.x,
                    self.pos.y - 8,
                    self.life / 2,
                    3,
                ),
            )
        else:
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
                    self.pos.x + self.body_size / 2,
                    self.pos.y - self.body_size / 2,
                )
                self.game_environment.screen.blit(text, textRect)
            # draw health bar
            pygame.draw.rect(
                self.game_environment.screen,
                "green",
                (
                    self.pos.x - self.body_size / 2 - 6,
                    self.pos.y - self.body_size / 2 - 8,
                    self.life / 2,
                    3,
                ),
            )

    def set_xspeed(self, speed):
        self.xspeed = speed

    def set_yspeed(self, speed):
        self.yspeed = speed

    def can_take_burn_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_burn > 100:
            self.last_time_burn = pygame.time.get_ticks()
            return True
        return False

    def can_take_poison_damage(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_burn > 100:
            self.last_time_burn = pygame.time.get_ticks()
            return True
        return False

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
        elif self.xspeed != 0:
            if self.xspeed > 0:
                self.facing = self.game_environment.FACINGRIGHT
                if self.modifiers.count(Spell.SLOWMODIFIER) > 0:
                    self.xspeed = self.xspeed - 1
            elif self.xspeed < 0:
                self.facing = self.game_environment.FACINGLEFT
                if self.modifiers.count(Spell.SLOWMODIFIER) > 0:
                    self.xspeed = self.xspeed + 1
            self.pos.x = self.pos.x + self.xspeed
        if self.yspeed != 0:
            self.pos.y = self.pos.y + self.yspeed
        if newy != 0:
            self.pos.y = newy
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
        # check for burn modifier is present on modifiers array
        if self.modifiers.count(Spell.BURNMODIFIER) > 0:
            if self.can_take_burn_damage():
                self.life -= 1
        if self.modifiers.count(Spell.POISONMODIFIER) > 0:
            if self.can_take_poison_damage():
                self.life -= 1

    def can_update_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time > self.game_environment.DEFAULTPLAYERMOVEDELAY:
            self.last_time = pygame.time.get_ticks()
            return True
        return False

    def set_spell(self, position, spell_number):
        spell_number -= 1
        if position == self.game_environment.FIRSTSPELL:
            self.first_spell = copy.deepcopy(GameSpells.spells[spell_number])
        elif position == self.game_environment.SECONDSPELL:
            self.second_spell = copy.deepcopy(GameSpells.spells[spell_number])

    def cast_spell(self, spell, xpos=None, ypos=None):
        angle = None
        if xpos == None and ypos == None:
            # get mouse position
            xpos, ypos = mouse_pos = pygame.mouse.get_pos()
            # get angle between player and mouse
            angle = pygame.math.Vector2(
                mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
            ).angle_to((1, 0))
        else:
            angle = pygame.math.Vector2(xpos - self.pos.x, ypos - self.pos.y).angle_to(
                (1, 0)
            )
        if self.pos.x > xpos:
            xpos = self.pos.x - self.body.width + 3
        else:
            xpos = self.pos.x + self.body.width + 3
        ypos = self.pos.y + self.body.height / 3
        if spell == self.game_environment.FIRSTSPELL:
            self.first_spell.cast(self.game_environment, xpos, ypos, angle)
        if spell == self.game_environment.SECONDSPELL:
            self.second_spell.cast(self.game_environment, xpos, ypos, angle)
        if spell == self.game_environment.THIRDSPELL:
            if self.first_spell != None and self.second_spell != None:
                s = SpellCombination.create_spell_combination(
                    self.first_spell, self.second_spell
                )
                if s != None:
                    s.cast(self.game_environment, xpos, self.pos.y, angle)
                else:
                    Spell.cast_failed_spell(xpos, self.pos.y)

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
        if self.image == None:
            pygame.draw.rect(self.game_environment.screen, self.bodycolor, self.body)
        else:
            # draw self.image as texture to surface
            for i in range(
                int(self.pos.x), int(self.width), int(self.image.get_width())
            ):
                self.game_environment.screen.blit(self.image, (i, self.pos.y))

    def update(self):
        pass

    def set_image(self, image_path):
        self.image = pygame.image.load(image_path)
        width, height = self.image.get_size()
        if self.width < width:
            self.width = width
        if self.height < height:
            self.height = height


# class Surface


class Background:
    def __init__(
        self,
        game_environment: GameEnvironment,
        image_path="assets/images/background.png",
    ):
        self.game_environment = game_environment
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)

    def draw(self):
        # blip self.image along the scren width and height
        for i in range(0, self.game_environment.WIDTH, self.image.get_width()):
            for j in range(0, self.game_environment.HEIGHT, self.image.get_height()):
                self.game_environment.screen.blit(self.image, (i, j))


# class Background


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


# show inputs on screen
class InputsDrawer:
    screen = None

    def drawKey(game_environment, key, xpos, ypos, sizex, sizey):
        color = "white"
        # make rectangle on xpos and ypox
        pygame.draw.rect(
            game_environment.screen,
            color,
            (xpos, ypos, sizex, sizey),
        )
        # draw key letter on rectangle
        font = pygame.font.Font("freesansbold.ttf", 12)
        text = font.render(key, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (
            xpos + sizex / 2,
            ypos + sizey / 2,
        )
        game_environment.screen.blit(text, textRect)
        pass

    def drawKeys(game_environemnt: GameEnvironment):
        xpos = GameEnvironment.WIDTH - 40
        ypos = 60
        size = 30
        InputsDrawer.drawKey(game_environemnt, "D", xpos, ypos, size, size)
        xpos -= 40
        InputsDrawer.drawKey(game_environemnt, "S", xpos, ypos, size, size)
        InputsDrawer.drawKey(game_environemnt, "W", xpos, ypos - 40, size, size)
        xpos -= 40
        InputsDrawer.drawKey(game_environemnt, "A", xpos, ypos, size, size)
        xpos = GameEnvironment.WIDTH - 40
        ypos += 40
        InputsDrawer.drawKey(game_environemnt, "P", xpos, ypos, size, size)
        xpos -= 80
        InputsDrawer.drawKey(game_environemnt, "SPACE", xpos, ypos, size * 2, size)


# class InputsDrawer


class EnemyAI:
    def __init__(self, actor: Actor):
        self.actor = actor
        self.running = False

    def update(self, player: Actor):
        if self.actor.first_spell == None:
            self.actor.set_spell(GameEnvironment.FIRSTSPELL, GameEnvironment.FIRSTSPELL)
        xspeed = GameEnvironment.DEFAULTACTORSPEED * 0.8
        if self.actor.pos.x > player.pos.x:
            xspeed = -xspeed
        if abs(self.actor.pos.x - player.pos.x) < 99:
            self.running = True
            xspeed = -xspeed
        if abs(self.actor.pos.x - player.pos.x) >= 100:
            self.running = False
        self.actor.set_xspeed(xspeed)
        yspeed = GameEnvironment.DEFAULTACTORSPEED * 3
        if self.actor.pos.y > player.pos.y:
            yspeed = -yspeed
        if self.running == True:
            yspeed = 0
        self.actor.set_yspeed(yspeed + GameEnvironment.DEFAULTGRAVITY)
        if self.running == False:
            # shot spell at player pos
            self.actor.cast_spell(
                GameEnvironment.FIRSTSPELL,
                player.pos.x,
                player.pos.y,
            )
        self.actor.update()


# class EnemyAI


def setup(game_environment: GameEnvironment):
    # game setup
    pygame.init()
    game_environment.screen = pygame.display.set_mode(
        (game_environment.WIDTH, game_environment.HEIGHT)
    )
    game_environment.background = Background(game_environment)
    game_environment.clock = pygame.time.Clock()
    game_environment.running = True
    game_environment.player = Actor(
        game_environment.WIDTH / 2,
        game_environment.HEIGHT / 2,
        True,
        "Player",
        game_environment,
    )
    game_environment.player.set_image("assets/images/evil_wizard.png")
    # pre alloc index on GameSpells.spells
    GameSpells.spells.insert(
        GameEnvironment.FIRSTSPELL,
        Spell(
            shape={"type": "circle", "size": 2, "color": "yellow"},
            effect="damage",
            element=Spell.ENERGYELEMENT,
            modifiers=[],
            description="simple projectile",
            is_projectile=True,
            cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
            image="assets/images/first_spell.png",
        ),
    )
    GameSpells.spells.insert(
        GameEnvironment.SECONDSPELL,
        Spell(
            shape={"type": "circle", "size": 2, "color": "blue"},
            effect="damage",
            element=Spell.ICEELEMENT,
            modifiers=[Spell.SLOWMODIFIER],
            description="3 shot projectile",
            is_projectile=True,
            cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN * 2,
            image="assets/images/second_spell.png",
        ),
    )
    GameSpells.spells.insert(
        GameEnvironment.THIRDSPELL,
        Spell(
            shape={"type": "circle", "size": 2, "color": "red"},
            effect="damage",
            element=Spell.FIREELEMENT,
            modifiers=[Spell.BURNMODIFIER],
            description="simple projectile",
            is_projectile=True,
            cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
            image="assets/images/third_spell.png",
        ),
    )
    GameSpells.spells.insert(
        GameEnvironment.FORTHSPELL,
        Spell(
            shape={"type": "line", "size": 5, "color": "green"},
            effect="damage",
            element=Spell.VENOMELEMENT,
            modifiers=[Spell.POISONMODIFIER],
            description="arrow projectile",
            is_projectile=True,
            cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN,
            image="assets/images/forth_spell.png",
        ),
    )
    GameSpells.spells.insert(
        GameEnvironment.FIFTHSPELL,
        Spell(
            shape={"type": "line", "size": 5, "color": "blue"},
            effect="damage",
            element=Spell.LIGHTNINGELEMENT,
            modifiers=[Spell.LIGHTNINGMODIFIER],
            description="arrow projectile",
            is_projectile=True,
            cooldown=GameEnvironment.DEFAULTSPELLCOOLDOWN / 2,
            image="assets/images/fifth_spell.png",
        ),
    )
    # put first spell on player.set_spell
    game_environment.player.set_spell(
        game_environment.FIRSTSPELL, game_environment.FIRSTSPELL
    )
    game_environment.player.set_spell(
        game_environment.SECONDSPELL, game_environment.SECONDSPELL
    )
    floor = Surface(
        0,
        game_environment.HEIGHT - game_environment.HEIGHT * 0.1,
        game_environment.WIDTH,
        4,
        game_environment,
    )
    floor.set_image("assets/images/floor_2.png")
    platform1 = Surface(
        game_environment.WIDTH / 2 + 100,
        game_environment.HEIGHT / 2,
        game_environment.WIDTH,
        4,
        game_environment,
    )
    platform1.set_image("assets/images/floor_2.png")
    platform2 = Surface(
        0,
        game_environment.HEIGHT / 4,
        game_environment.WIDTH / 2 - 300,
        4,
        game_environment,
    )
    platform2.set_image("assets/images/floor_2.png")
    game_environment.surfaces.append(floor)
    game_environment.surfaces.append(platform1)
    game_environment.surfaces.append(platform2)
    game_environment.player_moving_left = False
    game_environment.player_moving_right = False
    game_environment.player_moving_up = False
    game_environment.player_moving_down = False

    # enemies
    en1 = Actor(100, game_environment.HEIGHT / 2, True, "Enemy1", game_environment)
    en1.set_image("assets/images/New_Piskel-1.png")
    ai1 = EnemyAI(en1)
    game_environment.enemies.append(en1)
    game_environment.enemies_ai.append(ai1)

    game_environment.m1_spell_cooldown = SpellCooldownDisplay(
        "M1", game_environment.player.first_spell, game_environment, 10, 10, 30
    )
    game_environment.m2_spell_cooldown = SpellCooldownDisplay(
        "M2", game_environment.player.second_spell, game_environment, 50, 10, 30
    )


def loop(game_environment: GameEnvironment):
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
                mouse_pos = pygame.mouse.get_pos()
                if game_environment.game_paused == True:
                    # check if mouse clicked on spell
                    spell_position = GameEnvironment.FIRSTSPELL
                    if mouse_buttons[2] == True:
                        spell_position = GameEnvironment.SECONDSPELL
                    xpos = GameSpells.spells_initial_x
                    ypos = GameSpells.spells_initial_y
                    for spell in GameSpells.spells:
                        if (
                            xpos < mouse_pos[0] < xpos + GameSpells.spells_square_size
                            and ypos
                            < mouse_pos[1]
                            < ypos + GameSpells.spells_square_size
                        ):
                            game_environment.player.set_spell(
                                spell_position,
                                GameSpells.spells.index(spell) + 1,
                            )
                            if spell_position == GameEnvironment.FIRSTSPELL:
                                game_environment.m1_spell_cooldown = (
                                    SpellCooldownDisplay(
                                        "M1",
                                        game_environment.player.first_spell,
                                        game_environment,
                                        10,
                                        10,
                                        30,
                                    )
                                )
                            else:
                                game_environment.m2_spell_cooldown = (
                                    SpellCooldownDisplay(
                                        "M2",
                                        game_environment.player.second_spell,
                                        game_environment,
                                        50,
                                        10,
                                        30,
                                    )
                                )
                            break
                        xpos += GameSpells.spells_square_spacing

                        # check if mouse clicked on spell
                    break
                if mouse_buttons[0] == True:
                    game_environment.player.cast_spell(game_environment.FIRSTSPELL)
                if mouse_buttons[2] == True:
                    game_environment.player.cast_spell(game_environment.SECONDSPELL)
                if mouse_buttons[1] == True:
                    game_environment.player.cast_spell()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_environment.game_paused = not game_environment.game_paused
                # break key event check if game is paused
                if game_environment.game_paused == True:
                    break
                if event.key == pygame.K_a:
                    game_environment.player_moving_left = True
                if event.key == pygame.K_d:
                    game_environment.player_moving_right = True
                if event.key == pygame.K_w:
                    game_environment.player_moving_up = True
                if event.key == pygame.K_s:
                    game_environment.player_moving_down = True
                if event.key == pygame.K_q:
                    pass
                if event.key == pygame.K_p:
                    GameEnvironment.enemies_shoot_at_player = (
                        not GameEnvironment.enemies_shoot_at_player
                    )
            # check if key is still pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    game_environment.player_moving_left = False
                if event.key == pygame.K_d:
                    game_environment.player_moving_right = False
                if event.key == pygame.K_w:
                    game_environment.player_moving_up = False
                if event.key == pygame.K_s:
                    game_environment.player_moving_down = False
        if game_environment.game_paused == False:
            if game_environment.player.can_update_move():
                xspeed = game_environment.DEFAULTACTORSPEED
                if game_environment.player_moving_left:
                    game_environment.player.set_xspeed(-xspeed)
                elif game_environment.player_moving_right:
                    game_environment.player.set_xspeed(xspeed)
                else:
                    game_environment.player.set_xspeed(0)
                if game_environment.player_moving_up:
                    game_environment.player.set_yspeed(
                        -GameEnvironment.DEFAULTACTORSPEED * 3
                    )
                elif game_environment.player_moving_down:
                    game_environment.player.set_yspeed(
                        GameEnvironment.DEFAULTACTORSPEED
                    )
                else:
                    game_environment.player.set_yspeed(0)
            # make enemy shoot at player
            if GameEnvironment.enemies_shoot_at_player == True:
                for enemy in game_environment.enemies_ai:
                    enemy.update(game_environment.player)

            # updates
            game_environment.player.update()
            for projectile in game_environment.global_projectiles:
                projectile.update()
            for enemy in game_environment.enemies:
                if enemy.life <= 0:
                    game_environment.enemies.remove(enemy)
                else:
                    enemy.update(enemy.pos.x, enemy.pos.y)

            # check if player collides with projectiles
            for projectile in game_environment.global_projectiles:
                if game_environment.player.body.colliderect(projectile.body):
                    game_environment.global_projectiles.remove(projectile)
                    game_environment.player.interact(projectile)
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
                if GameEnvironment.enemies_shoot_at_player == False:
                    enemy.pos.y += game_environment.DEFAULTGRAVITY
                    enemy.update(enemy.pos.x + random.randint(-3, 3), enemy.pos.y)
            # check if player collides with surfaces
            for surface in game_environment.surfaces:
                player = game_environment.player
                if (
                    player.pos.x > surface.body.x
                    and player.pos.x < surface.body.x + surface.body.width
                ):
                    if (
                        player.pos.y > surface.body.y
                        and player.pos.y < surface.body.y + surface.body.height
                    ):
                        player.pos.x -= player.xspeed
                if game_environment.player.body.colliderect(surface.body):
                    if game_environment.player.yspeed < 0:
                        game_environment.player.yspeed = 0
                    else:
                        game_environment.player.pos.y = (
                            surface.pos.y - game_environment.player.body.height
                        )
                    game_environment.player.yspeed = 0
                for enemy in game_environment.enemies:
                    if enemy.body.colliderect(surface.body):
                        enemy.pos.y = surface.pos.y - enemy.body.height
                        enemy.yspeed = 0

        # drawings
        # fill the game_environment.screen with a color to wipe away anything from last frame
        # game_environment.screen.fill("black")
        game_environment.background.draw()

        if game_environment.game_paused == True:
            mouse_pos = pygame.mouse.get_pos()
            GameSpells.show_all_spells(game_environment)
            for enemy in game_environment.enemies:
                if enemy.body.collidepoint(mouse_pos[0], mouse_pos[1]):
                    # show enemy modifiers
                    modifiers_str = "modifiers:"
                    for modifier in enemy.modifiers:
                        modifiers_str += modifier + " "
                    font = pygame.font.Font("freesansbold.ttf", 12)
                    text = font.render(modifiers_str, True, (255, 255, 255))
                    textRect = text.get_rect()
                    textRect.center = (
                        mouse_pos[0],
                        mouse_pos[1] - 50,
                    )
                    game_environment.screen.blit(text, textRect)
            # show player modifiers
            if game_environment.player.body.collidepoint(mouse_pos[0], mouse_pos[1]):
                modifiers_str = "modifiers:"
                for modifier in game_environment.player.modifiers:
                    modifiers_str += modifier + " "
                font = pygame.font.Font("freesansbold.ttf", 12)
                text = font.render(modifiers_str, True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (
                    mouse_pos[0],
                    mouse_pos[1] - 50,
                )
                game_environment.screen.blit(text, textRect)

        for surface in game_environment.surfaces:
            surface.draw()
        for projectile in game_environment.global_projectiles:
            projectile.draw()
        for enemy in game_environment.enemies:
            enemy.draw()
        game_environment.player.draw()
        game_environment.m1_spell_cooldown.draw()
        game_environment.m2_spell_cooldown.draw()
        InputsDrawer.drawKeys(game_environment)

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
