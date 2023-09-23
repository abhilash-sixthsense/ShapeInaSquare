from colorama import Fore, Style
from typing import List


class Shape:
    instace_count = 0
    available_fill_chars = list(range(1, 100))
    empty_char = "0"
    history = []
    arr = []

    def __init__(self, arr, empty_char=0, unique_fill_char=False):
        def convert_to_matrix():
            # Clone a new copy to avoid giving an array reference outside.
            new_arr = [row[:] for row in arr]
            max_cols = 0
            for row in new_arr:
                if len(row) > max_cols:
                    max_cols = len(row)

            # print(f"Matrix size is {len(new_arr)},{max_cols}")

            for row in new_arr:
                for _ in range(0, max_cols - len(row)):
                    row.append(self.empty_char)
            self.arr = new_arr

        if not arr:
            raise BaseException("Passed array couldn't be null or empty")
        self.empty_char = empty_char
        if unique_fill_char:
            self.fill_char = Shape.available_fill_chars.pop(0)
        else:
            self.fill_char = 1

        # print(
        #     f"Fill Char is {self.fill_char} , remaining fill chars {Shape.available_fill_chars}"
        # )
        convert_to_matrix()
        if unique_fill_char:
            for row in self.arr:
                for i in range(0, len(row)):
                    if row[i] != self.empty_char:
                        # print("freplaced")
                        row[i] = self.fill_char
        # print(len(arr))
        Shape.instace_count += 1

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
        colors = [
            Fore.BLACK,
            Fore.BLUE,
            Fore.CYAN,
            Fore.GREEN,
            Fore.LIGHTBLUE_EX,
            Fore.LIGHTGREEN_EX,
            Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTRED_EX,
            Fore.LIGHTRED_EX,
        ]
        print(prefix)
        msg = ""

        for row in self.arr:
            for col in row:
                msg += colors[col % 8]
                msg += f" {col:3} "
            msg += "\n"
        print(msg)
        print(Style.RESET_ALL)

    def size(self):
        return (len(self.arr), len(self.arr[0]))

    def clone_arr(self):
        return [row[:] for row in self.arr]

    def clone(self):
        return Shape(self.clone_arr())

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

    def rotations(self):
        def rotate_matrix_90_clockwise(matrix):
            if not matrix:
                return []

            num_rows, num_cols = len(matrix), len(matrix[0])
            rotated_matrix = [[0] * num_rows for _ in range(num_cols)]

            for i in range(num_rows):
                for j in range(num_cols):
                    rotated_matrix[j][num_rows - i - 1] = matrix[i][j]

            return rotated_matrix

        # All 90 degree rotations, total 4
        arr = self.clone_arr()
        arr_90 = rotate_matrix_90_clockwise(arr)
        arr_180 = rotate_matrix_90_clockwise(arr_90)
        arr_270 = rotate_matrix_90_clockwise(arr_180)
        return [Shape(arr), Shape(arr_90), Shape(arr_180), Shape(arr_270)]

    @staticmethod
    def add_history(f):
        def decorator(*args, **kwargs):
            print(args)
            self = args[0]
            new_arr = [row[:] for row in self.arr]
            self.history.append(new_arr)
            return f(*args, **kwargs)

        return decorator

    def revert(self):
        if self.history:
            print("Before Pop", self.history)
            self.arr = self.history.pop()
            print("After Pop", self.history)
            return True
        return False

    @add_history
    def rotate_right(self):
        self.arr = list(zip(*self.arr[::-1]))

    @add_history
    def rotate_left(self):
        # Not the best way, use this till an optinmal solution is found
        for _ in range(0, 3):
            self.arr = list(zip(*self.arr[::-1]))

    @staticmethod
    def merge_add_below(s1: "Shape", s2: "Shape"):
        """
        Loop s1 from bottom to top
        loop s2 from top to bottom
        """
        print("Incoming merge request for ")
        s1.print()
        s2.print()
        arr1: List[List[int]] = s1.arr
        arr2: List[List[int]] = s2.arr
        len_1 = len(arr1)
        len_2 = len(arr2)
        min_row_count = len_1 if len_1 <= len_2 else len_2

        merged_shapes = []
        for i in range(min_row_count):
            # check if mergable
            is_mergable = True
            for j in range(i + 1):
                print(f"{len_1}, {j}")
                row1 = arr1[(len_1 - 1) - j]  # start from the last row
                row2 = arr2[j]
                print(f"Row1 {row1}")
                print(f"Row2 {row2}")
                min_col_len = len(row1) if len(row1) <= len(row2) else len(row2)
                for k in range(min_col_len):
                    if row1[k] != s1.empty_char and row2[k] != s2.empty_char:
                        is_mergable = False
                        print(f"Breaking merge at row {i}")
                        break
                    else:
                        print(f"No breaking merge")
                if not is_mergable:
                    break

            if not is_mergable:
                break

            # if the code is here it means its mergable up to i rows
            print(f"Mergable up to {i} rows")
            cln_1 = s1.clone_arr()
            cln_2 = s2.clone_arr()

            for j in range(i + 1):
                row1 = cln_1[(len_1 - 1) - j]
                row2 = cln_2[j]
                min_col_len = len(row1) if len(row1) <= len(row2) else len(row2)
                for k in range(min_col_len):
                    if row1[k] == s1.empty_char and row2[k] != s2.empty_char:
                        row1[k] = row2[k]
                        print(f"Replaced at index {j}{k}")
                    elif (row1[k] != s1.empty_char and row2[k] == s2.empty_char) or (
                        row1[k] == s1.empty_char and row2[k] == s2.empty_char
                    ):
                        pass  # retain the value
                    else:
                        print("Wrong condition")
                        raise Exception("Wrong condition in the logic")
                # if the second array has larger number of colums , append the remaining ones
                for k in range(min_col_len, len(row2)):
                    row1.append(row2[k])

            for k in range(i + 1, len(cln_2)):
                row = cln_2[k]
                cln_1.append(row)
            merged_shapes.append(Shape(cln_1))

        return merged_shapes

        # merge the mergable rows

    @add_history
    def add_below(self, shape_1: "Shape"):
        def simple_add_below(s1: "Shape", s2: "Shape"):
            arr = s1.clone_arr()
            for row in s2.arr:
                arr.append(row)
            return Shape(arr)

        arr = []
        arr.append(simple_add_below(self, shape_1))
        arr.extend(Shape.merge_add_below(self, shape_1))

        for i in range(1, len(self.arr[0])):  # loop thru the number of columns
            arr.append(simple_add_below(self, shape_1.empty_fill(i, True)))
            arr.extend(Shape.merge_add_below(self, shape_1.empty_fill(i, True)))

        for i in range(1, len(shape_1.arr[0])):  # loop thru the number of columns
            arr.append(simple_add_below(self.empty_fill(i, True), shape_1))
            arr.extend(Shape.merge_add_below(self.empty_fill(i, True), shape_1))

        return arr

    def add_above(self, shape_1: "Shape"):
        return shape_1.add_below(self)

    def add_left(self, shape_1: "Shape"):
        pass

    def add_right(self, shape_1: "Shape"):
        pass


