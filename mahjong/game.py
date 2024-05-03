import sys
from collections import defaultdict

import pygame

from constants import STATES


class Game:
    def __init__(self, frame_rate):
        self._frame_rate = frame_rate
        self._game_over = False
        self._keydown_handlers = defaultdict(list)
        self._keyup_handlers = defaultdict(list)
        self._mouse_handlers = list()
        self._is_game_resized = False
        self._scale_coeff = 1
        self.clock = pygame.time.Clock()

        self._screen_state = STATES.NORMAL
        self._builder = None
        self._director = None

    def update(self):
        self._builder.sort_objects(key=lambda obj: obj.depth)
        for o in self._builder.objects:
            o.update()

    def draw(self):
        for obj in self._builder.objects:
            obj.draw(self._director.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_alt_tab(event)
                self.handle_key_down_event(event.key)
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

    def handle_mouse_events(self, type, pos):
        for handler in self._mouse_handlers:
            handler(type, pos)

    def handle_key_down_event(self, key):
        for handler in self._keydown_handlers[key]:
            handler(key)

    def handle_key_up_events(self, key):
        for handler in self._keyup_handlers[key]:
            handler(key)

    def handle_game_resize(self):
        self._director.width, self._director.height = pygame.display.get_surface().get_size()
        self._is_game_resized = True

    def run(self):
        while not self._game_over:
            self._director.surface.fill((0, 0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self._frame_rate)
