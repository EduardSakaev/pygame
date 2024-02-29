import colors


class GAME_CONSTANTS:
    GAME_NAME = 'Mahjong game'
    FRAME_RATE = 90
    MAX_CORNERS = 2


class CHIP_CONSTANTS:
    COLUMNS = 15
    ROWS = 8
    UNIQUE_CHIPS = 15


class TEXTURES:
    PATH = 'images'
    BACKGROUND = 'background.jpg'
    CURSOR = 'cursor.png'
    CHIP_NAME_PATTERN = 'icons_64px/monster_{}.png'
    CHIP_BORDER_NAME = 'icons_64px/monster_border.png'
    LINE_NAME = 'icons_64px/line_horizontal.png'
    POINT_NAME = 'icons_64px/dot.png'


class TEXT:
    TEXT_COLOR = colors.YELLOW2
    FONT_NAME = 'Arial'
    FONT_SIZE = 22


class SOUND:
    BACKGROUND = 'sound_effects/background.wav'
    CONNECTION_DONE = 'sound_effects/connection_done.wav'
    CONNECTION_WRONG = 'sound_effects/connection_wrong.wav'
    LEVEL_COMPLETE = 'sound_effects/level_complete.wav'


class STATES:
    NORMAL = 'normal'
    HOVER = 'hover'
    PRESSED = 'pressed'
    FULLSCREEN = 'fullscreen'
