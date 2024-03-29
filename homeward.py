"""
Homeward

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

import constants
import levels
import health
import score

from player import Player


def main():
    """Main Program"""
    pygame.init()

    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Homeward")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.MainMenu(player))
    level_list.append(levels.LevelTutorial(player))
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    level_list.append(levels.Level_03(player))
    level_list.append(levels.Level_04(player))
    level_list.append(levels.YouWin(player))
    level_list.append(levels.GameOver(player))

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # HUD
    game_HUD = health.HUD(player)
    score_HUD = score.ScoreHUD(player)

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 25
    active_sprite_list.add(player)

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            left_control_keys = [pygame.K_LEFT, pygame.K_a]
            right_control_keys = [pygame.K_d, pygame.K_RIGHT]
            up_control_keys = [pygame.K_w, pygame.K_UP, pygame.K_SPACE]
            down_control_keys = [pygame.K_DOWN, pygame.K_s]

            if event.type == pygame.KEYDOWN:
                if event.key in left_control_keys:
                    player.go_left()
                if event.key in right_control_keys:
                    player.go_right()
                if event.key in up_control_keys:
                    player.jump()
                if event.key in down_control_keys:
                    player.duck()

                if (
                    event.key == pygame.K_LEFT
                    and pygame.key.get_mods() & pygame.KMOD_SHIFT
                ):
                    if current_level_no > 0:
                        current_level_no -= 1
                        current_level = level_list[current_level_no]
                        player.level = current_level
                        player.rect.y = (
                            constants.SCREEN_HEIGHT - player.rect.height - 25
                        )

                if (
                    event.key == pygame.K_RIGHT
                    and pygame.key.get_mods() & pygame.KMOD_SHIFT
                ):
                    if current_level_no < len(level_list) - 1:
                        current_level_no += 1
                        current_level = level_list[current_level_no]
                        player.level = current_level
                        player.rect.y = (
                            constants.SCREEN_HEIGHT - player.rect.height - 25
                        )

            if event.type == pygame.KEYUP:
                if event.key in left_control_keys and player.change_x < 0:
                    player.stop()
                if event.key in right_control_keys and player.change_x > 0:
                    player.stop()
                if event.key in down_control_keys and player.change_y > 0:
                    player.stand_up()

        # Update the player.
        active_sprite_list.update()

        # Update HUD
        game_HUD.update()
        score_HUD.update()

        # Update items in the level
        current_level.update()

        current_position = player.rect.x + current_level.world_shift

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if (
            player.rect.x <= 120 and current_level.world_shift < -1
        ):  # -1 to prevent edge of wall being seen
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world(diff)

        # If the player gets to the end of the level, go to the next level
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list) - 1:
                current_level_no += 1
                print(current_level_no)
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 25

        if player.health <= 0:
            current_level_no = len(level_list) - 1
            current_level = level_list[current_level_no]
            player.level = current_level
            player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 40
            player.rect.x = (constants.SCREEN_WIDTH / 2) - (player.rect.width / 2)
            time_since_death = pygame.time.get_ticks() - player.death_time
            if time_since_death > 2000:
                player.health = 100
                current_level_no = 0
                current_level = level_list[current_level_no]
                player.level = current_level
                player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 40

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        game_HUD.draw(screen)
        score_HUD.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()


if __name__ == "__main__":
    main()
