import sys
import ctypes
import pygame

from collections import defaultdict
from constants import STATES

class Game:
    def __init__(self, caption, frame_rate):
        self.frame_rate = frame_rate
        self.game_over = False
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.objects = list()
        self.mouse_handlers = []
        self.screen_state = STATES.NORMAL
        self.surface = None
        self.cur_width = 0
        self.cur_height = 0
        self.max_window_sizes = list()  # fullscreen mode size, windowed max size
        self.dw_pr = 0
        self.dh_pr = 0
        self._is_game_resized = False
        self._display_info = None
        self._init_pygame(caption)
        self.clock = pygame.time.Clock()

    def _set_windowed_mode(self):
        self.surface = pygame.display.set_mode((self.cur_width, self.cur_height), pygame.RESIZABLE)
        if sys.platform == "win32":
            HWND = pygame.display.get_wm_info()['window']
            SW_MAXIMIZE = 3
            ctypes.windll.user32.ShowWindow(HWND, SW_MAXIMIZE)

    def _init_pygame(self, caption):
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self._display_info = pygame.display.Info()  # fullscreen sizes
        self._set_windowed_mode()
        self.cur_width, self.cur_height = pygame.display.get_surface().get_size()
        self.max_window_sizes.append((self._display_info.current_w, self._display_info.current_h))
        self.max_window_sizes.append((self.cur_width, self.cur_height))

    def update(self):
        self.objects = sorted(self.objects, key=lambda obj: obj.depth)
        for o in self.objects:
            o.update()
        # self.dw_pr, self.dh_pr = 0, 0

    def draw(self):
        for obj in self.objects:
            obj.draw(self.surface)

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
                # if self.cur_width != self.max_width or self.cur_height != self.max_height:
                #     self.screen_state = 'normal'

    def handle_alt_tab(self, event):
        if event.mod & pygame.KMOD_ALT and event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
            if self.screen_state == STATES.FULLSCREEN:
                self.screen_state = STATES.NORMAL
                self._set_windowed_mode()
            elif self.screen_state == STATES.NORMAL:
                self.screen_state = STATES.FULLSCREEN
                self.surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def handle_mouse_events(self, type, pos):
        for handler in self.mouse_handlers:
            handler(type, pos)

    def handle_key_down_event(self, key):
        for handler in self.keydown_handlers[key]:
            handler(key)

    def handle_key_up_events(self, key):
        for handler in self.keyup_handlers[key]:
            handler(key)

    def handle_game_resize(self):
        self.cur_width, self.cur_height = pygame.display.get_surface().get_size()

        print('{} _ {}'.format(self.cur_width, self.cur_height))
        self._is_game_resized = True
        # if (cur_width, cur_height) in self.max_window_sizes:
        #     self.dw_pr, self.dh_pr = 1, 1
        # else:
        #     self.dw_pr = (cur_width - self.cur_width) / self.cur_width
        #     self.dh_pr = (cur_height - self.cur_height) / self.cur_height
        # ,  = cur_width, cur_height

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
