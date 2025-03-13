import pygame

from scene_builders.manager_base import ManagerBase
from scene_builders.menu_scene.menu_builder import MenuBuilder


class MenuManager(ManagerBase):
    """
    Creates all objects related to mahjong scene + includes game logic
    """

    def __init__(self, width, height):
        super().__init__()
        self._width, self._height = width, height
        self._menu_builder = MenuBuilder()
        self._scene_priority = 2
        self._mouse_handlers = []
        self._surface = None
        self._is_game_resized = False
        self._is_scene_created = False
        self._manager_name = MenuManager.__name__

    def create_scene(self):
        #  need to make it as decorator
        if not self._is_scene_created:
            self._menu_builder.create_menu()
            self._mouse_handlers.append(self._menu_builder.cursor.handle_events)
            self._mouse_handlers.append(self._menu_builder.new_game_button.handle_events)
            self._mouse_handlers.append(self._menu_builder.exit_game_button.handle_events)
            self._mouse_handlers.append(self._menu_builder.settings_button.handle_events)
            self._is_scene_created = True

    def update(self):
        # need to make it as decorator !!!!!
        if not self._is_hidden:
            for scene_object in self._menu_builder.scene_objects:
                scene_object.update()

    def draw(self):
        if not self._is_hidden:
            for scene_object in self._menu_builder.scene_objects:
                scene_object.draw(self._surface)

    def handle_mouse_events(self, event_type, pos):
        if not self._is_hidden:
            for handler in self._mouse_handlers:
                handler(event_type, pos)

    def handle_key_down_event(self, key):
        if not self._is_hidden:
            delta = 3
            if key == pygame.K_DOWN:
                self._menu_builder.background.top += delta
            elif key == pygame.K_UP:
                self._menu_builder.background.top -= delta
            elif key == pygame.K_LEFT:
                self._menu_builder.background.left -= delta
            elif key == pygame.K_RIGHT:
                self._menu_builder.background.left += delta

    def handle_key_up_events(self, key):
        pass

    @property
    def scene_priority(self):
        return self._scene_priority

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, surface):
        self._surface = surface

    @property
    def manager_name(self):
        return 'menu_manager'

    def hide(self):
        self._is_hidden = True

    def show(self):
        self._is_hidden = False
