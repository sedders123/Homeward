import pygame

from spritesheet import SpriteSheet

FLY_DEAD = (143, 0, 59, 33)
FLY_WINGS_UP = (0, 32, 72, 36)
FLY_WINGS_DOWN = (0, 0, 75, 31)


class Enemy(pygame.sprite.Sprite):
    """Enemy"""

    def __init__(self, sprite_sheet_data=None):
        """ Enemy constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        self.sprite_sheet = SpriteSheet("resources/enemies_spritesheet.png")
        # Grab the image for this platform
        if sprite_sheet_data:
            self.image = self.sprite_sheet.get_image(sprite_sheet_data[0],
                                                sprite_sheet_data[1],
                                                sprite_sheet_data[2],
                                                sprite_sheet_data[3])
            self.rect = self.image.get_rect()

        self.level = None


class Fly(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.change_x = 1

        self.boundary_left = 0
        self.boundary_right = 0

        self.frames_left = []
        image = self.sprite_sheet.get_image(FLY_WINGS_UP[0],
                                           FLY_WINGS_UP[1],
                                           FLY_WINGS_UP[2],
                                           FLY_WINGS_UP[3])
        self.frames_left.append(image)
        image = self.sprite_sheet.get_image(FLY_WINGS_DOWN[0],
                                           FLY_WINGS_DOWN[1],
                                           FLY_WINGS_DOWN[2],
                                           FLY_WINGS_DOWN[3])
        self.frames_left.append(image)

        self.frames_right = []

        image = self.sprite_sheet.get_image(FLY_WINGS_UP[0],
                                           FLY_WINGS_UP[1],
                                           FLY_WINGS_UP[2],
                                           FLY_WINGS_UP[3])
        image = pygame.transform.flip(image, True, False)
        self.frames_right.append(image)

        image = self.sprite_sheet.get_image(FLY_WINGS_DOWN[0],
                                            FLY_WINGS_DOWN[1],
                                            FLY_WINGS_DOWN[2],
                                            FLY_WINGS_DOWN[3])
        image = pygame.transform.flip(image, True, False)
        self.frames_right.append(image)

        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the Enemy."""
        pos = self.rect.x - self.level.world_shift
        frame = (pos // 30) % 2  # 2 numbers of states
        if self.change_x < 1:
            self.image = self.frames_left[frame]
        else:
            self.image = self.frames_right[frame]

        self.rect.x += self.change_x
        hit = pygame.sprite.collide_rect(self, self.player)

        if hit:
            print("Hit")

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
