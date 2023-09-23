class Shape:
    available_fill_chars = [i for i in range(1, 100)]
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
        for row in self.arr:
            for i in range(0, len(row)):
                if row[i] != self.empty_char:
                    # print("freplaced")
                    row[i] = self.fill_char
        # print(len(arr))

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
        from colorama import Fore, Back, Style

        colors = [
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
                msg += f" {col} "
            msg += "\n"
        print(msg)

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

    @add_history
    def add_below(self, shape_1: "Shape"):
        def simple_add_below(s1, s2):
            s1 = s1.clone()
            for row in s2.arr:
                s1.arr.append(row)
            return s1

        arr = []
        arr.append(simple_add_below(self, shape_1))

        for i in range(1, len(self.arr[0])):  # loop thru the number of columns
            arr.append(simple_add_below(self, shape_1.empty_fill(i, True)))

        for i in range(1, len(shape_1.arr[0])):  # loop thru the number of columns
            arr.append(simple_add_below(self.empty_fill(i, True), shape_1))

        # TODO add below needn't be exactly the row below, row can be merged if the shapes fit in

        """
        eg 
        1 0 0
        1 0 0
        1 0 0
        
        ++++++++
        0 1 1
        1 0 0
        1 0 0
        
        could be 
        
        1 0 0
        1 0 0
        1 1 1
        1 0 0
        1 0 0
        
        """

        return arr

    def add_above(self, shape_1: "Shape"):
        pass

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
