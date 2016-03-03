import pygame
import constants
import math

from spritesheet import SpriteSheet

HEART_EMPTY = (0, 47, 53, 45)
HEART_FULL = (0, 94, 53, 45)
HEART_HALF = (0, 0, 53, 45)


class HUD():
    def __init__(self, player):
        self.player = player
        self.hud_items_list = pygame.sprite.Group()
        self.hud_items_list.add(HealthBar(player))

    def update(self):
        """ Update everything in this level."""
        self.hud_items_list.update()

    def draw(self, screen):
        self.hud_items_list.draw(screen)


class HUDItem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data=None):
        pygame.sprite.Sprite.__init__(self)
        if sprite_sheet_data:
            self.image = self.sprite_sheet.get_image(sprite_sheet_data[0],
                                                 sprite_sheet_data[1],
                                                 sprite_sheet_data[2],
                                                 sprite_sheet_data[3])
            self.rect = self.image.get_rect()


class Heart(HUDItem):
    def __init__(self, health):
        HUDItem.__init__(self)
        self.health = health

    def update(self):
        if health == 10:
            self.image = self.sprite_sheet.get_image(HEART_FULL[0],
                                                     HEART_FULL[1],
                                                     HEART_FULL[2],
                                                     HEART_FULL[3])
            self.rect = self.image.get_rect()
        elif health == 5:
            self.image = self.sprite_sheet.get_image(HEART_HALF[0],
                                                     HEART_HALF[1],
                                                     HEART_HALF[2],
                                                     HEART_HALF[3])
            self.rect = self.image.get_rect()
        elif health == 0:
            self.image = self.sprite_sheet.get_image(HEART_EMPTY[0],
                                                     HEART_EMPTY[1],
                                                     HEART_EMPTY[2],
                                                     HEART_EMPTY[3])
            self.rect = self.image.get_rect()
        else:
            print("Error in heart creation")


class HealthBar(pygame.sprite.Group):
    def __init__(self, player):
        pygame.sprite.Group.__init__(self)
        self.player = player
        self.hearts = None

    def update(self):
        health = self.player.health
        self.hearts = []
        no_of_hearts = int(health / 20)
        hearts_tuple = math.modf(no_of_hearts)
        no_of_full_hearts = int(hearts_tuple[1])
        no_of_half_hearts = 0
        if hearts_tuple[0] != 0:
            no_of_half_hearts = 1
        no_of_empty_hearts = 5 - no_of_full_hearts
        for i in range(no_of_full_hearts):
            self.hearts.append(Heart(10))
        for i in range(no_of_half_hearts):
            self.hearts.append(Heart(5))
        for i in range((5-no_of_hearts)):  # Display empty hearts
            self.hearts.append(Heart(0))
