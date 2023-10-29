from typing import List

from shape import Shape


class Board:
    shapes = [Shape([[1, 1, 1, 1], [1, 1]]), Shape([[1, 1, 1, 1], [1, 1, 1]])]
    # board size
    size = (8, 8)
    empty_slot = 0

    solved_shapes = []

    def __init__(self, shapes, size: tuple[int, int]):
        self.shapes = shapes
        self.size = size
        print(f"Creating board of size {size}")

    @staticmethod
    # Returns a 3*3 solvable shapes
    def create3_3_shape() -> List[Shape]:
        arr = [
            [
                [1, 0],
                [1, 1],
            ],
            [
                [1, 1],
                [0, 1],
            ],
            [
                [1, 1, 1],
            ],
        ]

        shapes = [Shape(s, unique_fill_char=True) for s in arr]
        return shapes

    def is_solved(self, shape: Shape) -> bool:
        # write the check solved logic
        # check the size of the shape is equal to the size of the board
        shape_size = shape.size()
        size_fit = shape_size[0] == self.size[0] and shape_size[1] == self.size[1]
        if not size_fit:
            print(f"Board size {self.size} doesn't match shape size {shape_size}")
            return False

        print(f"Board size {self.size} match shape size {shape_size}")

        if shape.empty_slot_exits():
            print("There are empty slots in the shape")
            return False
        print("There are no empty slots in the shape")
        return True

    def __is_error(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    @staticmethod
    def __horizontal_flip(arr):
        pass

    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        print(f"Inside __try_combinations shape {shape} , list : {remaining_shapes_list}")

        if len(remaining_shapes_list) == 1:
            # Just try combinations and no need to procced further
            shape_1 = remaining_shapes_list[0]

            shape.add_above(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_below(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_left(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_right(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()
        else:
            shape_1 = remaining_shapes_list[0]

            shape.add_above(shape_1)
            if not self.__is_error(shape):
                self.__try_combinations(shape, remaining_shapes_list[1:])

            shape.revert()

            shape.add_below(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_left(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

            shape.add_right(shape_1)
            if self.is_solved(shape):
                self.solved_shapes.append(shape.clone_arr())
            shape.revert()

    def solve(self):
        self.__try_combinations(self.shapes[0], self.shapes[1:])
        if self.solved_shapes:
            print(f"There are {len(self.solved_shapes)} combinations")
        else:
            print("No solved combinations")
