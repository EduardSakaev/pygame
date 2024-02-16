import pygame
import sys

from collections import defaultdict


class Game:
    def __init__(self, caption, width, height, frame_rate):
        self.frame_rate = frame_rate
        self.game_over = False
        pygame.mixer.init(44100, -16, 2, 4096)
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.objects = list()
        self.mouse_handlers = []

    def update(self):
        self.objects = sorted(self.objects, key=lambda object: object.depth)
        for o in self.objects:
            o.update()

    def draw(self):
        for object in self.objects:
            object.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down_event(event.key)
            elif event.type == pygame.KEYUP:
                self.handle_key_up_events(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_events(event.type, event.pos)

    def handle_mouse_events(self, type, pos):
        for handler in self.mouse_handlers:
            handler(type, pos)

    def handle_key_down_event(self, key):
        for handler in self.keydown_handlers[key]:
            handler(key)

    def handle_key_up_events(self, key):
        for handler in self.keyup_handlers[key]:
            handler(key)

    def run(self):
        while not self.game_over:
            self.surface.fill((0, 0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
