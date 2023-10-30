from typing import List

from shape import Shape


class Board:
    shapes = [Shape([[1, 1, 1, 1], [1, 1]]), Shape([[1, 1, 1, 1], [1, 1, 1]])]
    # board size
    size = (8, 8)
    empty_slot = 0

    solved_shapes = []

    def __add_to_solved_shape(self, shape):
        self.solved_shapes.append(shape.clone())

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

        shapes = [Shape(s) for s in arr]
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

    def is_invalid(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    @staticmethod
    def __horizontal_flip(arr):
        pass

    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        print(f"Inside __try_combinations shape {shape} , list : {remaining_shapes_list}")

        # Just try combinations and no need to procced further
        shape_1 = remaining_shapes_list[0]
        shapes = []
        shapes.extend(shape.add_above(shape_1))
        shapes.extend(shape.add_below(shape_1))
        shapes.extend(shape.add_left(shape_1))
        shapes.extend(shape.add_right(shape_1))
        # TODO consider flips also
        for s in shapes:
            if self.is_solved(s):
                self.__add_to_solved_shape(s)
                print(f"Adding shape to solved shapes {s.__str__()}")
            elif not self.is_invalid(s):
                self.__try_combinations(s, self.shapes[1:])

    def solve(self):
        self.__try_combinations(self.shapes[0], self.shapes[1:])
        if self.solved_shapes:
            print(f"There are {len(self.solved_shapes)} combinations")
        else:
            print("No solved combinations")
