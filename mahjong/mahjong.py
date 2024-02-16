import pygame

from constants import GAME_CONSTANTS, TEXTURES, TEXT
from game import Game
from game_elements.background import Background
from game_elements.chip import Chip
from game_elements.cursor import Cursor
from game_elements.text_object import TextObject
from chip_matrix_helper import ChipMatrixHelper


class Mahjong(Game):
    def __init__(self, caption, width, height, frame_rate):
        Game.__init__(self,
                      caption,
                      width,
                      height,
                      frame_rate)
        self.is_game_running = True
        self.cursor = None
        self.background_image = None
        self.chip_objects = list()
        self.selected_chip = None
        self.matrix_info = ChipMatrixHelper()
        self.create_objects()

    def create_objects(self):
        self.create_cursor()
        self.create_background()
        self.create_chips()

    def create_background(self):
        self.background_image = Background(TEXTURES.BACKGROUND, -100)
        self.objects.append(self.background_image)

    def create_cursor(self):
        self.cursor = Cursor(TEXTURES.CURSOR, 100)
        self.objects.append(self.cursor)
        self.mouse_handlers.append(self.cursor.handle)

    def create_chips(self):
        chip_matrix = self.matrix_info.chips_matrix
        for index, chip_number in enumerate(chip_matrix):
            row, column = self.matrix_info.get_row_column_by_array_id(index)
            x, y = self.matrix_info.get_x_y_by_row_column(row, column)
            text_obj = TextObject(x + 5, y + 5, f'{row}-{column}', TEXT.TEXT_COLOR, TEXT.FONT_NAME,
                                  TEXT.FONT_SIZE, depth=1)
            self.objects.append(text_obj)
            if chip_number == 0:
                continue
            chip_name = TEXTURES.CHIP_NAME_PATTERN.format(chip_number)
            chip_obj = Chip(x, y, chip_name, row, column)
            # add chip postions text for debugging

            self.objects.append(chip_obj)

            self.chip_objects.append(chip_obj)

    def handle_mouse_events(self, type, pos):
        for handler in self.mouse_handlers:
            handler(type, pos)

        for chip_obj in self.chip_objects:
            if type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down_event(chip_obj, pos)
            elif type == pygame.MOUSEBUTTONUP:
                chip_obj.handle_mouse_up(pos)
            elif type == pygame.MOUSEMOTION:
                chip_obj.handle_mouse_move(pos)

    def handle_mouse_down_event(self, chip_obj, pos):
        if chip_obj.rect.collidepoint(pos):
            if self.selected_chip and str(self.selected_chip) == str(chip_obj):
                self.selected_chip = None

            elif self.selected_chip and str(self.selected_chip) != str(chip_obj):
                if self.selected_chip.name == chip_obj.name:
                    print ('{}-{} -> {}-{}'.format(self.selected_chip.row, self.selected_chip.column,
                                                          chip_obj.row, chip_obj.column))
                    result = self.matrix_info.can_connect(self.selected_chip.row, self.selected_chip.column,
                                                          chip_obj.row, chip_obj.column)
                    print(result)
                    if result:
                        self.matrix_info.connect(self.selected_chip.row, self.selected_chip.column,
                                                 chip_obj.row, chip_obj.column)

                    print()
                    index = 0
                    result = ''
                    for value in self.matrix_info.chips_matrix:
                        if index == self.matrix_info.columns:
                            index = 0
                            print(result)
                            result = ''
                        index += 1
                        result = result + str(value) + ' '
                    else:
                        print(result)
                    self.remove_object_from_lists(chip_obj)
                    self.remove_object_from_lists(self.selected_chip)

                self.selected_chip = None
                return
            else:
                self.selected_chip = chip_obj
        chip_obj.handle_mouse_down(pos)

    def remove_object_from_lists(self, chip_object):
        self.objects.pop(self.get_object_id_in_list(self.objects, chip_object))
        self.chip_objects.pop(self.get_object_id_in_list(self.chip_objects, chip_object))

    @staticmethod
    def get_object_id_in_list(array, chip_object):
        return next((i for i, obj in enumerate(array) if str(obj) == str(chip_object)), -1)


if __name__ == '__main__':
    mahjong = Mahjong(GAME_CONSTANTS.GAME_NAME,
                      GAME_CONSTANTS.WIDTH,
                      GAME_CONSTANTS.HEIGHT,
                      GAME_CONSTANTS.FRAME_RATE).run()
