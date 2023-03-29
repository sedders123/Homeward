import pygame
import math

import constants
import structures
from enemies import Fly, Slime


class Level:
    """This is a generic super-class used to define a level.
    Create a child class for each level with level-specific
    info."""

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    FLOOR = 575
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    level_limit = -1000

    def __init__(self, player):
        """Constructor. Pass in a handle to player. Needed for when moving structures
        collide with the player."""
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.score = 0

    # Update everythign on this level
    def update(self):
        """Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """Draw everything on this level."""

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """When the user moves left/right and we need to scroll everything:"""

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def make_floor(self, structure, x, y, length):
        floor = []
        number_of_platforms = math.ceil(length // 70)
        for i in range(number_of_platforms):
            platform_x = i * 70 + x
            platform = (structure, platform_x, y)
            floor.append(platform)
        return floor

    def construct_world(self, level, floors, level_enemies, y_offset=0):
        for floor in floors:
            for platform in floor:
                level.append(platform)

        # Go through the array above and add structures
        for platform in level:
            block = structures.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2] - y_offset
            block.player = self.player
            self.platform_list.add(block)

        for enemy in level_enemies:
            if enemy[0] == Slime.name:
                block = Slime()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 100
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)
            elif enemy[0] == Fly.name:
                block = Fly()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 300
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)


class MainMenu(Level):
    """Definition for Main Menu"""

    def __init__(self, player):
        """Create Main Menu level."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/main_menu.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = 100  # equals width of image + width of window? Needs testing

        # Array with type of platform, and x, y location of the platform.
        level = [(structures.INVISIBLE_WALL, 0, 0)]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        floors.append(first_floor)

        self.construct_world(level, floors, [], y_offset=15)


# Create structures for the level
class LevelTutorial(Level):
    """Definition for level tutorial."""

    def __init__(self, player):
        """Create level tutorial."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load(
            "resources/background_tutorial.png"
        ).convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = (
            -2500
        )  # equals width of image + width of window? Needs testing

        enemy_list = [(Fly.name, 700, 250), (Slime.name, 1600, 550)]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [
            (structures.INVISIBLE_WALL, 0, 0),
            (structures.GRASS_LEFT, 770, 450),
            (structures.GRASS_MIDDLE, 840, 450),
            (structures.GRASS_RIGHT, 910, 450),
            (structures.STONE_PLATFORM_LEFT, 1120, 300),
            (structures.STONE_PLATFORM_MIDDLE, 1190, 300),
            (structures.STONE_PLATFORM_RIGHT, 1260, 300),
        ]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1050)
        second_floor = self.make_floor(structures.GRASS_MIDDLE, 1040, self.FLOOR, 2600)
        floors.append(first_floor)
        floors.append(second_floor)

        self.construct_world(level, floors, enemy_list)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 300
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


# Create structures for the level
class Level_01(Level):
    """Definition for level 1."""

    def __init__(self, player):
        """Create level 1."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/grass_background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = (
            -2500
        )  # equals width of image + width of window? Needs testing

        enemy_list = [
            (Fly.name, 700, 280),
            (Slime.name, 1120, 275),
            (Fly.name, 2800, 140),
        ]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [
            (structures.INVISIBLE_WALL, 0, 0),
            (structures.STONE_PLATFORM_LEFT, 770, 450),
            (structures.STONE_PLATFORM_MIDDLE, 840, 450),
            (structures.STONE_PLATFORM_RIGHT, 910, 450),
            (structures.STONE_PLATFORM_LEFT, 1120, 300),
            (structures.STONE_PLATFORM_MIDDLE, 1190, 300),
            (structures.STONE_PLATFORM_RIGHT, 1260, 300),
            (structures.STONE_PLATFORM_LEFT, 2020, 430),
            (structures.STONE_PLATFORM_MIDDLE, 2090, 430),
            (structures.STONE_PLATFORM_RIGHT, 2160, 430),
        ]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        second_floor = self.make_floor(structures.GRASS_MIDDLE, 1900, self.FLOOR, 400)
        third_floor = self.make_floor(structures.GRASS_MIDDLE, 3000, self.FLOOR, 700)
        floors.append(first_floor)
        floors.append(second_floor)
        floors.append(third_floor)

        self.construct_world(level, floors, enemy_list)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1350
        block.rect.y = 300
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1900
        block.rect.y = 300
        block.boundary_left = 1650
        block.boundary_right = 1900
        block.change_x = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1450
        block.rect.y = 180
        block.boundary_left = 1450
        block.boundary_right = 1800
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1450
        block.rect.y = 20
        block.boundary_left = 1450
        block.boundary_right = 1800
        block.change_x = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2340
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2540
        block.rect.y = 200
        block.boundary_top = 200
        block.boundary_bottom = 500
        block.change_y = -3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2740
        block.rect.y = 200
        block.boundary_top = 50
        block.boundary_bottom = 500
        block.change_y = -8
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2800
        block.rect.y = 200
        block.boundary_left = 2800
        block.boundary_right = 3000
        block.change_x = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


