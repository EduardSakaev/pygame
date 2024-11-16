import pygame


class ImageButton:
    def __init__(self, x, y, text, image_path, sound_path=None):
        self.x = x
        self.y = y

        self.text = text
        self.image = pygame.image.load(image_path)

        self._width = self.image.get_width()
        self._height = self.image.get_height()
        self.image = pygame.transform.scale(self.image, (self._width, self._height * 3))

        self.hover_image = self.image

        self.rect = pygame.rect.Rect(x, y, self._width, self._height)
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        self.is_hovered = False
        self.is_clicked = False

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.image = pygame.transform.scale(self.image, (value, self._height))
        self.rect.width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        self.image = pygame.transform.scale(self.image, (self._width, value * 3))
        self.rect.height = value

    def draw(self, screen):
        # current_image = self.hover_image if self.is_hovered else self.image
        if self.is_clicked:
            screen.blit(self.image, self.rect.topleft, (0, self.height * 2 + 1, self.width, self.height))
        elif self.is_hovered:
            screen.blit(self.image, self.rect.topleft, (0, self.height, self.width, self.height))
        else:
            screen.blit(self.image, self.rect.topleft, (0, 0, self.width, self.height))

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.is_clicked = True
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False

