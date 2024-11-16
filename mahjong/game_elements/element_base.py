from abc import abstractmethod
from uuid import uuid4

import pygame


class ElementBase:
    def __init__(self, left, top, width, height, depth=0):
        self._bounds = pygame.rect.Rect(left, top, width, height)
        self._depth = depth
        self._unique_id = uuid4()
        self._parent_object = None
        self._attached_objects = dict()

    @property
    def left(self):
        return self._bounds.left - self._parent_object.left if self._parent_object else self._bounds.left

    @left.setter
    def left(self, value):
        delta = self._bounds.left - value
        self._bounds.left = value + self._parent_object.left if self._parent_object else value
        for child in self._attached_objects.values():
            child.left -= delta

    @property
    def top(self):
        return self._bounds.top - self._parent_object.top if self._parent_object else self._bounds.top

    @top.setter
    def top(self, value):
        delta = self._bounds.top - value
        self._bounds.top = value + self._parent_object.top if self._parent_object else value
        for child in self._attached_objects.values():
            child.top -= delta

    @property
    def right(self):
        return self._bounds.right

    @property
    def bottom(self):
        return self._bounds.bottom

    @bottom.setter
    def bottom(self, value):
        self._bounds.bottom = value

    @property
    def width(self):
        return self._bounds.width

    @width.setter
    def width(self, value):
        self._bounds.width = value

    @property
    def height(self):
        return self._bounds.height

    @height.setter
    def height(self, value):
        self._bounds.height = value

    @property
    def center(self):
        return self._bounds.center

    @property
    def centerx(self):
        return self._bounds.centerx

    @property
    def centery(self):
        return self._bounds.centery

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = value

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def handle_events(self, *args, **kwargs):
        pass

    @property
    def rect(self):
        return self._bounds

    @abstractmethod
    def update(self):
        pass

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def attached_objects(self):
        return self._attached_objects

    @property
    def parent_object(self):
        return self._parent_object

    def attach_to(self, parent_object):
        self._parent_object = parent_object
        self._parent_object.attached_objects[self.unique_id] = self

    def detach(self):
        self._parent_object.attached_objects.pop(self.unique_id)
        self._parent_object = None

    def move(self, dx, dy):
        self.left += dx
        self.top += dy

        for child in self.attached_objects:
            child.move(dx, dy)
