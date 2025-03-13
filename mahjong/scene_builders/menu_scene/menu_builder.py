import pygame

from constants import TEXTURES
from game_elements.cursor import Cursor
from game_elements.image_object_base import ImageObjectBase
from game_elements.button import Button
from sounds import Sounds


class MenuBuilder:
    def __init__(self):
        self._scene_objects = list()
        self._sound_effects = Sounds()
        self._cursor = None
        self._background = None
        self._new_game_button = None
        self._settings_button = None
        self._exit_game_button = None
        self._settings_button = None

    def create_menu(self):
        self.create_background()
        self.create_cursor()
        self.create_new_game_button()
        self.create_settings_button()
        self.create_exit_game_button()
        self.sort_objects()

    def create_background(self):
        display_info = pygame.display.Info()
        self._background = ImageObjectBase(display_info.current_w / 2, display_info.current_h / 2,
                                           TEXTURES.MENU_BG, -70)
        bg_width = self._background.width
        bg_height = self._background.height
        self._background.top = display_info.current_h / 2 - bg_height / 2
        self._background.left = display_info.current_w / 2 - bg_width / 2
        self._scene_objects.append(self._background)

    def create_cursor(self):
        self._cursor = Cursor(TEXTURES.CURSOR, 100)
        self._scene_objects.append(self._cursor)

    def create_new_game_button(self):
        self._new_game_button = Button(100, 100, image_path=TEXTURES.BUTTON, text='new game', depth=5)
        self._new_game_button.attach_to(self._background)
        self._new_game_button.left = 440
        self._new_game_button.top = 200
        self._new_game_button.width = 300
        self._new_game_button.height = 74

        def on_button_click():
            self._sound_effects.sounds['LEVEL_COMPLETE'].play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, key='new_game'))
            # send here user event
        self._new_game_button.button_event += on_button_click
        self._scene_objects.append(self._new_game_button)

    def create_settings_button(self):
        self._settings_button = Button(100, 100, image_path=TEXTURES.BUTTON, text='settings', depth=5)
        self._settings_button.attach_to(self._background)
        self._settings_button.left = 440
        self._settings_button.top = 300
        self._settings_button.width = 300
        self._settings_button.height = 74

        def on_button_click():
            self._sound_effects.sounds['LEVEL_COMPLETE'].play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, key='settings'))

        self._settings_button.button_event += on_button_click
        self._scene_objects.append(self._settings_button)

    def create_exit_game_button(self):
        self._exit_game_button = Button(100, 100, image_path=TEXTURES.BUTTON, text='exit', depth=6)
        self._exit_game_button.attach_to(self._background)
        self._exit_game_button.left = 440
        self._exit_game_button.top = 400
        self._exit_game_button.width = 300
        self._exit_game_button.height = 74

        def on_button_click():
            # self._sound_effects.sounds['LEVEL_COMPLETE'].play()
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            # send here user event
        self._exit_game_button.button_event += on_button_click
        self._scene_objects.append(self._exit_game_button)

    @property
    def sound_effects(self):
        return self._sound_effects

    @property
    def background(self):
        return self._background

    @property
    def cursor(self):
        return self._cursor

    @property
    def new_game_button(self):
        return self._new_game_button

    @property
    def exit_game_button(self):
        return self._exit_game_button

    @property
    def settings_button(self):
        return self._settings_button

    @property
    def scene_objects(self):
        return self._scene_objects

    def sort_objects(self):
        self._scene_objects = sorted(self._scene_objects, key=lambda obj: obj.depth)
