from constants import GAME_CONSTANTS
from game import Game

if __name__ == '__main__':
    Game(GAME_CONSTANTS.GAME_NAME, GAME_CONSTANTS.FRAME_RATE).run()

