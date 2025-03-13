import ctypes
import sys
import operator

import pygame

from collections import OrderedDict


class SceneDirector:
    def __init__(self, caption):
        self._managers = OrderedDict()
        self._surface = None
        self._width, self._height = 0, 0
        self._init_game(caption)

    def _init_game(self, caption):
        pygame.init()
        pygame.font.init()

        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self.set_windowed_mode()
        self._width, self._height = pygame.display.get_surface().get_size()

    def add_manager(self, manager):
        if manager.name in self._managers:
            self._managers[manager.name].destroy()
        manager.surface = self.surface
        self._managers[manager.name] = manager
        self._managers = OrderedDict({key: value for key, value in sorted(self._managers.items(), key=lambda item:
                                     item[1].scene_priority)})
        manager.create_scene()

    def remove_manager(self, manager_name):
        self._managers = [manager for manager in self._managers if manager.name != manager_name]

    def set_windowed_mode(self):
        self._surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
        if sys.platform == "win32":
            HWND = pygame.display.get_wm_info()['window']
            SW_MAXIMIZE = 3
            ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    def create_scene(self):
        for manager in self._managers.values():
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
        for manager in self._managers.values():
            manager.update()

    def draw(self):
        for manager in self._managers.values():
            manager.draw()

    def handle_mouse_events(self, event_type, pos):
        for manager in self._managers.values():
            manager.handle_mouse_events(event_type, pos)

    def handle_key_down_event(self, key):
        for manager in self._managers.values():
            manager.handle_key_down_event(key)

    def handle_key_up_events(self, key):
        for manager in self._managers.values():
            manager.handle_key_down_event(key)

    def handle_user_event(self, key):
        for manager in self._managers.values():
            manager.handle_user_event(key)

    def handle_game_resize(self):
        self._width, self._height = pygame.display.get_surface().get_size()
        for manager in self._managers.values():
            manager.handle_game_resize(self._width, self._height)
