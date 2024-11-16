import pygame

from constants import GAME_CONSTANTS, SOUNDS


class SoundsMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Sounds(metaclass=SoundsMeta):
    def __init__(self):
        pygame.mixer.init(GAME_CONSTANTS.AUDIO_FREQUENCY,
                          GAME_CONSTANTS.AUDIO_SIZE,
                          GAME_CONSTANTS.AUDIO_CHANNELS,
                          GAME_CONSTANTS.AUDIO_BUFFER)  # pygame module for loading and playing sounds

        self._sounds = {name: pygame.mixer.Sound(getattr(SOUNDS, name)) for name in SOUNDS.__dict__.keys() if
                        '__' not in name}

    @property
    def sounds(self):
        return self._sounds

    def set_sounds_volume(self, value):
        for sound in self.sounds.values():
            sound.set_volume(value)
