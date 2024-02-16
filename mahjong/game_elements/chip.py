from constants import TEXTURES
from game_elements.element_base import ElementBase


class Chip(ElementBase):
    def __init__(self, left, top, image_name, row, column, depth=0):
        self._name = image_name
        self._chip_obj = self.load_image(image_name)
        self._chip_light = self.load_image(TEXTURES.CHIP_BORDER_NAME)
        self._row = row
        self._column = column
        width = self._chip_obj.get_width()
        height = self._chip_obj.get_height()
        self._state = 'normal'

        ElementBase.__init__(self, left, top, width, height, depth)

    def draw(self, surface):
        surface.blit(self._chip_obj, self._bounds)

        if self._state in ('hover', 'pressed'):
            surface.blit(self._chip_light, (self.left - 25, self.top - 24))

    def handle_mouse_move(self, pos):
        if self._bounds.collidepoint(pos):
            if self._state != 'pressed':
                self._state = 'hover'
        else:
            if not self._state == 'pressed':
                self._state = 'normal'

    def handle_mouse_up(self, pos):
        pass

    def handle_mouse_down(self, pos):
        if self._bounds.collidepoint(pos):
            if self._state == 'pressed':
                self._state = 'hover'
            else:
                self._state = 'pressed'
        else:
            self._state = 'normal'

    @property
    def name(self):
        return self._name

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    def __repr__(self):
        return '{}_{}'.format(self._row, self._column)
