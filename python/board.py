import os
import sys
from datetime import datetime

from decorators import measure_time, print_measure_time
from shape import Shape
from utils import is_stop_flag_on, get_file_size_in_gb


class Board:
    shapes: list[Shape] = []
    # board size
    size: tuple[int, int] = tuple()
    empty_slot = 0

    solved_shapes: list[Shape] = []

    tried_combination_count = 0

    # key will be the number of zeros and value will be the arr
    tried_combinations = set()
    tried_combination_hit_count = 0
    tried_combinations_bk_up_file = "tried_combination_machine_generated.txt"
    start_time = datetime.now()

    @measure_time
    def check_tried_combination(self, s: Shape):
        return False
        # t = tuple(tuple(inner_list) for inner_list in s.arr)
        # if t in self.tried_combinations:
        #     return True
        # else:
        #     self.tried_combinations.add(t)

    @measure_time
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

    def __save_state(self):
        def __save_tried_combinations():
            print(f"Saving Tried combinations {len(self.tried_combinations)} combinations")
            print(f"Tried combinations count {self.tried_combination_count}")
            with open("tried_combination_count_machine_generated.txt", "a") as f:
                f.write(str(self.tried_combination_count) + "\n")
            # Create a set with tuples of tuples
            my_set = self.tried_combinations

            # Convert the set to a list (if needed)
            my_list = list(my_set)

            # Define the file name

            tmp_file_name = "tmp_" + self.tried_combinations_bk_up_file
            # Open the file in write mode
            with open(tmp_file_name, "w") as file:
                for item in my_list:
                    for sub_tuple in item:
                        file.write(str(sub_tuple) + "\n")
                    file.write("\n")  # Add a newline between each tuple of tuples

            print("Saved Tried combinations")
            if os.path.exists(self.tried_combinations_bk_up_file):
                print("Existing back up found")
                size_existing = get_file_size_in_gb(self.tried_combinations_bk_up_file)
                size_new = get_file_size_in_gb(tmp_file_name)
                if size_existing < size_new:
                    # replace old with new
                    print("Replacing old back up with new")
                    os.remove(self.tried_combinations_bk_up_file)
                    os.rename(tmp_file_name, self.tried_combinations_bk_up_file)
                    print(f"Replaced old backup with new one , {size_new} GB")
                else:
                    print("Old back up is bigger than new, so skipping backup , removing new file ")
                    os.remove(tmp_file_name)
            else:
                os.rename(tmp_file_name, self.tried_combinations_bk_up_file)

        __save_tried_combinations()

    def __load_state(self):
        def __load_tried_combinations():
            # Initialize an empty set
            loaded_set = set()

            # Open the file in read mode
            if os.path.exists(self.tried_combinations_bk_up_file):
                # Initialize an empty set
                loaded_set = set()
                file_size_gb = get_file_size_in_gb(self.tried_combinations_bk_up_file)
                print(f"Loading the already calculated combinations ,file size {file_size_gb} GB")
                # Open the file in read mode
                with open(self.tried_combinations_bk_up_file, "r") as file:
                    current_tuple = set()
                    lines = file.readlines()
                    for line in lines:
                        line = line.strip()  # Remove leading/trailing whitespace and newline characters
                        if line:
                            org_line = line
                            line = line.replace("(", "").replace(")", "")
                            try:
                                current_tuple.add(tuple(map(int, line.split(","))))
                            except Exception as e:
                                print(line)
                                print(e)
                        else:
                            if current_tuple:
                                loaded_set.add(tuple(current_tuple))
                                current_tuple = set()

                # Print the loaded set
                print("Loaded tried combinations")
                # print(loaded_set)
            else:
                print(f"Cannot load tried combinations, file {self.tried_combinations_bk_up_file} doesn't exist")
            # Print the loaded set

            self.tried_combinations = loaded_set

        __load_tried_combinations()

    def __print_board_summary(self):
        print("-------------- Shapes --------------")
        for s in self.shapes:
            s.print()
        print(f"-------------- Total {len(self.shapes)} Shapes --------------")

    def __init__(self, shapes, size: tuple[int, int]):
        self.shapes = shapes
        self.size = size
        print(f"Creating board of size {size}")
        # self.__print_board_summary()
        self.__load_state()

    @staticmethod
    # Returns a 3*3 solvable shapes
    @measure_time
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
    @measure_time
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

    @measure_time
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

    @measure_time
    def is_invalid(self, shape: Shape):
        shape_size = shape.size()
        return shape_size[0] > self.size[0] or shape_size[1] > self.size[1]

    @staticmethod
    @measure_time
    def __horizontal_flip(arr):
        pass

    def __print_progress_info(self):
        # for k, v in self.tried_combinations.items():
        #     print(k, len(v))
        tried_combinations_length = len(self.tried_combinations)
        print(
            f"Combinations: {self.tried_combination_count:<15,} "
            # f"Already Tried Combinations {tried_combinations_length:<10,}"
            # f"Hit tried Combinations count {self.tried_combination_hit_count:<10,}"
            f" solved: {len(self.solved_shapes)}"
        )
        print_measure_time()
        elapsed_time = datetime.now() - self.start_time
        hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Running for {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
        if is_stop_flag_on():
            self.__save_state()
            sys.exit()
        print("===" * 40, "\n")

    @measure_time
    def __try_combinations(self, shape: Shape, remaining_shapes_list):
        # print(f"Inside __try_combinations shape , list size: {len(remaining_shapes_list)}")
        # shape.print()

        # Just try combinations and no need to proceed further
        shape_1 = remaining_shapes_list[0]
        shapes = []
        sr = shape_1.rotations()
        for s in sr:
            shapes.extend(shape.add_above(s))
            shapes.extend(shape.add_below(s))
            shapes.extend(shape.add_left(s))
            shapes.extend(shape.add_right(s))
        # TODO consider flips also
        for s in shapes:
            self.tried_combination_count += 1
            if self.tried_combination_count % 100000 == 0:
                self.__print_progress_info()

            if self.check_tried_combination(s):
                # print("Already tried combination")
                self.tried_combination_hit_count += 1
                continue
            if self.is_solved(s):
                self.__add_to_solved_shape(s)
            if not self.is_invalid(s) and len(remaining_shapes_list) > 1:
                self.__try_combinations(s, remaining_shapes_list[1:])
            else:
                # print("Can't proceed further with this shape , returning")
                # s.print()
                # input("Press Enter to continue...")
                pass

    @measure_time
    def solve(self):
        print("Solver running .....")
        try:
            self.__try_combinations(self.shapes[0], self.shapes[1:])
        except KeyboardInterrupt:
            print("\nForced stop detected. Exiting gracefully.")
            self.__save_state()
        if self.solved_shapes:
            print(f"There are {len(self.solved_shapes)} solved combinations")
            for index, s in enumerate(self.solved_shapes):
                print(index + 1, "----------")
                s.print()
        else:
            print("No solved combinations")
