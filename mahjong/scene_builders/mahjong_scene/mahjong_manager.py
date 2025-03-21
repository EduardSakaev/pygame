import pygame
import time
import re
from pygame.locals import RESIZABLE
from twisted.internet import reactor

from constants import TEXTURES, GAME_CONSTANTS
from game_elements.image_object_base import ImageObjectBase
from scene_builders.manager_base import ManagerBase
from scene_builders.mahjong_scene.mahjong_builder import MahjongBuilder
from scene_builders.mahjong_scene.mahjong_logic import MahjongLogic


class MahjongManager(ManagerBase):
    """
    Creates all objects related to mahjong scene + includes game logic
    """

    def __init__(self, width, height):
        super().__init__()
        self._width, self._height = width, height
        self._mahjong_logic = MahjongLogic(width, height)
        self._mahjong_builder = MahjongBuilder()
        self._scene_priority = 1
        self._mouse_handlers = []
        self._surface = None
        self._selected_chip = None
        self._is_game_resized = False
        self._connection_lines = list()
        self._manager_name = MahjongManager.__name__
        self._level = 0
        self._alignment_timeout = 0.5
        self._is_connected = False
        self._removing_chips = list()
        self._is_board_blocked = False
        self._start_time = time.time()

    def create_scene(self):
        if not self._is_scene_created:
            self._mahjong_builder.create_cursor()
            self._mahjong_builder.create_timer(*self._mahjong_logic.get_matrix_top_left_x_y(), GAME_CONSTANTS.TIME)
            self._mahjong_builder.create_background()
            self._mahjong_builder.create_matrix_background()
            self._mahjong_builder.create_chips_background(self._mahjong_logic)
            self._mahjong_builder.create_chips(self._mahjong_logic)
            self._mahjong_builder.sound_effects.sounds['BACKGROUND'].play(-1)

            self._mahjong_builder.sort_objects()
            self._mouse_handlers.append(self._mahjong_builder.cursor.handle_events)
            self._is_scene_created = True

    def destroy(self):
        self._mahjong_builder.sound_effects.sounds['BACKGROUND'].stop()
        self._mahjong_builder = None

    def update(self):
        if self._is_game_resized:
            self._mahjong_logic.update(self._width, self._height)
            self._mahjong_builder.matrix_background.width = self._width
            self._mahjong_builder.matrix_background.height = self._height
            self._mahjong_logic.update_obj_pos(self._mahjong_builder.matrix_background, 0, 0)

            for chip_obj in self._mahjong_builder.chip_objects.values():
                new_x, new_y = self._mahjong_logic.get_x_y_by_row_column(chip_obj.row, chip_obj.column)
                self._mahjong_logic.update_obj_pos(chip_obj, new_x, new_y)

            for index, brick_obj in enumerate(self._mahjong_builder.chip_background_objects):
                new_x, new_y = self._mahjong_logic.get_x_y_by_id(index)
                self._mahjong_logic.update_obj_pos(brick_obj, new_x, new_y)

            self._is_game_resized = False

        self.visualize_remove_chip_action()
        for scene_object in self._mahjong_builder.scene_objects:
            scene_object.update()

        self._mahjong_builder.timer.text = re.sub(r'\d+',
                                                  str(GAME_CONSTANTS.TIME - int(time.time() - self._start_time)),
                                                  self._mahjong_builder.timer.text)

    def draw(self):
        for scene_object in self._mahjong_builder.scene_objects:
            scene_object.draw(self._surface)

        for line_obj in self._connection_lines:
            line_obj.draw(self._surface)

    def visualize_remove_chip_action(self):
        if self._removing_chips:
            result = False
            for chip_obj in self._removing_chips:
                remove_scale_speed = 0.9
                chip_obj.scale(chip_obj.width * remove_scale_speed, chip_obj.height * remove_scale_speed)
                if chip_obj.width < 0.1 * chip_obj.image_max_width:
                    result = True

                if result:
                    self._mahjong_builder.remove_object(chip_obj)
                    self._mahjong_builder.remove_chip(chip_obj)
                    self._connection_lines = list()

            if result:
                self._removing_chips = list()
                self._is_board_blocked = False

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

    def handle_mouse_events(self, event_type, pos):
        for handler in self._mouse_handlers:
            handler(event_type, pos)

            if event_type == pygame.MOUSEBUTTONDOWN:
                for chip_obj in self._mahjong_builder.chip_objects.values():
                    if chip_obj.rect.collidepoint(pos):
                        self.handle_mouse_down_event(chip_obj, pos)
                        break
                else:
                    if self._selected_chip:
                        self._selected_chip.handle_mouse_down(pos)
                        self._selected_chip = None

            if not self._is_board_blocked:
                for chip_obj in self._mahjong_builder.chip_objects.values():
                    if event_type == pygame.MOUSEBUTTONUP:
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

    def handle_chips_connection(self, chip_obj, conn_path):
        chip_obj.reset_state()
        self._removing_chips.append(chip_obj)
        self._removing_chips.append(self._selected_chip)
        self._is_board_blocked = True
        self._mahjong_builder.sound_effects.sounds['CONNECTION_DONE'].play()
        self.visualize_connection(conn_path)
        reactor.callLater(self._alignment_timeout, self._mahjong_logic.align_chips,
                          self._mahjong_builder.chip_objects, self._selected_chip.row,
                          self._selected_chip.column, chip_obj.row, chip_obj.column)
        result = self._mahjong_logic.provide_possible_connection()
        if not result:
            self._mahjong_logic.shuffle_chips(self._mahjong_builder.chip_objects)

    def handle_mouse_down_event(self, chip_obj, pos):
        if self._selected_chip and str(self._selected_chip) == str(chip_obj):
            self._selected_chip = None
        elif self._selected_chip and str(self._selected_chip) != str(chip_obj):
            if self._selected_chip.image_name == chip_obj.image_name:
                conn_path = self._mahjong_logic.connect(self._selected_chip.row, self._selected_chip.column,
                                                        chip_obj.row, chip_obj.column)
                if conn_path:
                    self.handle_chips_connection(chip_obj, conn_path)
                else:
                    self._mahjong_builder.sound_effects.sounds['CONNECTION_WRONG'].play()

            self._selected_chip.handle_mouse_down(pos)
            self._selected_chip = None
            return
        else:
            self._selected_chip = chip_obj
        chip_obj.handle_mouse_down(pos)
        if self._selected_chip and chip_obj != self._selected_chip:
            self._selected_chip.handle_mouse_down(pos)

    @property
    def scene_priority(self):
        return self._scene_priority

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    def hide(self):
        self._is_hidden = True

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._mahjong_logic.level = value
        self._level = value
