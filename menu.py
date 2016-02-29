import pygame

from spritesheet import SpriteSheet

class Menu():

    def __init__(self):
        pass

    def draw(self, screen):
        # Draw the background
        screen.fill(constants.BLUE)
        screen.blit(self.background,(0,0))

        self.menu_items.draw(screen)


class MenuItem(pygame.sprite.Sprite):

    def __init__(self, sprite_sheet_data):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("resources/menu_items.png")  # To be created
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])  # x, y, height, width of menu item
        self.rect = self.image.get_rect()
