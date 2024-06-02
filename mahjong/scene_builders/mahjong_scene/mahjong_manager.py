import pygame
from pygame.locals import RESIZABLE

from constants import TEXTURES
from game_elements.image_object_base import ImageObjectBase
from scene_builders.manager_base import ManagerBase
from scene_builders.mahjong_scene.mahjong_builder import MahjongBuilder
from scene_builders.mahjong_scene.mahjong_logic import MahjongLogic


class MahjongManager(ManagerBase):
    """
    Creates all objects related to mahjong scene + includes game logic
    """

    def __init__(self, width, height):
        self._width, self._height = width, height
        self._mahjong_logic = MahjongLogic(width, height)
        self._mahjong_builder = MahjongBuilder()
        self._scene_priority = 1
        self._mouse_handlers = []
        self._surface = None
        self._selected_chip = None
        self._is_game_resized = False
        self._connection_lines = list()

    def create_scene(self):
        self._mahjong_builder.create_cursor()
        self._mahjong_builder.create_background()
        self._mahjong_builder.create_matrix_background(self._mahjong_logic)
        self._mahjong_builder.create_chips_background(self._mahjong_logic)
        self._mahjong_builder.create_chips(self._mahjong_logic)
        self._mahjong_builder.create_sound_effects()
        self._mahjong_builder.sound_effects['background'].play(-1)

        self._mahjong_builder.sort_objects()
        self._mouse_handlers.append(self._mahjong_builder.cursor.handle)

    def update(self):
        if self._is_game_resized:
            self._mahjong_logic.update(self._width, self._height)

            x, y = self._mahjong_logic.get_matrix_top_left_x_y()
            self._mahjong_builder.matrix_background.width = self._mahjong_logic.matrix_width - self._mahjong_logic.space_columns
            self._mahjong_builder.matrix_background.height = self._mahjong_logic.matrix_height - self._mahjong_logic.space_rows
            self._mahjong_logic.update_obj_pos(self._mahjong_builder.matrix_background, x, y)

            for chip_obj in self._mahjong_builder.chip_objects.values():
                new_x, new_y = self._mahjong_logic.get_x_y_by_row_column(chip_obj.row, chip_obj.column)
                self._mahjong_logic.update_obj_pos(chip_obj, new_x, new_y)

            for index, brick_obj in enumerate(self._mahjong_builder.chip_background_objects):
                new_x, new_y = self._mahjong_logic.get_x_y_by_id(index)
                self._mahjong_logic.update_obj_pos(brick_obj, new_x, new_y)

            self._is_game_resized = False

        values = list(self._mahjong_builder.chip_objects.values())
        for chip_obj in values:
            if chip_obj.is_removed:
                self._mahjong_builder.remove_object(chip_obj)
                self._mahjong_builder.remove_chip(chip_obj)
                self._connection_lines = list()

        for scene_object in self._mahjong_builder.scene_objects:
            scene_object.update()

    def visualize_connection(self, path):
        depth = 2
        for index, point in enumerate(path):
            x, y = self._mahjong_logic.get_x_y_by_row_column(point[0], point[1])
            if index == 0 or index == len(path) - 1:
                light_point_obj = ImageObjectBase(x, y, TEXTURES.POINT_NAME, depth=depth)
                self._connection_lines.append(light_point_obj)
                if index == 0:
                    continue

            line_obj = None
            width = height = angle = 0
            if point[0] == path[index - 1][0]:
                dx = self._mahjong_logic.chip_width / 2 + self._mahjong_logic.space_columns
                x += -dx if point[1] - path[index - 1][1] > 0 else dx - self._mahjong_logic.space_columns - 1
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self._mahjong_logic.space_columns + 2
                height = line_obj.height

            elif point[1] == path[index - 1][1]:
                dy = self._mahjong_logic.chip_height / 2 + self._mahjong_logic.space_rows
                y += -dy if point[0] - path[index - 1][0] > 0 else dy
                line_obj = ImageObjectBase(x, y, TEXTURES.LINE_NAME, depth=depth)
                width = line_obj.width + self._mahjong_logic.space_rows
                height = line_obj.height
                angle = 90

            line_obj.scale(width, height, angle)
            self._connection_lines.append(line_obj)

    def draw(self):
        for scene_object in self._mahjong_builder.scene_objects:
            scene_object.draw(self._surface)

        for line_obj in self._connection_lines:
            line_obj.draw(self._surface)

    def handle_mouse_events(self, event_type, pos):
        for handler in self._mouse_handlers:
            handler(event_type, pos)

        for chip_obj in self._mahjong_builder.chip_objects.values():
            if event_type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down_event(chip_obj, pos)
            elif event_type == pygame.MOUSEBUTTONUP:
                chip_obj.handle_mouse_up(pos)
            elif event_type == pygame.MOUSEMOTION:
                chip_obj.handle_mouse_move(pos)

    def handle_key_down_event(self, key):
        pass

    def handle_key_up_events(self, key):
        pass

    def handle_game_resize(self, new_width, new_height):
        width, height = pygame.display.get_surface().get_size()

        if width < self._mahjong_logic.matrix_width or height < self._mahjong_logic.matrix_height:
            self._surface = pygame.display.set_mode((width, height), RESIZABLE)
            return

        self._width, self._height = pygame.display.get_surface().get_size()
        self._is_game_resized = True

    def handle_mouse_down_event(self, chip_obj, pos):
        if chip_obj.rect.collidepoint(pos):
            if self._selected_chip and str(self._selected_chip) == str(chip_obj):
                self._selected_chip = None

            elif self._selected_chip and str(self._selected_chip) != str(chip_obj):
                if self._selected_chip.image_name == chip_obj.image_name:
                    conn_path = self._mahjong_logic.connect(self._selected_chip.row, self._selected_chip.column,
                                                            chip_obj.row, chip_obj.column)

                    print(conn_path)
                    if conn_path:

                        chip_obj.remove_chip_from_board()
                        self._selected_chip.remove_chip_from_board()
                        self._mahjong_builder.sound_effects['connection_done'].play()
                        self.visualize_connection(conn_path)
                        result = self._mahjong_logic.provide_possible_connection()
                        if not result:
                            self._mahjong_logic.shuffle_chips(self._mahjong_builder.chip_objects)
                    else:
                        self._mahjong_builder.sound_effects['connection_wrong'].play()

                self._selected_chip = None
                return
            else:
                self._selected_chip = chip_obj
        chip_obj.handle_mouse_down(pos)

    @property
    def scene_priority(self):
        return self._scene_priority

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface
