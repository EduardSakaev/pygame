from constants import TEXTURES, STATES
from game_elements.image_object_base import ImageObjectBase


class Chip(ImageObjectBase):
    def __init__(self, left, top, image_name, row, column, depth=0):
        ImageObjectBase.__init__(self, left, top, image_name, depth)
        self._chip_light = self.load_image(TEXTURES.CHIP_BORDER_NAME)
        self._image_max_width = self.width
        self._row = row
        self._column = column
        self._state = STATES.NORMAL

    def draw(self, surface):
        surface.blit(self.image_obj, self._bounds)

        if self._state in (STATES.HOVER, STATES.PRESSED):
            surface.blit(self._chip_light, (self.left, self.top))

    def handle_mouse_move(self, pos):
        if self._bounds.collidepoint(pos):
            if self._state != STATES.PRESSED:
                self._state = STATES.HOVER
        else:
            if not self._state == STATES.PRESSED:
                self._state = STATES.NORMAL

    def reset_state(self):
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

    @row.setter
    def row(self, value):
        self._row = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def image_max_width(self):
        return self._image_max_width

    def __repr__(self):
        return '{}'.format(self.unique_id)

    def update(self):
        pass
