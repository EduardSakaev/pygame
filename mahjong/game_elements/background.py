import pygame

from game_elements.element_base import ElementBase


class Background(ElementBase):
    def __init__(self, image_name, depth=0):
        self.bg_obj = self.load_image(image_name)
        width = self.bg_obj.get_width()
        height = self.bg_obj.get_height()
        ElementBase.__init__(self, 0, 0, width, height, depth)

    def draw(self, surface):
        surface.blit(self.bg_obj, (0, 0))
