import pygame
import constants
import math
import structures

from spritesheet import SpriteSheet

HEART_EMPTY = (0, 47, 53, 45)
HEART_FULL = (0, 94, 53, 45)
HEART_HALF = (0, 0, 53, 45)


class HUD():
    def __init__(self, player):
        self.player = player
        self.health_draw_list = pygame.sprite.OrderedUpdates()
        self.hearts = []
        self.health_bar()

    def update(self):
        """ Update everything in this level."""
        self.health_draw_list.update()
        if self.player.health < self.last_health:
            self.health_bar()

    def draw(self, screen):
        for i, heart in enumerate(self.health_draw_list.sprites()):
            heart.rect.y = 10
            heart.rect.x = (i+0.1)*55
        self.health_draw_list.draw(screen)

    def health_bar(self):
        health = self.player.health
        self.last_health = health

        for heart in self.hearts:
            self.health_draw_list.remove(heart)
        self.hearts = []

        no_of_full_hearts, no_of_half_hearts = self.calculate_no_hearts(health)
        no_of_empty_hearts = 5 - (no_of_full_hearts + no_of_half_hearts)

        # print("Health: {}".format(health))
        # print("Full: {}".format(no_of_full_hearts))
        # print("Half: {}".format(no_of_half_hearts))
        # print("Empty: {}".format(no_of_empty_hearts))

        for i in range(no_of_full_hearts):
            self.hearts.append(Heart(10))
        for i in range(no_of_half_hearts):
            self.hearts.append(Heart(5))
        for i in range((no_of_empty_hearts)):  # Display empty hearts
            self.hearts.append(Heart(0))

        for heart in self.hearts:
            self.health_draw_list.add(heart)

    def calculate_no_hearts(self, health):
        no_of_hearts = health / 20
        hearts_tuple = math.modf(no_of_hearts)
        no_of_full_hearts = int(hearts_tuple[1])
        if hearts_tuple[0] != 0:
            no_of_half_hearts = 1
        else:
            no_of_half_hearts = 0
        return no_of_full_hearts, no_of_half_hearts


class HUDItem(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_data=None):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_sheet = SpriteSheet("resources/hud_spritesheet.png")
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
        self.get_image()

    def __repr__(self):
        return "<Heart: {}>".format(self.health)

    def update(self):
        self.get_image()

    def get_image(self):
        health = self.health
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

    def update(self):
        pass

    def draw(self, screen):
        for i, heart in enumerate(self.sprites()):
            heart.rect.y = 100
            heart.rect.x = 500 + (i+1)*10
            heart.draw(screen)
            print("Test")
