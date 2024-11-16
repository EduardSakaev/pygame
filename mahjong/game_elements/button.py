import pygame

from constants import FONTS
from game_elements.event import Event
from game_elements.image_object_base import ImageObjectBase


class Button(ImageObjectBase):
    """
    Button loads as image with 3 layers (normal button, hovered button, clicked button)
    """

    def __init__(self, top, left, image_path, text='', is_layered_button=True, depth=0):
        ImageObjectBase.__init__(self, left, top, image_path, depth)
        height = self._height * 3 if is_layered_button else self._height
        self._image_obj = pygame.transform.scale(self._image_obj, (self._width, height))

        self._is_layered_button = is_layered_button
        self._font = FONTS.ARIAL
        self._text = text
        self._is_hovered = False
        self._is_clicked = False
        self._layer_height = None
        self.button_event = Event()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def draw(self, surface):
        bottom = 0
        if self._is_layered_button:
            bottom = self.height if self._is_hovered else bottom
            bottom = self.height * 2 + 1 if self._is_clicked else bottom
        surface.blit(self._image_obj, self.rect.topleft, (0, bottom, self.width, self.height))

        if self._text:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def handle_events(self, event_type, mouse_pos):
        if event_type == pygame.MOUSEMOTION:
            self._is_hovered = self.rect.collidepoint(mouse_pos)
        if event_type == pygame.MOUSEBUTTONDOWN and self._is_hovered:
            self._is_clicked = True

            self.button_event()
        elif event_type == pygame.MOUSEBUTTONUP:
            self._is_clicked = False

    @ImageObjectBase.height.setter
    def height(self, value):
        self._height = value
        height = value * 3 if self._is_layered_button else value
        self._image_obj = pygame.transform.scale(self._image_obj, (self._width, height))
        self.rect.height = value

    @property
    def is_layered_button(self):
        return self._is_layered_button

