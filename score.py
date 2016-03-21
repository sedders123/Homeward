import pygame
import constants
import math
import structures

from spritesheet import SpriteSheet

ZERO  = (230, 0, 30, 38)
ONE   = (196, 41, 26, 37)
TWO   = (55, 98, 32, 38)
THREE = (239, 80, 28, 38)
FOUR  = (238, 122, 29, 38)
FIVE  = (238, 162, 28, 38)
SIX   = (230, 40, 20, 38)
SEVEN = (226, 206, 32, 39)
EIGHT = (192, 206, 32, 40)
NINE  = (196, 0, 32, 39)


class ScoreHUD():
    def __init__(self, player):
        self.player = player
        self.score_draw_list = pygame.sprite.OrderedUpdates()
        self.numbers = []
        self.score_tracker()

    def update(self):
        """ Update everything in this level."""
        self.score_draw_list.update()
        if self.player.score > self.last_score:
            self.score_tracker()

    def draw(self, screen):
        for i, number in enumerate(self.score_draw_list.sprites()):
            number.rect.y = 10
            number.rect.x = ((i+0.01)*55) + 700
        self.score_draw_list.draw(screen)

    def score_tracker(self):
        score = self.player.score
        self.last_score = score

        for number in self.numbers:
            self.score_draw_list.remove(number)
        self.numbers = []

        score = str(score)
        for integer in score:
            number = Number(int(integer))
            self.numbers.append(number)
            self.score_draw_list.add(number)

        for number in self.numbers:
            self.score_draw_list.add(number)


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


class Number(HUDItem):
    def __init__(self, value):
        HUDItem.__init__(self)
        self.value = value
        self.get_image()

    def __repr__(self):
        return "<Number: {}>".format(self.value)

    def update(self):
        self.get_image()

    def get_image(self):
        value = self.value
        if value == 0:
            self.image = self.sprite_sheet.get_image(ZERO[0],
                                                     ZERO[1],
                                                     ZERO[2],
                                                     ZERO[3])
            self.rect = self.image.get_rect()
        elif value == 1:
            self.image = self.sprite_sheet.get_image(ONE[0],
                                                     ONE[1],
                                                     ONE[2],
                                                     ONE[3])
            self.rect = self.image.get_rect()
        elif value == 2:
            self.image = self.sprite_sheet.get_image(TWO[0],
                                                     TWO[1],
                                                     TWO[2],
                                                     TWO[3])
            self.rect = self.image.get_rect()
        elif value == 3:
            self.image = self.sprite_sheet.get_image(THREE[0],
                                                     THREE[1],
                                                     THREE[2],
                                                     THREE[3])
            self.rect = self.image.get_rect()
        elif value == 4:
            self.image = self.sprite_sheet.get_image(FOUR[0],
                                                     FOUR[1],
                                                     FOUR[2],
                                                     FOUR[3])
            self.rect = self.image.get_rect()
        elif value == 5:
            self.image = self.sprite_sheet.get_image(FIVE[0],
                                                     FIVE[1],
                                                     FIVE[2],
                                                     FIVE[3])
            self.rect = self.image.get_rect()
        elif value == 6:
            self.image = self.sprite_sheet.get_image(SIX[0],
                                                     SIX[1],
                                                     SIX[2],
                                                     SIX[3])
            self.rect = self.image.get_rect()
        elif value == 7:
            self.image = self.sprite_sheet.get_image(SEVEN[0],
                                                     SEVEN[1],
                                                     SEVEN[2],
                                                     SEVEN[3])
            self.rect = self.image.get_rect()
        elif value == 8:
            self.image = self.sprite_sheet.get_image(EIGHT[0],
                                                     EIGHT[1],
                                                     EIGHT[2],
                                                     EIGHT[3])
            self.rect = self.image.get_rect()
        elif value == 9:
            self.image = self.sprite_sheet.get_image(NINE[0],
                                                     NINE[1],
                                                     NINE[2],
                                                     NINE[3])
            self.rect = self.image.get_rect()
        else:
            print("Error in score creation")
            print("Value: {}".format(value))
            print(type(value))
