from abc import abstractmethod


class ManagerBase:
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
