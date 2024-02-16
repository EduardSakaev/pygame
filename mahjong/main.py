# importing required library
import pygame
from copy import deepcopy
from mahjong.constants import GAME_CONSTANTS, TEXTURES

matrix = list()

def initGame():
    # activate the pygame library .
    pygame.init()

    # set the pygame window name
    pygame.display.set_caption(GAME_CONSTANTS.GAME_NAME)

    # hide cursor
    pygame.mouse.set_visible(False)



def initCursor():
    # cursor image
    imageCursor = pygame.image.load(f'{TEXTURES.PATH}\{TEXTURES.CURSOR}')
    imageCursor = pygame.transform.scale(imageCursor, (imageCursor.get_width(), imageCursor.get_height()))
    return imageCursor


def loadChips():
    size_x = GAME_CONSTANTS.NUMBER_CHIPS_X
    size_y = GAME_CONSTANTS.NUMBER_CHIPS_Y



    pass

if __name__ == '__main__':
    initGame()
    imageCursor = initCursor()
    # pygame.sprite.LayeredUpdates
    # create a surface object, image is drawn on it.

    imageBg = pygame.image.load(f'{TEXTURES.PATH}\{TEXTURES.BACKGROUND}')
    imageHeight = imageBg.get_height()
    imageWidth = imageBg.get_width()
    imageBg = pygame.transform.scale(imageBg, (imageWidth, imageHeight))
    scrn = pygame.display.set_mode((imageWidth, imageHeight))


    image_chip = pygame.image.load(f'{TEXTURES.PATH}\{TEXTURES.CHIP_NAME_PATTERN.format("1")}')
    image_chip_height = image_chip.get_height()
    image_chip_width = image_chip.get_width()
    image_chip = pygame.transform.scale(image_chip, (image_chip_width, image_chip_height))
    image_chip_2 = image_chip
    # paint screen one time
    pygame.display.update()
    status = True

    clock = pygame.time.Clock()

    while (status):

        # iterate over the list of Event objects
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():

            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False

            if event.type == pygame.MOUSEMOTION:
                scrn.fill((0, 0, 0))
                mouse_position = pygame.mouse.get_pos()
                scrn.blit(imageBg, (0, 0))
                scrn.blit(image_chip, (100, 100))
                scrn.blit(image_chip_2, (200, 200))
                scrn.blit(imageCursor, mouse_position)

                pygame.display.update()
                clock.tick(60)

                # deactivates the pygame library
    pygame.quit()
