import pygame


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

    def run(self):
        while self._is_game_running:
            self._director.surface.fill((0, 0, 0))

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self._clock.tick(self._frame_rate)
