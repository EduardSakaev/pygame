import pygame

from constants import TEXTURES, STATES
from game_elements.image_object_base import ImageObjectBase


class Chip(ImageObjectBase):
    def __init__(self, left, top, image_name, row, column, depth=0):
        self._chip_light = self.load_image(TEXTURES.CHIP_BORDER_NAME)
        self._row = row
        self._column = column
        self._state = STATES.NORMAL
        self._chip_light_width = self._chip_light.get_width()
        self._chip_light_height = self._chip_light.get_height()
        self._remove_chip_action = False
        self._is_object_removed = False

        ImageObjectBase.__init__(self, left, top, image_name, depth)

    def draw(self, surface):
        surface.blit(self.image_obj, self._bounds)

        if self._state in (STATES.HOVER, STATES.PRESSED):
            surface.blit(self._chip_light, (self.left, self.top))

    def handle_mouse_move(self, pos):
        if self._bounds.collidepoint(pos):
            if self._state != STATES.PRESSED and not self._remove_chip_action:
                self._state = STATES.HOVER
        else:
            if not self._state == STATES.PRESSED:
                self._state = STATES.NORMAL

    def handle_mouse_up(self, pos):
        pass

    def handle_mouse_down(self, pos):
        if self._bounds.collidepoint(pos):
            if self._state == STATES.PRESSED:
                self._state = STATES.HOVER
            else:
                self._state = STATES.PRESSED
        else:
            self._state = STATES.NORMAL

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def is_removed(self):
        return self._is_object_removed

    def __repr__(self):
        return '{}_{}'.format(self._row, self._column)

    def update_chip_light(self, dw_pr, dh_pr):
        chip_light_obj = self.load_image(TEXTURES.CHIP_BORDER_NAME)

        width = chip_light_obj.get_width()
        height = chip_light_obj.get_height()
        new_width = width if dw_pr == 1 else self._chip_light_width * (1 + dw_pr)
        new_height = height if dw_pr == 1 else self._chip_light_height * (1 + dh_pr)
        self._chip_light = pygame.transform.smoothscale(chip_light_obj, (new_width, new_height))
        self._chip_light_width = new_width
        self._chip_light_height = new_height

    def scale_object(self, dw_pr, dh_pr):
        pass

    def remove_chip_from_board(self):
        self._remove_chip_action = True
        self._state = STATES.NORMAL

    def remove_chip_action(self):
        remove_scale_speed = 0.92
        self.scale(self.width * remove_scale_speed, self.height * remove_scale_speed)
        if self.width < 0.1 * self._max_width:
            self._remove_chip_action = False
            self._is_object_removed = True

    def update(self):
        if self._remove_chip_action:
            self.remove_chip_action()

