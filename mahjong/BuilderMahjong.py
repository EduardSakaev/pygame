
from random import randint

import pygame

import colors
from constants import TEXTURES, SOUND
from game_elements.brick import Brick
from game_elements.chip import Chip
from game_elements.cursor import Cursor
from game_elements.image_object_base import ImageObjectBase


class BuilderMahjong:
    def __init__(self, matrix_helper):
        self._matrix_helper = matrix_helper
        self._background = None
        self._matrix_background = None
        self._objects = list()
        self._chip_objects = dict()
        self._chip_background_objects = list()
        self._cursor = None
        self._sound_effects = None
        self._width, self._height = 0, 0

    def create_cursor(self):
        self._cursor = Cursor(TEXTURES.CURSOR, 100)
        self._objects.append(self._cursor)

    def reset(self):
        self._background = None
        self._chip_background_objects = list()
        self._objects = list()
        self._chip_objects = dict()
        self._cursor = None

    def create_background(self):
        display_info = pygame.display.Info()
        self._background = ImageObjectBase(0, 0, TEXTURES.BACKGROUND, -100)
        self._background.scale(display_info.current_w, display_info.current_h)
        self._objects.append(self._background)

    def create_matrix_background(self):
        x, y = self._matrix_helper.get_matrix_top_left_x_y()
        width = self._matrix_helper.matrix_width - self._matrix_helper.space_columns
        height = self._matrix_helper.matrix_height - self._matrix_helper.space_rows
        self._matrix_background = Brick(x, y, width, height, colors.GRAY1, -50)
        self._matrix_background.alpha = 120
        self._objects.append(self._matrix_background)

    def create_chips_background(self):
        chip_width = self._matrix_helper.chip_width
        chip_height = self._matrix_helper.chip_height
        for index, _ in enumerate(self._matrix_helper.chips_matrix):
            x, y = self._matrix_helper.get_x_y_by_id(index)
            brick_chip_obj = Brick(x, y, chip_width, chip_height, colors.PINK, -49)
            brick_chip_obj.alpha = 30
            self._chip_background_objects.append(brick_chip_obj)
            self._objects.append(brick_chip_obj)

    def create_chips(self):
        chip_matrix = self._matrix_helper.chips_matrix
        for index, chip_number in enumerate(chip_matrix):
            if chip_number == 0:
                continue
            row, column = self._matrix_helper.get_row_column_by_array_id(index)
            x, y = self._matrix_helper.get_x_y_by_row_column(row, column)
            chip_name = TEXTURES.CHIP_NAME_PATTERN.format(chip_number.split('_')[0])
            chip_obj = Chip(x, y, chip_name, row, column)

            self._objects.append(chip_obj)
            self._chip_objects[chip_obj.unique_id] = chip_obj

    def create_sound_effects(self):
        self._sound_effects = {'background': pygame.mixer.Sound(SOUND.BACKGROUND),
                               'level_complete': pygame.mixer.Sound(SOUND.LEVEL_COMPLETE),
                               'connection_done': pygame.mixer.Sound(SOUND.CONNECTION_DONE),
                               'connection_wrong': pygame.mixer.Sound(SOUND.CONNECTION_WRONG)}

    def sort_objects(self, key):
        self._objects = sorted(self._objects, key=key)

    def shuffle_chips(self):
        counter = len(self.chips)
        chips_objs = list(self.chips.values())

        while counter > 0:
            # Generate a random integer between 0 and counter
            rnd = randint(0, counter)
            counter -= 1

            # Swap the element at the random index with the element at counter
            self._swap_chips(chips_objs[counter], chips_objs[rnd])
            chips_objs[counter],  chips_objs[rnd] = chips_objs[rnd], chips_objs[counter]

    def _swap_chips(self, obj_left, obj_right):
        matrix_id_left = self._matrix_helper.get_id_by_row_column(obj_left.row, obj_left.column)
        matrix_id_right = self._matrix_helper.get_id_by_row_column(obj_right.row, obj_right.column)
        self._matrix_helper.chips_matrix[matrix_id_left], self._matrix_helper.chips_matrix[matrix_id_right] = \
            self._matrix_helper.chips_matrix[matrix_id_right], self._matrix_helper.chips_matrix[matrix_id_left]

        obj_left.row, obj_right.row = obj_right.row, obj_left.row
        obj_left.column, obj_right.column = obj_right.column, obj_left.column
        obj_left.left, obj_right.left = obj_right.left, obj_left.left
        obj_left.top, obj_right.top = obj_right.top, obj_left.top

    @property
    def background(self):
        return self._background

    @property
    def cursor(self):
        return self._cursor

    @property
    def objects(self):
        return self._objects

    @property
    def matrix_background(self):
        return self._matrix_background

    @property
    def chips(self):
        return self._chip_objects

    @property
    def chips_background(self):
        return self._chip_background_objects

    @property
    def sound_effects(self):
        return self._sound_effects
