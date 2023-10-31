from shape import Shape


class Board:
    shapes: list[Shape] = []
    # board size
    size: tuple[int, int] = tuple()
    empty_slot = 0

    solved_shapes: list[Shape] = []

    tried_combination_count = 0

    # key will be the number of zeros and value will be the arr
    tried_combinations = dict()

    def check_tried_combination(self, s: Shape):
        a = s.arr
        zero_count = 0
        for row in a:
            zero_count += len(row)
        if zero_count in self.tried_combinations:
            combo = self.tried_combinations[zero_count]
        else:
            combo = []
            self.tried_combinations[zero_count] = combo

        if s.arr in combo:
            return True
        else:
            combo.append(s.arr)
            return False

    def __add_to_solved_shape(self, shape):
        for rs in shape.rotations():
            for ss in self.solved_shapes:
                if rs == ss:
                    # print("Skipping duplicate solved shape")
                    return
        print("Adding shape to solved shapes ")
        shape.print()
        self.solved_shapes.append(shape)
        shape.dump_to_file()

    def __init__(self, shapes, size: tuple[int, int]):
        self.shapes = shapes
        self.size = size
        print(f"Creating board of size {size}")
        print("-------------- Shapes --------------")
        for s in shapes:
            s.print()
        print(f"-------------- Total {len(self.shapes)} Shapes --------------")

    @staticmethod
    # Returns a 3*3 solvable shapes
    def create3_3_board() -> "Board":
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
        board = Board(shapes, (3, 3))
        return board

    @staticmethod
    def create3_3_board_1() -> "Board":
        arr = [
            [
                [1, 0, 1],
                [1, 1, 1],
            ],
            [
                [1, 1, 1],
                [0, 1, 0],
            ],
        ]

        shapes = [Shape(s) for s in arr]
        board = Board(shapes, (3, 3))
        return board

    def is_solved(self, shape: Shape) -> bool:
        # write the check solved logic
        # check the size of the shape is equal to the size of the board
        shape_size = shape.size()
        size_fit = shape_size[0] == self.size[0] and shape_size[1] == self.size[1]
        if not size_fit:
            # print(f"Board size {self.size} doesn't match shape size {shape_size}")
            return False

        # print(f"Board size {self.size} match shape size {shape_size}")

        if shape.empty_slot_exits():
            # print("There are empty slots in the shape")
            return False
        # print("There are no empty slots in the shape")
        return True

    def is_invalid(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    @staticmethod
    def __horizontal_flip(arr):
        pass

    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        # print(f"Inside __try_combinations shape , list size: {len(remaining_shapes_list)}")
        # shape.print()

        # Just try combinations and no need to proceed further
        shape_1 = remaining_shapes_list[0]
        shapes = []
        # sr = shape_1.rotations()
        sr = [shape_1]
        for s in sr:
            shapes.extend(shape.add_above(s))
            shapes.extend(shape.add_below(s))
            shapes.extend(shape.add_left(s))
            shapes.extend(shape.add_right(s))
        # TODO consider flips also
        for s in shapes:
            self.tried_combination_count += 1
            if self.tried_combination_count % 50000 == 0:
                # for k, v in self.tried_combinations.items():
                #     print(k, len(v))
                tried_combinations_length = sum(len(row) for row in self.tried_combinations.values())
                print(
                    f"Combinations: {self.tried_combination_count:<8} Total Shapes: {Shape.instance_count:<8} Active "
                    f"Shapes {len(Shape.active_instance_ids):<8} "
                    f"Already Tried Combinations {tried_combinations_length:<10}"
                    f" solved: {len(self.solved_shapes)}"
                )

            if self.is_solved(s):
                self.__add_to_solved_shape(s)
            if not self.is_invalid(s) and len(remaining_shapes_list) > 1:
                if self.check_tried_combination(s):
                    # print("Already tried combination")
                    continue
                self.__try_combinations(s, remaining_shapes_list[1:])
            else:
                # print("Can't proceed further with this shape , returning")
                # s.print()
                # input("Press Enter to continue...")
                pass

    def solve(self):
        print("Solver running .....")
        self.__try_combinations(self.shapes[0], self.shapes[1:])
        if self.solved_shapes:
            print(f"There are {len(self.solved_shapes)} solved combinations")
            for index, s in enumerate(self.solved_shapes):
                print(index + 1, "----------")
                s.print()
        else:
            print("No solved combinations")
