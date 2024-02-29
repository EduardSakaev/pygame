import pygame


class TextObject:
    def __init__(self, left, top, text, color, font_name, font_size, depth=0, is_bold=True):
        self.pos = (left, top)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size, bold=is_bold, italic=True)
        self.bounds = self.get_surface(text)
        self._depth = depth

    def draw(self, surface, centralized=False):
        text_surface, self.bounds = self.get_surface(self.text)
        if centralized:
            pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        else:
            pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)
        return text_surface, text_surface.get_rect()

    def update(self, dw, dh):
        pass

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value
