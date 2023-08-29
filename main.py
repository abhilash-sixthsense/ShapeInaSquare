print("hi")


class Shape:
    fill_char = "1"
    empty_char = "0"
    history = []
    arr = []

    def __init__(self, arr):
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


class Board:
    shapes = [Shape([[1, 1, 1, 1], [1, 1]]), Shape([[1, 1, 1, 1], [1, 1, 1]])]
    # board size
    size = (8, 8)
    # @staticmethod
    # def clone_list(l):
    #     new_list = [item for item in l]
    #     return new_list

    @staticmethod
    def __is_solved(shape: Shape):
        # write the check solved logic
        return False

    def __is_error(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        print(
            f"Inside __try_combinations shape {shape} , list : {remaining_shapes_list}"
        )
        if self.__is_error(shape):
            return False
        if not remaining_shapes_list:
            if self.__is_solved(shape):
                return shape
        self.__try_combinations(remaining_shapes_list[0], remaining_shapes_list[1:])

    def solve(self):
        solved_shape = self.__try_combinations(self.shapes[0], self.shapes[1:])
        if solved_shape:
            print(solved_shape)
        else:
            print("Not solved")


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
