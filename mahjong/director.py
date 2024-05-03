import ctypes
import sys

import pygame


class Director:
    def __init__(self):
        self._builder = None
        self._surface = None
        self._width, self._height = 0, 0

    def set_builder(self, builder):
        self._builder = builder

    def init_game(self, caption):
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self.set_windowed_mode()
        self._width, self._height = pygame.display.get_surface().get_size()

    def set_windowed_mode(self):
        self._surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        if sys.platform == "win32":
            HWND = pygame.display.get_wm_info()['window']
            SW_MAXIMIZE = 3
            ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    def reset_builder(self, new_builder):
        self._builder = new_builder

    def create_objects(self):
        self._builder.create_cursor()
        self._builder.create_background()
        self._builder.create_matrix_background()
        self._builder.create_chips_background()
        self._builder.create_chips()
        self._builder.create_sound_effects()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._surface = value
