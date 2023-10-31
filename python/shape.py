import os
import pickle
from typing import List

from colorama import Fore, Style, Back

from exception import ShapeException


class Shape:
    instance_count = 0
    available_fill_chars = list(range(2, 100))
    empty_char = 0
    history = []
    arr = []
    unique_fill_char = True
    fill_char = -1

    instance_id = -1
    active_instance_ids = set()

    def __init__(self, arr):
        def convert_to_matrix():
            # Clone a new copy to avoid giving an array reference outside.
            new_arr = [r[:] for r in arr]
            max_cols = 0
            for r in new_arr:
                if len(r) > max_cols:
                    max_cols = len(r)

            # print(f"Matrix size is {len(new_arr)},{max_cols}")

            for r in new_arr:
                for _ in range(0, max_cols - len(r)):
                    r.append(self.empty_char)
            self.arr = new_arr

        if not arr:
            raise ShapeException("Passed array couldn't be null or empty")

        # print(
        #     f"Fill Char is {self.fill_char} , remaining fill chars {Shape.available_fill_chars}"
        # )
        convert_to_matrix()
        if Shape.unique_fill_char:
            for row in self.arr:
                for i, _ in enumerate(row):
                    if row[i] == 1:
                        # print("replaced")
                        if self.fill_char == -1:
                            self.fill_char = Shape.available_fill_chars.pop(0)
                        row[i] = self.fill_char
        # print(len(arr))
        Shape.instance_count += 1
        self.instance_id = Shape.instance_count
        Shape.active_instance_ids.add(self.instance_id)

    def __del__(self):
        # print(f'Destructing instance {self.instance_id}')
        # Double check because when loaded from file, there may be multiple shapes instances with same instance id
        if self.instance_id in Shape.active_instance_ids:
            Shape.active_instance_ids.remove(self.instance_id)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Shape):
            return self.arr == other.arr
        return False

    def __str__(self) -> str:
        msg = ""
        for row in self.arr:
            for col in row:
                msg += f" {col} "
            msg += "\n"
        return msg

    def empty_fill(self, no_of_empty_chars, before=False):
        s = self.clone()
        for row in s.arr:
            for _ in range(no_of_empty_chars):
                if before:
                    row.insert(0, s.empty_char)
                else:
                    row.append(s.empty_char)
        return s

    def print(self, prefix="\n"):
        # fg_colors = [
        #     Fore.BLACK,
        #     Fore.BLUE,
        #     Fore.CYAN,
        #     Fore.GREEN,
        #     Fore.LIGHTBLUE_EX,
        #     Fore.LIGHTGREEN_EX,
        #     Fore.LIGHTMAGENTA_EX,
        #     Fore.LIGHTRED_EX,
        #     Fore.LIGHTRED_EX,
        # ]
        bg_colors = [
            Back.BLACK,
            Back.BLUE,
            Back.CYAN,
            Back.GREEN,
            Back.LIGHTBLUE_EX,
            Back.LIGHTGREEN_EX,
            Back.LIGHTMAGENTA_EX,
            Back.LIGHTRED_EX,
            Back.LIGHTRED_EX,
        ]
        # print(prefix)
        msg = ""

        for row in self.arr:
            for col in row:
                # msg += fg_colors[col % 7]
                msg += Fore.BLACK
                msg += bg_colors[col % 8]
                msg += f" {col:2} "
                msg += Style.RESET_ALL
            msg += "\n"
        print(msg)
        # print(Style.RESET_ALL)

    def size(self):
        return len(self.arr), len(self.arr[0])

    def clone_arr(self):
        return [row[:] for row in self.arr]

    def clone(self):
        return Shape(self.clone_arr())

    def dump_to_file(self, folder_path="./solved shapes"):
        file_path = f"{folder_path}/{self.instance_id}.shape"
        with open(f"{file_path}", "wb") as f:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            pickle.dump(self, f)
        return file_path

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def flips(self):
        # Vertical, horizontal, vertical-horizontal filips
        def horizontal_flip_matrix(matrix):
            flipped_matrix = []
            for row in matrix:
                flipped_row = row[::-1]  # Reverse the order of elements in the row
                flipped_matrix.append(flipped_row)
            return flipped_matrix

        def vertical_flip_matrix(matrix):
            flipped_matrix = matrix[::-1]  # Reverse the order of rows in the matrix
            return flipped_matrix

        arr = self.clone_arr()
        hf_arr = horizontal_flip_matrix(arr)
        vf_arr = vertical_flip_matrix(arr)
        hvf_arr = vertical_flip_matrix(hf_arr)

        return [
            Shape(arr),
            Shape(hf_arr),
            Shape(vf_arr),
            Shape(hvf_arr),
        ]

    @staticmethod
    def rotate_matrix_90_clockwise(matrix):
        if not matrix:
            return []

        num_rows, num_cols = len(matrix), len(matrix[0])
        rotated_matrix = [[0] * num_rows for _ in range(num_cols)]

        for i in range(num_rows):
            for j in range(num_cols):
                rotated_matrix[j][num_rows - i - 1] = matrix[i][j]

        return rotated_matrix

    def rotations(self):
        # All 90 degree rotations, total 4
        arr = self.clone_arr()
        arr_90 = self.rotate_matrix_90_clockwise(arr)
        arr_180 = self.rotate_matrix_90_clockwise(arr_90)
        arr_270 = self.rotate_matrix_90_clockwise(arr_180)
        return [Shape(arr), Shape(arr_90), Shape(arr_180), Shape(arr_270)]

    @staticmethod
    def add_history(f):
        def decorator(*args, **kwargs):
            # print(args)
            self = args[0]
            # new_arr = [row[:] for row in self.arr]
            # self.history.append(new_arr)
            return f(*args, **kwargs)

        return decorator

    def revert(self):
        if self.history:
            # print("Before Pop", self.history)
            self.arr = self.history.pop()
            # print("After Pop", self.history)
            return True
        return False

    @add_history
    def rotate_right(self):
        return Shape(self.rotate_matrix_90_clockwise(self.arr))

    @add_history
    def rotate_left(self):
        # Rotate right side 3 times
        arr = self.clone_arr()
        # Use zip to transpose the matrix (swap rows and columns)
        arr_90 = self.rotate_matrix_90_clockwise(arr)
        arr_180 = self.rotate_matrix_90_clockwise(arr_90)
        arr_270 = self.rotate_matrix_90_clockwise(arr_180)
        return Shape(arr_270)

    @staticmethod
    def merge_add_below(s1: "Shape", s2: "Shape"):
        """
        Loop s1 from bottom to top
        loop s2 from top to bottom
        """
        # print("Incoming merge request for ")
        # s1.print()
        # s2.print()
        arr1: List[List[int]] = s1.arr
        arr2: List[List[int]] = s2.arr
        len_1 = len(arr1)
        len_2 = len(arr2)
        min_row_count = len_1 if len_1 <= len_2 else len_2

        merged_shapes = []
        for i in range(min_row_count):
            # check if mergeable
            is_mergeable = True
            for j in range(i + 1):
                # print(f"{len_1}, {j}")
                row1 = arr1[(len_1 - 1) - j]  # start from the last row
                row2 = arr2[j]
                # print(f"Row1 {row1}")
                # print(f"Row2 {row2}")
                min_col_len = len(row1) if len(row1) <= len(row2) else len(row2)
                for k in range(min_col_len):
                    if row1[k] != s1.empty_char and row2[k] != s2.empty_char:
                        is_mergeable = False
                        # print(f"Breaking merge at row {i}")
                        # break
                    else:
                        pass
                        # print("No breaking merge")
                if not is_mergeable:
                    break

            if not is_mergeable:
                break

            # if the code is here it means its mergeable up to i rows
            # print(f"mergeable up to {i} rows")
            cln_1 = s1.clone_arr()
            cln_2 = s2.clone_arr()

            for j in range(i + 1):
                row1 = cln_1[(len_1 - 1) - j]
                row2 = cln_2[j]
                min_col_len = len(row1) if len(row1) <= len(row2) else len(row2)
                for k in range(min_col_len):
                    if row1[k] == s1.empty_char and row2[k] != s2.empty_char:
                        row1[k] = row2[k]
                        # print(f"Replaced at index {j}{k}")
                    elif (row1[k] != s1.empty_char and row2[k] == s2.empty_char) or (
                        row1[k] == s1.empty_char and row2[k] == s2.empty_char
                    ):
                        pass  # retain the value
                    else:
                        # print("Wrong condition")
                        raise ShapeException("Wrong condition in the logic")
                # if the second array has larger number of columns , append the remaining ones
                for k in range(min_col_len, len(row2)):
                    row1.append(row2[k])

            for k in range(i + 1, len(cln_2)):
                row = cln_2[k]
                cln_1.append(row)
            merged_shapes.append(Shape(cln_1))

        return merged_shapes

        # merge the mergeable rows

    def shift_combinations(self, shape_1: "Shape") -> list[tuple["Shape", "Shape"]]:
        combinations = []
        for i in range(1, len(self.arr[0])):  # loop through the number of columns
            combinations.append((self, shape_1.empty_fill(i, True)))
        for i in range(1, len(shape_1.arr[0])):  # loop through the number of columns
            combinations.append((self.empty_fill(i, True), shape_1))

        return combinations

    @add_history
    def add_below(self, shape_1: "Shape"):
        """
        Add the argument shape below the current shape
        """

        def simple_add_below(s1: "Shape", s2: "Shape") -> Shape:
            cln_arr = s1.clone_arr()
            for row in s2.arr:
                cln_arr.append(row)
            return Shape(cln_arr)

        arr = [simple_add_below(self, shape_1)]
        arr.extend(Shape.merge_add_below(self, shape_1))

        shift_combinations = self.shift_combinations(shape_1)
        for combination in shift_combinations:
            arr.append(simple_add_below(combination[0], combination[1]))
            arr.extend(Shape.merge_add_below(combination[0], combination[1]))
        return arr

    def add_above(self, shape_1: "Shape") -> List:
        return shape_1.add_below(self)

    def add_left(self, shape: "Shape") -> List:
        s1_left_rotated = self.rotate_left()
        # s1_left_rotated.print()
        s2_left_rotated = shape.rotate_left()
        # s2_left_rotated.print()

        shapes = s1_left_rotated.add_below(s2_left_rotated)
        final_shapes = [s.rotate_right() for s in shapes]
        return final_shapes

    def add_right(self, shape_1: "Shape") -> List:
        return shape_1.add_left(self)

    def empty_slot_exits(self):
        for row in self.arr:
            for val in row:
                if val == self.empty_char:
                    # print(f"Empty char found at row {row} , so shape is not solved")
                    return True
        return False
