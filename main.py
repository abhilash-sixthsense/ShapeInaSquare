print("hi")


class Shape:
    fill_char = "1"
    empty_char = "0"
    history = []
    arr = []

    def __init__(self, arr):
        def convert_to_matrix():
            max_cols = 0
            for row in arr:
                if len(row) > max_cols:
                    max_cols = len(row)

            print(f"Matrix size is {len(arr)},{max_cols}")

            for row in arr:
                for _ in range(0, max_cols - len(row)):
                    row.append(self.empty_char)
            self.arr = arr

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

    @staticmethod
    def add_history(f):
        def decorator(self):
            self.history.append(self.arr)
            return f(self)

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
        pass


s1 = Shape([[1, 1, 1, 1], [1, 1]])
print(s1)
s1.rotate_right()
print(s1)

s1.rotate_left()
print(s1)
s1.revert()
print(s1)
s1.print()
