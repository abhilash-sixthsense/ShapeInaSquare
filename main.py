print("hi")


class Shape:
    fill_char = "1"
    empty_char = "0"
    history = []
    arr = []

    def __init__(self, arr, empty_char=" ", fill_char="1"):
        def convert_to_matrix():
            # Clone a new copy to avoid giving an array reference outside.
            new_arr = [row[:] for row in arr]
            max_cols = 0
            for row in new_arr:
                if len(row) > max_cols:
                    max_cols = len(row)

            print(f"Matrix size is {len(new_arr)},{max_cols}")

            for row in new_arr:
                for _ in range(0, max_cols - len(row)):
                    row.append(self.empty_char)
            self.arr = new_arr

        if not arr:
            raise BaseException("Passed array couldn't be null or empty")
        self.empty_char = empty_char
        self.fill_char = fill_char
        convert_to_matrix()
        print(len(arr))

    def __str__(self) -> str:
        msg = ""
        for row in self.arr:
            for col in row:
                msg += f" {col} "
            msg += "\n"
        return msg

    def print(self):
        print(self)

    def size(self):
        return (len(self.arr), len(self.arr[0]))

    def clone_arr(self):
        return [row[:] for row in self.arr]

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
        for row in shape_1.arr:
            self.arr.append(row)
        self.print()

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
