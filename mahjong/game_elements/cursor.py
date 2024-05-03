import pygame

from game_elements.image_object_base import ImageObjectBase


class Cursor(ImageObjectBase):
    def __init__(self, image_name, depth=0):
        self._cursor_pos = (0, 0)
        ImageObjectBase.__init__(self, 0, 0, image_name, depth)

    def draw(self, surface):
        surface.blit(self.image_obj, self._cursor_pos)

    def handle(self, event_type, event_pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(event_pos)

    def handle_mouse_move(self, event_pos):
        self._cursor_pos = event_pos


