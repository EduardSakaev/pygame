import sys

import pygame

from button import ImageButton

pygame.init()
WIDTH, HEIGHT = 600, 550

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Button test')

button_path = 'images/button_new.jpg'
sound_path = 'sounds/level_complete.wav'
green_button = ImageButton(WIDTH / 2 - (252 / 2),
                           100,

                           "new game",
                           image_path=r'images\menu_button_new_2.png',
                           sound_path=sound_path)

green_button.width = 300
green_button.height = 74


def main_menu():
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            green_button.handle_event(event)
        green_button.check_hover(pygame.mouse.get_pos())
        green_button.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main_menu()