# Create structures for the level
class Level_02(Level):
    """Definition for level 2."""

    def __init__(self, player):
        """Create level 2."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/ice_background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1200

        enemy_list = [
            (Fly.name, 600, 250),
            (Slime.name, 800, 375),
            (Slime.name, 1000, 225),
            (Fly.name, 1400, 210),
            (Slime.name, 1800, 405),
        ]

        # Array with type of platform, and x, y location of the platform.
        structures_list = [
            [structures.INVISIBLE_WALL, -70, 10],
            [structures.STONE_PLATFORM_LEFT, 420, 520],
            [structures.STONE_PLATFORM_MIDDLE, 490, 520],
            [structures.STONE_PLATFORM_MIDDLE, 540, 520],
            [structures.STONE_PLATFORM_RIGHT, 610, 520],
            [structures.STONE_PLATFORM_LEFT, 800, 400],
            [structures.STONE_PLATFORM_MIDDLE, 870, 400],
            [structures.STONE_PLATFORM_RIGHT, 940, 400],
            [structures.STONE_PLATFORM_LEFT, 1000, 250],
            [structures.STONE_PLATFORM_MIDDLE, 1070, 250],
            [structures.STONE_PLATFORM_RIGHT, 1140, 250],
            [structures.STONE_PLATFORM_LEFT, 1120, 120],
            [structures.STONE_PLATFORM_MIDDLE, 1190, 120],
            [structures.STONE_PLATFORM_RIGHT, 1260, 120],
            [structures.STONE_PLATFORM_LEFT, 500, 130],
            [structures.STONE_PLATFORM_MIDDLE, 570, 130],
            [structures.STONE_PLATFORM_RIGHT, 640, 130],
            [structures.STONE_PLATFORM_LEFT, 1600, 330],
            [structures.STONE_PLATFORM_RIGHT, 1670, 330],
            [structures.STONE_PLATFORM_LEFT, 1800, 430],
            [structures.STONE_PLATFORM_MIDDLE, 1870, 430],
            [structures.STONE_PLATFORM_RIGHT, 1940, 430],
        ]
        floors = []
        first_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, -5, self.FLOOR, 460
        )
        second_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, 2000, self.FLOOR, 300
        )
        floors.append(first_floor)
        floors.append(second_floor)

        self.construct_world(structures_list, floors, enemy_list)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_03(Level):
    """Definition for level 3."""

    def __init__(self, player):
        """Create level 3."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/grass_background.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = (
            -2500
        )  # equals width of image + width of window? Needs testing

        enemy_list = [
            (Fly.name, 600, 250),
            (Slime.name, 1100, 550),
            (Slime.name, 1120, 175),
            (Fly.name, 1400, 210),
            (Slime.name, 1870, 550),
        ]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [
            (structures.INVISIBLE_WALL, 0, 0),
            (structures.GRASS_LEFT, 700, 450),
            (structures.GRASS_MIDDLE, 770, 450),
            (structures.GRASS_RIGHT, 840, 450),
            (structures.GRASS_LEFT, 1120, 200),
            (structures.GRASS_MIDDLE, 1190, 200),
            (structures.GRASS_MIDDLE, 1260, 200),
            (structures.GRASS_RIGHT, 1330, 200),
            (structures.GRASS_LEFT, 1870, 400),
            (structures.GRASS_MIDDLE, 1940, 400),
            (structures.GRASS_RIGHT, 2010, 400),
        ]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        second_floor = self.make_floor(structures.GRASS_MIDDLE, 1050, self.FLOOR, 500)
        third_floor = self.make_floor(structures.GRASS_MIDDLE, 1750, self.FLOOR, 600)
        fourth_floor = self.make_floor(structures.GRASS_MIDDLE, 3000, self.FLOOR, 600)
        floors.append(first_floor)
        floors.append(second_floor)
        floors.append(third_floor)
        floors.append(fourth_floor)

        self.construct_world(level, floors, enemy_list)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 1400
        block.rect.y = 300
        block.boundary_left = 1400
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 1025
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 2140
        block.rect.y = 425
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 2340
        block.rect.y = 200
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = 3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 2540
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.GRASS_ROUND)
        block.rect.x = 2740
        block.rect.y = 100
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = 3
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_04(Level):
    """Definition for level 4."""

    def __init__(self, player):
        """Create level 4."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background_03.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = (
            -2500
        )  # equals width of image + width of window? Needs testing

        enemy_list = [
            (Fly.name, 600, 250),
            (Slime.name, 1000, 275),
            (Fly.name, 1400, 210),
            (Slime.name, 1870, 550),
        ]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [
            (structures.INVISIBLE_WALL, -80, 0),
            (structures.STONE_CLIFF_LEFT, 700, 450),
            (structures.STONE_CLIFF_MIDDLE, 770, 450),
            (structures.STONE_CLIFF_RIGHT, 840, 450),
            (structures.STONE_CLIFF_LEFT, 1000, 300),
            (structures.STONE_CLIFF_MIDDLE, 1070, 300),
            (structures.STONE_CLIFF_MIDDLE, 1140, 300),
            (structures.STONE_CLIFF_RIGHT, 1210, 300),
            (structures.STONE_CLIFF_LEFT, 1870, 100),
            (structures.STONE_CLIFF_MIDDLE, 1940, 100),
            (structures.STONE_CLIFF_RIGHT, 2010, 100),
            (structures.STONE_CLIFF_LEFT, 2300, 250),
            (structures.STONE_CLIFF_RIGHT, 2370, 250),
            (structures.STONE_CLIFF_LEFT, 2650, 350),
            (structures.STONE_CLIFF_RIGHT, 2720, 350),
        ]
        floors = []
        first_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, -5, self.FLOOR, 1000
        )
        second_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, 1050, self.FLOOR, 500
        )
        third_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, 1700, self.FLOOR, 600
        )
        fourth_floor = self.make_floor(
            structures.STONE_CLIFF_MIDDLE, 2900, self.FLOOR, 600
        )
        floors.append(first_floor)
        floors.append(second_floor)
        floors.append(third_floor)
        floors.append(fourth_floor)

        self.construct_world(level, floors, enemy_list)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1280
        block.rect.y = 300
        block.boundary_left = 1280
        block.boundary_right = 1480
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1600
        block.rect.y = 400
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 2840
        block.rect.y = 320
        block.boundary_top = 100
        block.boundary_bottom = 500
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class GameOver(Level):
    """Definition for Game Over Menu"""

    def __init__(self, player):
        """Create Game Over level."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/game_over.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = 800  # equals width of image + width of window? Needs testing

        # Array with type of platform, and x, y location of the platform.
        level = [(structures.INVISIBLE_WALL, 0, 0), (structures.INVISIBLE_WALL, 800, 0)]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        floors.append(first_floor)

        self.construct_world(level, floors, [], y_offset=15)


class YouWin(Level):
    """Definition for You WIn Menu"""

    def __init__(self, player):
        """Create You Win level."""

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/you_win.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = (
            -800
        )  # equals width of image + width of window? Needs testing

        # Array with type of platform, and x, y location of the platform.
        level = [(structures.INVISIBLE_WALL, 0, 0), (structures.INVISIBLE_WALL, 590, 0)]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        floors.append(first_floor)

        self.construct_world(level, floors, [], y_offset=15)
