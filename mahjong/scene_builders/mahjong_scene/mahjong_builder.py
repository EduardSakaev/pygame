import pygame

from constants import COLORS, FONTS
from sounds import Sounds
from constants import TEXTURES
from game_elements.brick import Brick
from game_elements.chip import Chip
from game_elements.cursor import Cursor
from game_elements.image_object_base import ImageObjectBase
from game_elements.text_object import TextObject


class MahjongBuilder:
    def __init__(self):
        self._background = None
        self._matrix_background = None
        self._scene_objects = list()
        self._chip_objects = dict()
        self._chip_background_objects = list()
        self._cursor = None
        self._sound_effects = Sounds()
        self._text_timer = None

    def create_cursor(self):
        self._cursor = Cursor(TEXTURES.CURSOR, 100)
        self._scene_objects.append(self._cursor)

    def create_timer(self, x_pos, y_pos, game_time):
        self._text_timer = TextObject(x_pos, y_pos - 40, 'Time: {}'.format(game_time),
                                      COLORS.ANTIQUEWHITE, FONTS.LUCIDAFAXREGULAR, 40, 5)
        self._scene_objects.append(self._text_timer)

    def create_background(self):
        display_info = pygame.display.Info()
        self._background = ImageObjectBase(0, 0, TEXTURES.MAHJONG_BG, -100)
        self._background.scale(display_info.current_w, display_info.current_h)
        self._scene_objects.append(self._background)

    def create_matrix_background(self):
        display_info = pygame.display.Info()
        self._matrix_background = Brick(0, 0, display_info.current_w, display_info.current_h, COLORS.GRAY1, -50)
        self._matrix_background.alpha = 120
        self._scene_objects.append(self._matrix_background)

    def create_chips_background(self, mahjong_logic):
        chip_width = mahjong_logic.chip_width
        chip_height = mahjong_logic.chip_height
        for index, _ in enumerate(mahjong_logic.chips_matrix):
            x, y = mahjong_logic.get_x_y_by_id(index)
            brick_chip_obj = Brick(x, y, chip_width, chip_height, COLORS.PINK, -49)
            brick_chip_obj.alpha = 60
            self._chip_background_objects.append(brick_chip_obj)
            self._scene_objects.append(brick_chip_obj)

    def create_chips(self, mahjong_logic):
        chip_matrix = mahjong_logic.chips_matrix
        for index, chip_number in enumerate(chip_matrix):
            if chip_number == 0:
                continue
            row, column = mahjong_logic.get_row_column_by_array_id(index)
            x, y = mahjong_logic.get_x_y_by_row_column(row, column)
            chip_name = TEXTURES.CHIP_NAME_PATTERN.format(chip_number.split('_')[0])
            chip_obj = Chip(x, y, chip_name, row, column)

            self._scene_objects.append(chip_obj)
            self._chip_objects[chip_obj.unique_id] = chip_obj

    def sort_objects(self):
        self._scene_objects = sorted(self._scene_objects, key=lambda obj: obj.depth)

    def remove_object(self, obj):
        self._scene_objects.pop(self.get_object_id_in_list(self._scene_objects, obj))

    def remove_chip(self, chip_object):
        self._chip_objects.pop(chip_object.unique_id)

    @staticmethod
    def get_object_id_in_list(array, chip_object):
        return next((i for i, obj in enumerate(array) if str(obj) == str(chip_object)), -1)

    @property
    def cursor(self):
        return self._cursor

    @property
    def timer(self):
        return self._text_timer

    @property
    def background(self):
        return self._background

    @property
    def matrix_background(self):
        return self._matrix_background

    @property
    def chip_background_objects(self):
        return self._chip_background_objects

    @property
    def chip_objects(self):
        return self._chip_objects

    @property
    def scene_objects(self):
        return self._scene_objects

    @property
    def sound_effects(self):
        return self._sound_effects
