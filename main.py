print('hi')


class Shape:
    arr = []

    def __init__(self, arr):
        self.arr = arr
        print(len(arr))

    def __str__(self) -> str:
        return str(self.arr)


s1 = Shape([[1, 1, 1], [1]])
print(s1)
