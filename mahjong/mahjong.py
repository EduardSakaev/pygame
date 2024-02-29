import pygame

from chip_matrix_helper import ChipMatrixHelper
from constants import GAME_CONSTANTS, TEXTURES, SOUND
from game import Game
from game_elements.image_object_base import ImageObjectBase
from game_elements.chip import Chip
from game_elements.cursor import Cursor
from game_elements.brick import Brick
import colors


class Mahjong(Game):
    def __init__(self, caption, frame_rate):
        Game.__init__(self,
                      caption,
                      frame_rate)
        self.is_game_running = True
        self.cursor = None
        self.background_image = None
        self.background_brick = None
        self.chip_objects = list()
        self.bricks_objects = list()
        self.selected_chip = None
        self.matrix_info = ChipMatrixHelper(self.cur_width, self.cur_height)

        self.sound_effects = {'background': pygame.mixer.Sound(SOUND.BACKGROUND),
                              'level_complete': pygame.mixer.Sound(SOUND.LEVEL_COMPLETE),
                              'connection_done': pygame.mixer.Sound(SOUND.CONNECTION_DONE),
                              'connection_wrong': pygame.mixer.Sound(SOUND.CONNECTION_WRONG)}
        self.create_objects()
        self.connection_lines = list()
        self.sound_effects['background'].play(-1)

    def create_objects(self):
        self.create_cursor()
        self.create_background()
        self._create_bricks()
        self.create_chips()

    def create_background(self):
        self.background_image = ImageObjectBase(0, 0, TEXTURES.BACKGROUND, -100)
        self.background_image.scale(self._display_info.current_w, self._display_info.current_h)
        self.objects.append(self.background_image)

    def create_cursor(self):
        self.cursor = Cursor(TEXTURES.CURSOR, 100)
        self.objects.append(self.cursor)
        self.mouse_handlers.append(self.cursor.handle)

    def create_chips(self):
        chip_matrix = self.matrix_info.chips_matrix
        for index, chip_number in enumerate(chip_matrix):
            if chip_number == 0:
                continue
            row, column = self.matrix_info.get_row_column_by_array_id(index)
            x, y = self.matrix_info.get_x_y_by_row_column(row, column)
            chip_name = TEXTURES.CHIP_NAME_PATTERN.format(chip_number)
            chip_obj = Chip(x, y, chip_name, row, column)

            self.objects.append(chip_obj)
            self.chip_objects.append(chip_obj)

    def _create_bricks(self):
        x, y = self.matrix_info.get_matrix_top_left_x_y()
        width = self.matrix_info.matrix_width - self.matrix_info.space_columns
        height = self.matrix_info.matrix_height - self.matrix_info.space_rows
        self.background_brick = Brick(x, y, width, height, colors.GRAY1, -50)
        self.background_brick.alpha = 120
        self.objects.append(self.background_brick)

        chip_width = self.matrix_info.chip_width
        chip_height = self.matrix_info.chip_height
        for index, _ in enumerate(self.matrix_info.chips_matrix):
            x, y = self.matrix_info.get_x_y_by_id(index)
            brick_chip_obj = Brick(x, y, chip_width, chip_height, colors.PINK, -49)
            brick_chip_obj.alpha = 30
            self.bricks_objects.append(brick_chip_obj)
            self.objects.append(brick_chip_obj)

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
                if self.selected_chip.image_name == chip_obj.image_name:
                    conn_path = self.matrix_info.connect(self.selected_chip.row, self.selected_chip.column,
                                                         chip_obj.row, chip_obj.column)

                    print(conn_path)
                    if conn_path:

                        chip_obj.remove_chip_from_board()
                        self.selected_chip.remove_chip_from_board()
                        self.sound_effects['connection_done'].play()
                        self.visualize_connection(conn_path)
                    else:
                        self.sound_effects['connection_wrong'].play()

                self.selected_chip = None
                return
            else:
                self.selected_chip = chip_obj
        chip_obj.handle_mouse_down(pos)

    def visualize_connection(self, path):
        depth = 2
        for index, point in enumerate(path):
            x, y = self.matrix_info.get_x_y_by_row_column(point[0], point[1])
            if index == 0 or index == len(path) - 1:
                light_point_obj = ImageObjectBase(x, y, TEXTURES.POINT_NAME, depth=depth)
                self.connection_lines.append(light_point_obj)
                if index == 0:
                    continue

            line_obj = None
            width = height = angle = 0
            if point[0] == path[index - 1][0]:
                dx = self.matrix_info.chip_width / 2 + self.matrix_info.space_columns
                x += -dx if point[1] - path[index - 1][1] > 0 else dx - self.matrix_info.space_columns - 1
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self.matrix_info.space_columns + 2
                height = line_obj.height

            elif point[1] == path[index - 1][1]:
                dy = self.matrix_info.chip_height / 2 + self.matrix_info.space_rows
                y += -dy if point[0] - path[index - 1][0] > 0 else dy
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self.matrix_info.space_rows
                height = line_obj.height
                angle = 90

            line_obj.scale(width, height, angle)
            self.connection_lines.append(line_obj)

    def remove_object(self, obj):
        self.objects.pop(self.get_object_id_in_list(self.objects, obj))

    def remove_chip(self, chip_object):
        self.chip_objects.pop(self.get_object_id_in_list(self.chip_objects, chip_object))

    @staticmethod
    def get_object_id_in_list(array, chip_object):
        return next((i for i, obj in enumerate(array) if str(obj) == str(chip_object)), -1)

    def _update_obj_pos(self, obj, x, y):
        obj.left = x
        obj.top = y

    def update(self):
        if self._is_game_resized:
            self.matrix_info.update(self.cur_width, self.cur_height)

            x, y = self.matrix_info.get_matrix_top_left_x_y()
            self.background_brick.width = self.matrix_info.matrix_width - self.matrix_info.space_columns
            self.background_brick.height = self.matrix_info.matrix_height - self.matrix_info.space_rows
            self._update_obj_pos(self.background_brick, x, y)

            for index, chip_obj in enumerate(self.chip_objects):
                new_x, new_y = self.matrix_info.get_x_y_by_row_column(chip_obj.row, chip_obj.column)
                self._update_obj_pos(chip_obj, new_x, new_y)

            for index, brick_obj in enumerate(self.bricks_objects):
                new_x, new_y = self.matrix_info.get_x_y_by_id(index)
                self._update_obj_pos(brick_obj, new_x, new_y)

            self._is_game_resized = False

        for chip_obj in self.chip_objects:
            if chip_obj.is_removed:
                self.remove_object(chip_obj)
                self.remove_chip(chip_obj)
                self.connection_lines = list()

            # row = chip_obj.row
            # column = chip_obj.column
            # x, y = self.matrix_info.get_x_y_by_row_column(row, column)
            # chip_obj.left = x
            # chip_obj.top = y
        super(Mahjong, self).update()

    def draw(self):
        super(Mahjong, self).draw()
        for line_obj in self.connection_lines:
            line_obj.draw(self.surface)


if __name__ == '__main__':
    mahjong = Mahjong(GAME_CONSTANTS.GAME_NAME, GAME_CONSTANTS.FRAME_RATE).run()
