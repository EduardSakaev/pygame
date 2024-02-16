from pygame import image
from pygame.rect import Rect
from constants import TEXTURES


class ElementBase:
    def __init__(self, left, top, width, height, depth=0, speed=(0, 0)):
        self._bounds = Rect(left, top, width, height)
        self._speed = speed
        self._depth = depth

    @classmethod
    def load_image(cls, image_name):
        return image.load('{}/{}'.format(TEXTURES.PATH, image_name))

    @property
    def left(self):
        return self._bounds.left

    @property
    def right(self):
        return self._bounds.right

    @property
    def top(self):
        return self._bounds.top

    @property
    def bottom(self):
        return self._bounds.bottom

    @property
    def width(self):
        return self._bounds.width

    @property
    def height(self):
        return self._bounds.height

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
        if self._speed == [0, 0]:
            return

        self.move(*self._speed)
