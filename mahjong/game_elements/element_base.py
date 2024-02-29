import pygame


class ElementBase:
    def __init__(self, left, top, width, height, depth=0):
        self._bounds = pygame.rect.Rect(left, top, width, height)
        self._depth = depth

    @property
    def left(self):
        return self._bounds.left

    @left.setter
    def left(self, value):
        self._bounds.left = value

    @property
    def right(self):
        return self._bounds.right

    @property
    def top(self):
        return self._bounds.top

    @top.setter
    def top(self, value):
        self._bounds.top = value

    @property
    def bottom(self):
        return self._bounds.bottom

    @bottom.setter
    def bottom(self, value):
        self._bounds.bottom = value

    @property
    def width(self):
        return self._bounds.width

    @width.setter
    def width(self, value):
        self._bounds.width = value

    @property
    def height(self):
        return self._bounds.height

    @height.setter
    def height(self, value):
        self._bounds.height = value

    @property
    def center(self):
        return self._bounds.center

    @property
    def centerx(self):
        return self._bounds.centerx

    @property
    def centery(self):
        return self._bounds.centery

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    def draw(self, surface):
        pass

    def handle(self, *args, **kwargs):
        pass

    @property
    def rect(self):
        return self._bounds

    def move(self, dx, dy):
        self._bounds = self._bounds.move(dx, dy)

    def update(self):
        pass
