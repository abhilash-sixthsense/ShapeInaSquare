import unittest
from main import Shape


class TestShape(unittest.TestCase):
    def are_matrices_equal(self, matrix1, matrix2):
        # Check if the dimensions of the matrices are the same
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            return False

        # Iterate through the elements and compare them
        for i, row1 in enumerate(matrix1):
            for j, element1 in enumerate(row1):
                if element1 != matrix2[i][j]:
                    print("\n")
                    print("Below matrixes are not equal")
                    Shape(matrix1).print()
                    Shape(matrix2).print()
                    return False

        return True

    def test_convert_to_matrix(self):
        arr = [[1, 1, 1, 1], [1, 1]]
        s: Shape = Shape(arr)
        expected_arr = [[1, 1, 1, 1], [1, 1, 0, 0]]
        self.assertTrue(
            self.are_matrices_equal(s.arr, expected_arr),
            "Error in convert matrix function",
        )
        s = Shape(
            arr=[
                [
                    1,
                ],
                [
                    1,
                ],
                [
                    1,
                ],
                [1, 1, 1, 1],
            ],
            empty_char=0,
        )
        # print(s.arr)
        self.assertTrue(
            self.are_matrices_equal(
                s.arr,
                [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
            ),
            "Error in convert matrix function",
        )

    def test_clone_arr(self):
        s = Shape([[1, 2, 3]])
        cln_arr = s.clone_arr()
        self.assertFalse(s == cln_arr)
        self.assertTrue(self.are_matrices_equal(s.arr, cln_arr))

    def test_flips(self):
        s = Shape([[1], [1], [1, 1, 1]])
        shapes = s.flips()
        self.assertEqual(len(shapes), 4)
        self.assertTrue(
            self.are_matrices_equal(shapes[0].arr, [[1, 0, 0], [1, 0, 0], [1, 1, 1]])
        )
        self.assertTrue(
            self.are_matrices_equal(shapes[1].arr, [[0, 0, 1], [0, 0, 1], [1, 1, 1]])
        )
        self.assertTrue(
            self.are_matrices_equal(shapes[2].arr, [[1, 1, 1], [1, 0, 0], [1, 0, 0]])
        )
        self.assertTrue(
            self.are_matrices_equal(shapes[3].arr, [[1, 1, 1], [0, 0, 1], [0, 0, 1]])
        )
        # s.print()

    def test_rotations(self):
        s = Shape([[1], [1], [1, 1, 1]])
        shapes = s.rotations()
        self.assertEqual(len(shapes), 4)

        self.assertTrue(
            self.are_matrices_equal(shapes[0].arr, [[1, 0, 0], [1, 0, 0], [1, 1, 1]])
        )
        # shapes[1].print()
        self.assertTrue(
            self.are_matrices_equal(shapes[1].arr, [[1, 1, 1], [1, 0, 0], [1, 0, 0]])
        )

        self.assertTrue(
            self.are_matrices_equal(shapes[2].arr, [[1, 1, 1], [0, 0, 1], [0, 0, 1]])
        )

        self.assertTrue(
            self.are_matrices_equal(shapes[3].arr, [[0, 0, 1], [0, 0, 1], [1, 1, 1]])
        )

    def test_add_below(self):
        s = Shape([[1], [1], [1, 1, 1]])
        s1 = Shape([[1], [1], [1, 1, 1]])
        # print(s.add_below(s1))
        for shape in s.add_below(s1):
            shape.print()

    # def test_upper(self):
    #     self.assertEqual("foo".upper(), "FOO")

    # def test_isupper(self):
    #     self.assertTrue("FOO".isupper())
    #     self.assertFalse("Foo".isupper())

    # def test_split(self):
    #     s = "hello world"
    #     self.assertEqual(s.split(), ["hello", "world"])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == "__main__":
    unittest.main()
