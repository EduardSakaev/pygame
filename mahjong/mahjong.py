import pygame
from pygame.locals import RESIZABLE

from BuilderMahjong import BuilderMahjong
from chip_matrix_helper import ChipMatrixHelper
from constants import GAME_CONSTANTS, TEXTURES
from director import Director
from game import Game
from game_elements.image_object_base import ImageObjectBase


class Mahjong(Game):
    def __init__(self, caption, frame_rate):
        Game.__init__(self, frame_rate)
        self.is_game_running = True
        self._director = Director()
        self._director.init_game(caption)
        self._matrix_helper = ChipMatrixHelper(self._director.width, self._director.height)
        self._builder = BuilderMahjong(self._matrix_helper)
        self._director.set_builder(self._builder)
        self._director.create_objects()

        self._builder.sound_effects['background'].play(-1)
        self._mouse_handlers.append(self._builder.cursor.handle)
        self._connection_lines = list()
        self._selected_chip = None
        self._matrix_width, self._matrix_height = self._matrix_helper.matrix_width, self._matrix_helper.matrix_height

    def handle_mouse_events(self, type, pos):
        for handler in self._mouse_handlers:
            handler(type, pos)

        for chip_obj in self._builder.chips.values():
            if type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down_event(chip_obj, pos)
            elif type == pygame.MOUSEBUTTONUP:
                chip_obj.handle_mouse_up(pos)
            elif type == pygame.MOUSEMOTION:
                chip_obj.handle_mouse_move(pos)

    def handle_mouse_down_event(self, chip_obj, pos):
        if chip_obj.rect.collidepoint(pos):
            if self._selected_chip and str(self._selected_chip) == str(chip_obj):
                self._selected_chip = None

            elif self._selected_chip and str(self._selected_chip) != str(chip_obj):
                if self._selected_chip.image_name == chip_obj.image_name:
                    conn_path = self._matrix_helper.connect(self._selected_chip.row, self._selected_chip.column,
                                                            chip_obj.row, chip_obj.column)

                    print(conn_path)
                    if conn_path:

                        chip_obj.remove_chip_from_board()
                        self._selected_chip.remove_chip_from_board()
                        self._builder.sound_effects['connection_done'].play()
                        self.visualize_connection(conn_path)
                        result = self._matrix_helper.provide_possible_connection()
                        if not result:
                            self._builder.shuffle_chips()
                    else:
                        self._builder.sound_effects['connection_wrong'].play()

                self._selected_chip = None
                return
            else:
                self._selected_chip = chip_obj
        chip_obj.handle_mouse_down(pos)

    def visualize_connection(self, path):
        depth = 2
        for index, point in enumerate(path):
            x, y = self._matrix_helper.get_x_y_by_row_column(point[0], point[1])
            if index == 0 or index == len(path) - 1:
                light_point_obj = ImageObjectBase(x, y, TEXTURES.POINT_NAME, depth=depth)
                self._connection_lines.append(light_point_obj)
                if index == 0:
                    continue

            line_obj = None
            width = height = angle = 0
            if point[0] == path[index - 1][0]:
                dx = self._matrix_helper.chip_width / 2 + self._matrix_helper.space_columns
                x += -dx if point[1] - path[index - 1][1] > 0 else dx - self._matrix_helper.space_columns - 1
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self._matrix_helper.space_columns + 2
                height = line_obj.height

            elif point[1] == path[index - 1][1]:
                dy = self._matrix_helper.chip_height / 2 + self._matrix_helper.space_rows
                y += -dy if point[0] - path[index - 1][0] > 0 else dy
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self._matrix_helper.space_rows
                height = line_obj.height
                angle = 90

            line_obj.scale(width, height, angle)
            self._connection_lines.append(line_obj)

    def remove_object(self, obj):
        self._builder.objects.pop(self.get_object_id_in_list(self._builder.objects, obj))

    def remove_chip(self, chip_object):
        self._builder.chips.pop(chip_object.unique_id)

    @staticmethod
    def get_object_id_in_list(array, chip_object):
        return next((i for i, obj in enumerate(array) if str(obj) == str(chip_object)), -1)

    def _update_obj_pos(self, obj, x, y):
        obj.left = x
        obj.top = y

    def update(self):
        if self._is_game_resized:
            self._matrix_helper.update(self._director.width, self._director.height)

            x, y = self._matrix_helper.get_matrix_top_left_x_y()
            self._builder.matrix_background.width = self._matrix_helper.matrix_width - self._matrix_helper.space_columns
            self._builder.matrix_background.height = self._matrix_helper.matrix_height - self._matrix_helper.space_rows
            self._update_obj_pos(self._builder.matrix_background, x, y)

            for chip_obj in self._builder.chips.values():
                new_x, new_y = self._matrix_helper.get_x_y_by_row_column(chip_obj.row, chip_obj.column)
                self._update_obj_pos(chip_obj, new_x, new_y)

            for index, brick_obj in enumerate(self._builder.chips_background):
                new_x, new_y = self._matrix_helper.get_x_y_by_id(index)
                self._update_obj_pos(brick_obj, new_x, new_y)

            self._is_game_resized = False

        values = list(self._builder.chips.values())
        for chip_obj in values:
            if chip_obj.is_removed:
                self.remove_object(chip_obj)
                self.remove_chip(chip_obj)
                self._connection_lines = list()

        super(Mahjong, self).update()

    def draw(self):
        super(Mahjong, self).draw()
        for line_obj in self._connection_lines:
            line_obj.draw(self._director.surface)

    def handle_game_resize(self):
        width, height = pygame.display.get_surface().get_size()

        if width < self._matrix_width or height < self._matrix_height:
            self._director.surface = pygame.display.set_mode((width, height), RESIZABLE)
            return

        super(Mahjong, self).handle_game_resize()


if __name__ == '__main__':
    mahjong = Mahjong(GAME_CONSTANTS.GAME_NAME, GAME_CONSTANTS.FRAME_RATE).run()
