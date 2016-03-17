import pygame
import math

import constants
import structures
import enemies


class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

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
        """ Constructor. Pass in a handle to player. Needed for when moving structures
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.score = 0

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background,(self.world_shift // 3,0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

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


# Create structures for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500  # equals width of image + width of window? Needs testing

        enemy_list = [("FLY", 700, 250), ("SLIME", 700, 100)]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [ (structures.INVISIBLE_WALL, -80, 0),
                  (structures.GRASS_LEFT, 770, 450),
                  (structures.GRASS_MIDDLE, 840, 450),
                  (structures.GRASS_RIGHT, 910, 450),
                  (structures.STONE_PLATFORM_LEFT, 1120, 300),
                  (structures.STONE_PLATFORM_MIDDLE, 1190, 300),
                  (structures.STONE_PLATFORM_RIGHT, 1260, 300),
                  ]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        second_floor = self.make_floor(structures.GRASS_MIDDLE, 1050, self.FLOOR, 1000)
        floors.append(first_floor)
        floors.append(second_floor)

        for floor in floors:
            for platform in floor:
                level.append(platform)

        # Go through the array above and add structures
        for platform in level:
            block = structures.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        for enemy in enemy_list:
            if enemy[0] == "FLY":
                block = enemies.Fly()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 300
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)
            elif enemy[0] == "SLIME":
                block = enemies.Slime()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 100
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)

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
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000


        # Array with type of platform, and x, y location of the platform.
        structures_list = [ [structures.INVISIBLE_WALL, -70, 10],
                  [structures.STONE_PLATFORM_LEFT, 500, 550],
                  [structures.STONE_PLATFORM_MIDDLE, 570, 550],
                  [structures.STONE_PLATFORM_RIGHT, 640, 550],
                  [structures.GRASS_LEFT, 800, 400],
                  [structures.GRASS_MIDDLE, 870, 400],
                  [structures.GRASS_RIGHT, 940, 400],
                  [structures.GRASS_LEFT, 1000, 500],
                  [structures.GRASS_MIDDLE, 1070, 500],
                  [structures.GRASS_RIGHT, 1140, 500],
                  [structures.STONE_PLATFORM_LEFT, 1120, 280],
                  [structures.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [structures.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add structures
        for platform in structures_list:
            block = structures.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)


        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

class Level_03(Level):
    """ Definition for level 3. """

    def __init__(self, player):
        """ Create level 3. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("resources/background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500  # equals width of image + width of window? Needs testing

        enemy_list = [("FLY", 600, 250), ("SLIME", 1100, 550), ("SLIME", 1120, 175), ("FLY", 1400, 210), ("SLIME", 1870, 550)]

        platforms = []  # Anything not on ground (excluding spikes)

        # Array with type of platform, and x, y location of the platform.
        level = [ (structures.INVISIBLE_WALL, -80, 0),
                  (structures.STONE_PLATFORM_LEFT, 700, 450),
                  (structures.STONE_PLATFORM_MIDDLE, 770, 450),
                  (structures.STONE_PLATFORM_RIGHT, 840, 450),
                  (structures.STONE_PLATFORM_LEFT, 1120, 200),
                  (structures.STONE_PLATFORM_MIDDLE, 1190, 200),
                  (structures.STONE_PLATFORM_MIDDLE, 1260, 200),
                  (structures.STONE_PLATFORM_RIGHT, 1300, 200),
                  (structures.STONE_PLATFORM_LEFT, 1870, 425),
                  (structures.STONE_PLATFORM_MIDDLE, 1940, 425),
                  (structures.STONE_PLATFORM_RIGHT, 2010, 425),

                  ]
        floors = []
        first_floor = self.make_floor(structures.GRASS_MIDDLE, -5, self.FLOOR, 1000)
        second_floor = self.make_floor(structures.GRASS_MIDDLE, 1050, self.FLOOR, 500)
        third_floor = self.make_floor(structures.GRASS_MIDDLE, 1700, self.FLOOR, 1000)
        floors.append(first_floor)
        floors.append(second_floor)
        floors.append(third_floor)

        for floor in floors:
            for platform in floor:
                level.append(platform)

        # Go through the array above and add structures
        for platform in level:
            block = structures.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        for enemy in enemy_list:
            if enemy[0] == "FLY":
                block = enemies.Fly()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 300
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)
            elif enemy[0] == "SLIME":
                block = enemies.Slime()
                block.rect.x = enemy[1]
                block.rect.y = enemy[2]
                block.boundary_left = enemy[1]
                block.boundary_right = enemy[1] + 200
                block.player = self.player
                block.level = self
                self.enemy_list.add(block)


        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1400
        block.rect.y = 300
        block.boundary_left = 1400
        block.boundary_right = 1600
        block.change_x = 1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving platform
        block = structures.MovingPlatform(structures.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1025
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
