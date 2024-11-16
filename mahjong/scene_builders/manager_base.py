from abc import abstractmethod


class ManagerBase:
    def __init__(self):
        self._manager_name = ''
        self._is_scene_created = False
        self._is_hidden = False

    @abstractmethod
    def create_scene(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def handle_mouse_events(self, type, pos):
        pass

    @abstractmethod
    def handle_key_down_event(self, key):
        pass

    @abstractmethod
    def handle_key_up_events(self, key):
        pass

    @abstractmethod
    def handle_game_resize(self, new_width, new_height):
        pass

    @abstractmethod
    def scene_priority(self):
        pass

    @property
    def name(self):
        return self._manager_name

    @property
    def is_created(self):
        return self._is_scene_created

    @property
    def is_hidden(self):
        return self._is_hidden
