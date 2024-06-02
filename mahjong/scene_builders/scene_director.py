import ctypes
import sys

import pygame
from constants import GAME_CONSTANTS


class SceneDirector:
    def __init__(self, caption):
        self._managers = list()
        self._surface = None
        self._width, self._height = 0, 0
        self._init_game(caption)

    def _init_game(self, caption):
        pygame.mixer.init(GAME_CONSTANTS.AUDIO_FREQUENCY,
                          GAME_CONSTANTS.AUDIO_SIZE,
                          GAME_CONSTANTS.AUDIO_CHANNELS,
                          GAME_CONSTANTS.AUDIO_BUFFER)  # pygame module for loading and playing sounds
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self.set_windowed_mode()
        self._width, self._height = pygame.display.get_surface().get_size()

    def add_manager(self, manager):
        manager.surface = self.surface
        self._managers.append(manager)
        self._managers = sorted(self._managers, key=lambda manager_obj: manager_obj.scene_priority)

    def remove_manager(self, manager):
        self._managers.remove(manager)

    def set_windowed_mode(self):
        self._surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        if sys.platform == "win32":
            HWND = pygame.display.get_wm_info()['window']
            SW_MAXIMIZE = 3
            ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    def create_scene(self):
        for manager in self._managers:
            manager.create_scene()

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

    def update(self):
        for manager in self._managers:
            manager.update()

    def draw(self):
        for manager in self._managers:
            manager.draw()

    def handle_mouse_events(self, event_type, pos):
        for manager in self._managers:
            manager.handle_mouse_events(event_type, pos)

    def handle_key_down_event(self, key):
        for manager in self._managers:
            manager.handle_key_down_event(key)

    def handle_key_up_events(self, key):
        for manager in self._managers:
            manager.handle_key_down_event(key)

    def handle_game_resize(self):
        self._width, self._height = pygame.display.get_surface().get_size()
        for manager in self._managers:
            manager.handle_game_resize(self._width, self._height)
