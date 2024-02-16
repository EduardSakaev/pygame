import copy
import math
from itertools import cycle

from pygame import image

from constants import CHIP_CONSTANTS, TEXTURES, GAME_CONSTANTS


class ChipMatrixHelper:
    def __init__(self):
        self.columns = CHIP_CONSTANTS.COLUMNS
        self.rows = CHIP_CONSTANTS.ROWS
        self.chips_count = self.columns * self.rows
        self.max_corners = GAME_CONSTANTS.MAX_CORNERS

        self.chips_matrix = self.create_matrix_game_field()
        chip_obj = image.load('{}/{}'.format(TEXTURES.PATH, TEXTURES.CHIP_NAME_PATTERN.format('1')))
        self.chip_width = chip_obj.get_width()
        self.chip_height = chip_obj.get_height()

    def get_x_y_by_row_column(self, row, column):
        left_top_x = CHIP_CONSTANTS.LEFT_TOP_X
        left_top_y = CHIP_CONSTANTS.LEFT_TOP_Y

        return (left_top_x + column * (self.chip_width + CHIP_CONSTANTS.SPACE_WIDTH),
                left_top_y + row * (self.chip_height + CHIP_CONSTANTS.SPACE_WIDTH))

    def get_row_column_by_array_id(self, index):
        return int(index / self.columns), int(index % self.columns)

    def get_value_by_row_column(self, row, column):
        return self.chips_matrix[self.get_id_by_row_column(row, column)]

    def get_id_by_row_column(self, row, column):
        return row * self.columns + column

    def create_chips_matrix(self):
        unique_chips = cycle(range(1, CHIP_CONSTANTS.UNIQUE_CHIPS + 1))
        chips = [next(unique_chips) for _ in range(self.columns - 2) for _ in range(self.rows - 2)]
        # random.shuffle(chips)
        return chips

    def create_matrix_game_field(self):
        chip_matrix = self.create_chips_matrix()
        game_field_matrix = list()

        index = 0
        for row in range(self.rows):
            for column in range(self.columns):
                if row == 0 or column == 0 or row == self.rows - 1 or column == self.columns - 1:
                    game_field_matrix.append(0)
                else:
                    game_field_matrix.append(chip_matrix[index])
                    index += 1

        return game_field_matrix

    def update_matrix(self, row, column, value):
        self.chips_matrix[self.get_id_by_row_column(row, column)] = value

    def can_connect(self, row1, column1, row2, column2):
        cur_row = row1
        cur_col = column1
        verified_cells = dict()
        path = list()
        verified_cells[(cur_row, cur_col)] = [(row1, column1), 0]
        path.append((cur_row, cur_col))
        number_of_corners = 0

        is_connected = False
        while not is_connected:
            # calculate distance to prioritize direction
            next_points = ((cur_row - 1, cur_col),  # going top
                           (cur_row, cur_col + 1),  # going right
                           (cur_row + 1, cur_col),  # going bottom
                           (cur_row, cur_col - 1))  # going left

            # check if next point is a target point, not depending on priority
            target = [point for point in next_points if point[0] == row2 and point[1] == column2]
            if target and not self.is_max_corners_exceeded(target[0][0], target[0][1], path, number_of_corners):
                path.append(target[0])
                break

            if cur_row == 8 and cur_col == 15:
                a = 5
            priority = {point: math.hypot(row2 - point[0], column2 - point[1]) for point in next_points}
            for next_row, next_col in sorted(priority, key=lambda x: priority[x]):
                if next_row >= self.rows or next_row < 0 or next_col >= self.columns or next_col < 0:
                    continue

                if (next_row, next_col) in verified_cells:
                    continue

                if (next_row == row2 and next_col == column2 and not
                self.is_max_corners_exceeded(target[0][0], target[0][1], path, number_of_corners)):
                    path.append((next_row, next_col))
                    is_connected = True
                    break

                if self.get_value_by_row_column(next_row, next_col):
                    continue

                is_corner = False if len(path) < 2 else self.is_corner(next_row, next_col, path[-2][0], path[-2][1],
                                                                       path[-1][0], path[-1][1])
                if is_corner:
                    if number_of_corners == self.max_corners:
                        continue
                    else:
                        number_of_corners += 1

                path.append((next_row, next_col))
                verified_cells[(next_row, next_col)] = [copy.copy(path), number_of_corners]
                cur_row = next_row
                cur_col = next_col
                break
            else:
                if len(path) > 1:
                    path.pop()

                is_corner = False if len(path) < 2 else self.is_corner(cur_row, cur_col, path[-2][0], path[-2][1],
                                                                       path[-1][0], path[-1][1])
                if is_corner:
                    number_of_corners = max(0, number_of_corners - 1)


                cur_row, cur_col = path[-1]

            if len(path) == 1:
                break

        for cell, value in verified_cells.items():
            print('{}:{}'.format(cell, value))

        if len(path) == 1:
            return None
        return path

    def connect(self, row1, column1, row2, column2):
        for row, column in ((row1, column1), (row2, column2)):
            index = self.get_id_by_row_column(row, column)
            self.chips_matrix[index] = 0

    def is_cell_empty(self, row, column):
        index = self.get_id_by_row_column(row, column)
        return not self.chips_matrix[index]

    @staticmethod
    def is_corner(row1, col1, row2, col2, row3, col3):
        return (row1 - row3) * (col2 - col3) != (row2 - row3) * (col1 - col3)

    def is_max_corners_exceeded(self, row, column, path, corners):
        is_corner = True if len(path) < 2 else self.is_corner(row, column, path[-2][0], path[-2][1],
                                                              path[-1][0], path[-1][1])
        corners = corners + 1 if is_corner else corners
        return corners > self.max_corners
