import unittest

from board import Board
from shape import Shape


class TestBoard(unittest.TestCase):
    def test_create3_3_shape(self):
        shapes = Board.create3_3_board().shapes
        print(shapes)
        self.assertEqual(3, len(shapes), "3 shapes must be created")

    def test_is_solved(self):
        board = Board.create3_3_board()

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

    def test_solve(self):
        board = Board.create3_3_board()
        board.solve()

    if __name__ == "__main__":
        unittest.main()