class Board:
    shapes = [Shape([[1, 1, 1, 1], [1, 1]]), Shape([[1, 1, 1, 1], [1, 1, 1]])]
    # board size
    size = (8, 8)
    empty_char = " "

    solved_shapes = []

    @staticmethod
    def __is_solved(shape: Shape):
        # write the check solved logic
        # check the size of the shape is equal to the size of the board
        shape_size = shape.size()
        size_fit = shape_size[0] == Board.size[0] or shape_size[1] == Board.size[1]
        if not size_fit:
            return False
        are_all_cells_filled = True
        for row in shape.clone_arr():
            for val in row:
                if val == Board.empty_char:
                    print(f"Empty char found at row {row} , so shape is not solved")
                    are_all_cells_filled = False

        return are_all_cells_filled

    def __is_error(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    @staticmethod
    def __horizontal_flip(arr):
        pass

    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        print(
            f"Inside __try_combinations shape {shape} , list : {remaining_shapes_list}"
        )

        if len(remaining_shapes_list) == 1:
            # Just try combinations and no need to procced further
            shape_1 = remaining_shapes_list[0]

            shape.add_above(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_below(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_left(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_right(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()
        else:
            shape_1 = remaining_shapes_list[0]

            shape.add_above(shape_1)
            if not self.__is_error(shape):
                self.__try_combinations(shape, remaining_shapes_list[1:])

            shape.revert()

            shape.add_below(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_left(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_right(shape_1)
            if self.__is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

    def solve(self):
        self.__try_combinations(self.shapes[0], self.shapes[1:])
        if self.solved_shapes:
            print(f"There are {len(self.solved_shapes)} combinations")
        else:
            print("No solved combinations")


if __name__ == "__main__":
    b = Board()
    b.solve()
# s1 = Shape([[1, 1, 1, 1], [1, 1]])
# print(s1)
# s2 = Shape(s1.arr)

# s1.rotate_right()
# print(s1)

# s1.rotate_left()
# print(s1)
# s1.revert()
# print(s1)
# s1.print()

# s2.add_below(s1)
# # print(s2)
# s1.add_below(s2)
