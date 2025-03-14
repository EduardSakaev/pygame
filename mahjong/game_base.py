import pygame
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class GameBase:
    def __init__(self, frame_rate):
        self._frame_rate = frame_rate
        self._clock = pygame.time.Clock()
        self._director = None
        self._is_game_running = True

    def update(self):
        pass

    def draw(self):
        pass

    def handle_events(self):
        pass

    def game_tick(self):
        self._director.surface.fill((0, 0, 0))

        self.handle_events()
        self.update()
        self.draw()
        pygame.display.update()

    def run(self):
        tick = LoopingCall(self.game_tick)
        tick.start(1.0 / self._frame_rate)
        reactor.run()
