import math
import random
from itertools import cycle

from pygame import image

from constants import CHIP_CONSTANTS, TEXTURES, GAME_CONSTANTS


class MahjongLogic:
    def __init__(self, width, height):
        self.columns = CHIP_CONSTANTS.COLUMNS + 2
        self.rows = CHIP_CONSTANTS.ROWS + 2
        self.chips_count = self.columns * self.rows
        self.max_corners = GAME_CONSTANTS.MAX_CORNERS

        self.chips_matrix = self.create_matrix_game_field()
        chip_obj = image.load('{}'.format(TEXTURES.CHIP_NAME_PATTERN.format('1')))
        self.max_chip_width = self.chip_width = chip_obj.get_width()
        self.max_chip_height = self.chip_height = chip_obj.get_height()
        self.max_game_width = self.game_width = width
        self.max_game_height = self.game_height = height
        self.max_game_height = self.game_height = height
        self.level = 0

    def get_x_y_by_row_column(self, row, column):
        left_top_x, left_top_y = self.get_matrix_top_left_x_y()

        return (left_top_x + column * (self.chip_width + self.space_columns),
                left_top_y + row * (self.chip_height + self.space_rows))

    def get_x_y_by_id(self, index):
        row, col = self.get_row_column_by_array_id(index)
        return self.get_x_y_by_row_column(row, col)

    def get_matrix_top_left_x_y(self):
        left_top_x = (self.game_width - self.columns * (self.chip_width + self.space_columns)) / 2
        left_top_y = (self.game_height - self.rows * (self.chip_height + self.space_rows)) / 2
        return left_top_x, left_top_y

    def get_chip_center_position(self, row, column):
        x, y = self.get_x_y_by_row_column(row, column)
        return x + self.chip_width / 2, y + self.chip_height / 2

    def get_row_column_by_array_id(self, index):
        return int(index / self.columns), int(index % self.columns)

    def get_value_by_row_column(self, row, column):
        return self.chips_matrix[self.get_id_by_row_column(row, column)]

    def get_id_by_row_column(self, row, column):
        return row * self.columns + column

    def create_chips_matrix(self):
        unique_chips = cycle(range(1, CHIP_CONSTANTS.UNIQUE_CHIPS + 1))
        chips = ['{}'.format(next(unique_chips))
                 for _ in range(self.columns - 2) for _ in range(self.rows - 2)]

        # TODO: need to refactor this one
        random.shuffle(chips)
        random.shuffle(chips)
        random.shuffle(chips)
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

    def shuffle_matrix(self):
        data_objects = [(index, value) for index, value in enumerate(self.chips_matrix) if value != 0]
        return random.shuffle(data_objects)

    def can_connect(self, row1, column1, row2, column2):
        cur_row = row1
        cur_col = column1
        verified_paths = list()
        cur_path = list()
        cur_path.append((cur_row, cur_col))
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
            if target and not self.is_max_corners_exceeded(target[0][0], target[0][1], cur_path, number_of_corners):
                cur_path.append(target[0])
                break

            priority = {point: math.hypot(row2 - point[0], column2 - point[1]) for point in next_points}
            priority = sorted(priority, key=lambda x: priority[x])
            for next_row, next_col in priority:
                if next_row >= self.rows or next_row < 0 or next_col >= self.columns or next_col < 0:
                    continue

                path_str = self.path_str(cur_path + [(next_row, next_col)])
                sub_path = [path for path in verified_paths if path_str in path]
                if sub_path or (next_row, next_col) in cur_path:
                    continue

                if (next_row == row2 and next_col == column2 and not self.is_max_corners_exceeded(target[0][0],
                                                                                                  target[0][1],
                                                                                                  cur_path,
                                                                                                  number_of_corners)):
                    cur_path.append((next_row, next_col))
                    is_connected = True
                    break

                if self.get_value_by_row_column(next_row, next_col):
                    continue

                is_corner = False if len(cur_path) < 2 else self.is_corner(next_row, next_col, cur_path[-2][0],
                                                                           cur_path[-2][1], cur_path[-1][0],
                                                                           cur_path[-1][1])
                if is_corner:
                    if number_of_corners == self.max_corners:
                        continue
                    else:
                        number_of_corners += 1

                cur_path.append((next_row, next_col))
                cur_row = next_row
                cur_col = next_col
                break
            else:
                cur_path_str = self.path_str(cur_path)
                sub_path = [path for path in verified_paths if cur_path_str in path]
                if not sub_path:
                    verified_paths.append(cur_path_str)

                len(cur_path) > 0 and cur_path.pop()
                is_corner = False if len(cur_path) < 2 else self.is_corner(cur_row, cur_col,
                                                                           cur_path[-2][0], cur_path[-2][1],
                                                                           cur_path[-1][0], cur_path[-1][1])
                if is_corner:
                    number_of_corners = max(0, number_of_corners - 1)

                if len(cur_path) == 0:
                    break
                cur_row, cur_col = cur_path[-1]

        return cur_path

    def connect(self, row1, column1, row2, column2):
        result = self.can_connect(row1, column1, row2, column2)
        if result:
            for row, column in ((row1, column1), (row2, column2)):
                index = self.get_id_by_row_column(row, column)
                self.chips_matrix[index] = 0

        return result

    def is_cell_empty(self, row, column):
        index = self.get_id_by_row_column(row, column)
        return not self.chips_matrix[index]

    def is_max_corners_exceeded(self, row, column, path, corners):
        is_corner = True if len(path) < 2 else self.is_corner(row, column, path[-2][0], path[-2][1],
                                                              path[-1][0], path[-1][1])
        corners = corners + 1 if is_corner else corners
        return corners > self.max_corners

    def provide_possible_connection(self):
        length = len(self.chips_matrix)
        for index_left in range(length):
            value_left = self.chips_matrix[index_left]

            if value_left == 0 or index_left == len(self.chips_matrix) - 1:
                continue

            for index_right in range(index_left + 1, length):
                value_right = self.chips_matrix[index_right]
                if index_left == index_right or value_right == 0:
                    continue

                if value_left == value_right:
                    row_left, col_left = self.get_row_column_by_array_id(index_left)
                    row_right, col_right = self.get_row_column_by_array_id(index_right)

                    if self.can_connect(row_left, col_left, row_right, col_right):
                        return (row_left, col_left), (row_right, col_right)

    def validate_matrix_on_connectivity(self):
        result = self.provide_possible_connection()
        if not result:
            pass

    def align_chips(self, chips, row_sel_1, col_sel_1, row_sel_2, col_sel_2):
        alignment_conditions = {
            2: lambda row1, col1, row2, col2: col1 == col2 and row1 > row2,  # align top
            3: lambda row1, col1, row2, col2: row1 == row2 and col1 < col2,  # align right
            4: lambda row1, col1, row2, col2: col1 == col2 and row1 < row2,  # align bottom
            5: lambda row1, col1, row2, col2: row1 == row2 and col1 > col2,  # align left
        }

        new_pos = {
            2: lambda row, col, row1, col1, row2, col2: (row - 2, col) if (col1 == col2 and row > row1 and row > row2)
            else (row - 1, col),  # top
            3: lambda row, col, row1, col1, row2, col2: (row, col + 2) if (row1 == row2 and col < col1 and col < col2)
            else (row, col + 1),  # right
            4: lambda row, col, row1, col1, row2, col2: (row + 2, col) if (col1 == col2 and row < row1 and row < row2)
            else (row + 1, col),  # bottom
            5: lambda row, col, row1, col1, row2, col2: (row, col - 2) if (row1 == row2 and col > col1 and col > col2)
            else (row, col - 1),  # left
        }

        if self.level not in alignment_conditions:
            return

        cells_to_align = list()
        for index, _ in enumerate(self.chips_matrix):
            row, col = self.get_row_column_by_array_id(int(index))
            if (alignment_conditions[self.level](row, col, row_sel_1, col_sel_1) or
                    alignment_conditions[self.level](row, col, row_sel_2, col_sel_2)):
                cells_to_align.append((row, col))

        new_chips_positions = dict()
        next_cell = new_pos[self.level](cells_to_align[0][0], cells_to_align[0][1],
                                        row_sel_1, col_sel_1, row_sel_2, col_sel_2)
        direction = (1 if cells_to_align[0][0] + cells_to_align[0][1] > next_cell[0] + next_cell[1]
                     else -1)
        for row, col in cells_to_align[::direction]:
            row_new, col_new = new_pos[self.level](row, col, row_sel_1, col_sel_1, row_sel_2, col_sel_2)
            cur_index = self.get_id_by_row_column(row, col)
            index_swap = self.get_id_by_row_column(row_new, col_new)

            self.chips_matrix[cur_index], self.chips_matrix[index_swap] = \
                self.chips_matrix[index_swap], self.chips_matrix[cur_index]

            for chip in chips.values():
                if chip.row == row and chip.column == col:
                    chip.row = row_new
                    chip.column = col_new
                    chip.left, chip.top = self.get_x_y_by_row_column(row_new, col_new)
                    break

    def shuffle_chips(self, chips):
        counter = len(chips)
        chips_objs = list(chips.values())

        while counter > 0:
            # Generate a random integer between 0 and counter
            rnd = random.randint(0, counter)
            counter -= 1

            # Swap the element at the random index with the element at counter
            self._swap_chips(chips_objs[counter], chips_objs[rnd])
            chips_objs[counter], chips_objs[rnd] = chips_objs[rnd], chips_objs[counter]

    def move_chips(self, level):
        pass

    def _swap_chips(self, obj_left, obj_right):
        matrix_id_left = self.get_id_by_row_column(obj_left.row, obj_left.column)
        matrix_id_right = self.get_id_by_row_column(obj_right.row, obj_right.column)
        self.chips_matrix[matrix_id_left], self.chips_matrix[matrix_id_right] = \
            self.chips_matrix[matrix_id_right], self.chips_matrix[matrix_id_left]

        obj_left.row, obj_right.row = obj_right.row, obj_left.row
        obj_left.column, obj_right.column = obj_right.column, obj_left.column
        obj_left.left, obj_right.left = obj_right.left, obj_left.left
        obj_left.top, obj_right.top = obj_right.top, obj_left.top

    def update_obj_pos(self, obj, x, y):
        obj.left = x
        obj.top = y

    def update(self, new_width, new_height):
        self.game_width = new_width
        self.game_height = new_height

    @staticmethod
    def is_corner(row1, col1, row2, col2, row3, col3):
        return (row1 - row3) * (col2 - col3) != (row2 - row3) * (col1 - col3)

    @staticmethod
    def path_str(path):
        return str(path).replace('[', '').replace(']', '')

    @property
    def space_columns(self):
        return max(1, (self.game_width - self.chip_width * self.columns) * 0.02)

    @property
    def space_rows(self):
        return max(1, (self.game_height - self.chip_height * self.columns) * 0.02)

    @property
    def matrix_width(self):
        return self.columns * (self.chip_width + self.space_columns)

    @property
    def matrix_height(self):
        return self.rows * (self.chip_height + self.space_rows)
