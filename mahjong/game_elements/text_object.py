import pygame


class TextObject:
    def __init__(self, left, top, text, color, font_name, font_size, depth=0, is_bold=True):
        self._pos = (left, top)
        self._text = text
        self._color = color
        self._font = pygame.font.SysFont(font_name, font_size, bold=is_bold, italic=True)
        self._bounds = self.get_surface(text)
        self._depth = depth

    def draw(self, surface, centralized=False):
        text_surface, self._bounds = self.get_surface(self._text)
        if centralized:
            pos = (self._pos[0] - self._bounds.width // 2, self._pos[1])
        else:
            pos = self._pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self._font.render(text, False, self._color)
        return text_surface, text_surface.get_rect()

    def update(self):
        pass

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
