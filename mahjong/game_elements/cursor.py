import pygame

from game_elements.element_base import ElementBase


class Cursor(ElementBase):
    def __init__(self, image_name, depth=0):
        cursor_obj = self.load_image(image_name)
        width = cursor_obj.get_width()
        height = cursor_obj.get_height()
        self.cursor_pos = (0, 0)
        self.cursor_obj = pygame.transform.scale(cursor_obj, (cursor_obj.get_width(), cursor_obj.get_height()))
        ElementBase.__init__(self, 0, 0, width, height, depth)

    def draw(self, surface):
        surface.blit(self.cursor_obj, self.cursor_pos)

    def handle(self, event_type, event_pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(event_pos)

    def handle_mouse_move(self, event_pos):
        self.cursor_pos = event_pos


