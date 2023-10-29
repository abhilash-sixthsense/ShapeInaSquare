import unittest

from board import Board
from shape import Shape


class TestBoard(unittest.TestCase):
    def test_create3_3_shape(self):
        shapes = Board.create3_3_shape()
        print(shapes)
        self.assertEqual(3, len(shapes), "3 shapes must be created")

    def test_is_solved(self):
        shapes = Board.create3_3_shape()
        board = Board(shapes=shapes, size=(3, 3))
        for shape in shapes:
            # shape.print()
            # print(shape.size())
            self.assertFalse(board.is_solved(shape), "Board shouldn't be solved with the given shape")
        shape = Shape(
            [
                [1, 1, 1],
                [1, 1, 0],
                [1, 1, 1],
            ]
        )
        self.assertFalse(board.is_solved(shape), msg="Board shouldn't be solved with the given shape")
        shape = Shape(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
            ]
        )
        self.assertFalse(board.is_solved(shape), msg="Board shouldn't be solved with the given shape")
        shape = Shape(
            [
                [1, 1, 1],
                [0, 1, 1],
                [1, 1, 1],
            ]
        )
        self.assertFalse(board.is_solved(shape), msg="Board shouldn't be solved with the given shape")
        self.assertFalse(board.is_solved(shape), msg="Board shouldn't be solved with the given shape")
        shape = Shape(
            [
                [1, 1],
                [0, 1],
            ]
        )
        self.assertFalse(board.is_solved(shape), msg="Board shouldn't be solved with the given shape")
        shape = Shape(
            [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
            ]
        )
        self.assertTrue(board.is_solved(shape), msg="Board should be solved with the given shape")

    if __name__ == "__main__":
        unittest.main()
