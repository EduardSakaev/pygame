import sys

import pygame

from constants import STATES
from game_base import GameBase
from scene_builders.menu_scene.menu_manager import MenuManager
from scene_builders.mahjong_scene.mahjong_manager import MahjongManager
from scene_builders.scene_director import SceneDirector


class EventsHandler:
    def __init__(self, director):
        self._director = director

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.key == 'new_game':
                    self.start_new_game()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_alt_tab(event)
                self.handle_key_down_event(event.key)

                if event.key == pygame.K_ESCAPE:
                    action = self.menu_manager.hide if self._is_menu_shown else self.menu_manager.show
                    self._is_menu_shown = False if self._is_menu_shown else True
                    action()

            elif event.type == pygame.KEYUP:
                self.handle_key_up_events(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_events(event.type, event.pos)
            elif event.type == pygame.VIDEORESIZE:
                self.handle_game_resize()

    def handle_alt_tab(self, event):
        if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
            if self._screen_state == STATES.FULLSCREEN:
                self._screen_state = STATES.NORMAL
                self._director.set_windowed_mode()
            elif self._screen_state == STATES.NORMAL:
                self._screen_state = STATES.FULLSCREEN
                self._director.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def handle_game_resize(self):
        self._director.handle_game_resize()

    def handle_mouse_events(self, event_type, pos):
        self._director.handle_mouse_events(event_type, pos)

    def handle_key_down_event(self, key):
        self._director.handle_key_down_event(key)

    def handle_key_up_events(self, key):
        self._director.handle_key_up_events(key)

    def handle_user_event(self, key):
        self._director.handle_user_event(key)