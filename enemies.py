import pygame
import constants

from spritesheet import SpriteSheet

FLY_DEAD = (143, 0, 59, 33)
FLY_WINGS_UP = (0, 32, 72, 36)
FLY_WINGS_DOWN = (0, 0, 75, 31)
SLIME_WALK_1 = (52, 125, 50, 28)
SLIME_WALK_2 = (0, 125, 51, 26)


class Enemy(pygame.sprite.Sprite):
    """Enemy"""

    def __init__(self, sprite_sheet_data=None):
        """ Enemy constructor. Assumes constructed with user passing in
            an array of 4 numbers like what's defined at the top of this
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
        self.alive = True

    def update(self):
        """ Move the Fly."""

        if self.alive:
            pos = self.rect.x - self.level.world_shift
            frame = (pos // 30) % 2  # 2 numbers of states
            if self.change_x < 1:
                self.image = self.frames_left[frame]
            else:
                self.image = self.frames_right[frame]

            self.rect.x += self.change_x
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit and not self.player.invincible:
                if self.player.change_y > 0:
                    self.alive = False
                    self.time_killed = pygame.time.get_ticks()
                    self.bounce_player()
                    self.level.score += 10
                else:
                    self.player.hit()

            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
                self.change_x *= -1
        else:
            time_since_killed = pygame.time.get_ticks() - self.time_killed
            if time_since_killed < 700:
                self.image = self.sprite_sheet.get_image(FLY_DEAD[0],
                                                         FLY_DEAD[1],
                                                         FLY_DEAD[2],
                                                         FLY_DEAD[3])
                self.rect.y += 10
            else:
                self.kill()

    def bounce_player(self):
        self.player.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self.player, self.level.platform_list, False)
        self.player.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) >= 0 or self.player.rect.bottom >= constants.SCREEN_HEIGHT:
            self.player.change_y = -5


class Slime(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.change_x = 1

        self.boundary_left = 0
        self.boundary_right = 0

        self.frames_left = []
        image = self.sprite_sheet.get_image(SLIME_WALK_1[0],
                                            SLIME_WALK_1[1],
                                            SLIME_WALK_1[2],
                                            SLIME_WALK_1[3])
        self.frames_left.append(image)
        image = self.sprite_sheet.get_image(SLIME_WALK_2[0],
                                            SLIME_WALK_2[1],
                                            SLIME_WALK_2[2],
                                            SLIME_WALK_2[3])
        self.frames_left.append(image)

        self.frames_right = []

        image = self.sprite_sheet.get_image(SLIME_WALK_1[0],
                                            SLIME_WALK_1[1],
                                            SLIME_WALK_1[2],
                                            SLIME_WALK_1[3])
        image = pygame.transform.flip(image, True, False)
        self.frames_right.append(image)

        image = self.sprite_sheet.get_image(SLIME_WALK_2[0],
                                            SLIME_WALK_2[1],
                                            SLIME_WALK_2[2],
                                            SLIME_WALK_2[3])
        image = pygame.transform.flip(image, True, False)
        self.frames_right.append(image)

        self.image = self.frames_right[0]
        self.rect = self.image.get_rect()
        self.alive = True

    def update(self):
        """ Move the Fly."""

        if self.alive:
            pos = self.rect.x - self.level.world_shift
            frame = (pos // 30) % 2  # 2 numbers of states
            if self.change_x < 1:
                self.image = self.frames_left[frame]
            else:
                self.image = self.frames_right[frame]

            self.rect.x += self.change_x
            hit = pygame.sprite.collide_rect(self, self.player)
            if hit and not self.player.invincible:
                if self.player.change_y > 0:
                    self.alive = False
                    self.time_killed = pygame.time.get_ticks()
                    self.bounce_player()
                    self.level.score += 10
                else:
                    self.player.hit()

            cur_pos = self.rect.x - self.level.world_shift
            if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
                self.change_x *= -1
        else:
            time_since_killed = pygame.time.get_ticks() - self.time_killed
            if time_since_killed < 700:
                self.rect.y += 10
            else:
                self.kill()

    def bounce_player(self):
        self.player.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self.player, self.level.platform_list, False)
        self.player.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) >= 0 or self.player.rect.bottom >= constants.SCREEN_HEIGHT:
            self.player.change_y = -5
