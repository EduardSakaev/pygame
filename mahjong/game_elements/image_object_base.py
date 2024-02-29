import pygame

from constants import TEXTURES
from game_elements.element_base import ElementBase


class ImageObjectBase(ElementBase):
    def __init__(self, left, top, image_name, depth=0):
        self._image_name = image_name
        self._image_obj = self.load_image(image_name).convert_alpha()
        self._max_width = self._image_obj.get_width()
        self._max_height = self._image_obj.get_height()
        self._angle = 0
        self._start_track_time = None

        ElementBase.__init__(self, left, top, self._max_width, self._max_height, depth)

    @property
    def image_name(self):
        return self._image_name

    @classmethod
    def load_image(cls, image_name):
        return pygame.image.load('{}/{}'.format(TEXTURES.PATH, image_name))

    @property
    def alpha(self):
        return self._image_obj.get_alpha()

    @alpha.setter
    def alpha(self, value):
        self._image_obj.set_alpha(value)

    @property
    def angle(self):
        return self._angle

    @property
    def image_obj(self):
        return self._image_obj

    def draw(self, surface):
        surface.blit(self._image_obj, self._bounds)

    def rotate(self, angle):
        self._angle = angle
        self._image_obj = pygame.transform.rotate(self._image_obj, angle)

    def scale(self, width, height, angle=0):
        image_obj = self.load_image(self.image_name)
        self._image_obj = pygame.transform.smoothscale(image_obj, (width, height))
        self._bounds.width = width
        self._bounds.height = height
        self.rotate(angle)

    def update(self):
        pass

    def delay_exec(self, func, timeout):
        if not self._start_track_time:
            self._start_track_time = pygame.time.get_ticks()

        if (pygame.time.get_ticks() - self._start_track_time) / 1000.0 > timeout:
            func()
            self._start_track_time = None
