import pygame

from game_elements.element_base import ElementBase


class Brick(ElementBase):
    def __init__(self, x, y, width, height, color, depth=0, special_effect=None):
        ElementBase.__init__(self, x, y, width, height, depth)
        self._color = color
        self._special_effect = special_effect
        self._alpha = 255
        self._color = color
        self._surface = pygame.Surface((width, height))  # the size of your rect
        self._surface.fill(color)  # this fills the entire surface

    def draw(self, surface):
        surface.blit(self._surface, self._bounds)

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self._surface.set_alpha(value)

    def update(self):
        pass

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._surface.fill(self.color)

    @ElementBase.width.setter
    def width(self, value):
        self._bounds.width = value
        self._surface = pygame.Surface((self.width, self.height))
        self.color = self._color
        self.alpha = self._alpha

