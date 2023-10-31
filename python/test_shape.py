import unittest

from shape import Shape


def are_matrices_equal(matrix1, matrix2):
    # Check if the dimensions of the matrices are the same
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return False

    # Iterate through the elements and compare them
    for i, row1 in enumerate(matrix1):
        for j, element1 in enumerate(row1):
            if element1 != matrix2[i][j] and (
                element1 == 0 or matrix2[i][j] == 0
            ):  # pass even if the values are not matching but non empty character
                print("\n")
                print("Below matrices are not equal")
                Shape(matrix1).print()
                Shape(matrix2).print()
                return False

    return True


class TestShape(unittest.TestCase):
    Shape.unique_fill_char = True

    def test_convert_to_matrix(self):
        arr = [[1, 1, 1, 1], [1, 1]]
        s: Shape = Shape(arr)
        expected_arr = [[1, 1, 1, 1], [1, 1, 0, 0]]
        self.assertTrue(
            are_matrices_equal(s.arr, expected_arr),
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
        )
        # print(s.arr)
        self.assertTrue(
            are_matrices_equal(
                s.arr,
                [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
            ),
            "Error in convert matrix function",
        )

    def test_clone_arr(self):
        s = Shape([[1, 2, 3]])
        cln_arr = s.clone_arr()
        self.assertFalse(s == cln_arr)
        self.assertTrue(are_matrices_equal(s.arr, cln_arr))

    def test_flips(self):
        s = Shape(
            [[1], [1], [1, 1, 1]],
        )
        shapes = s.flips()
        self.assertEqual(len(shapes), 4)
        self.assertTrue(are_matrices_equal(shapes[0].arr, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
        self.assertTrue(are_matrices_equal(shapes[1].arr, [[0, 0, 1], [0, 0, 1], [1, 1, 1]]))
        self.assertTrue(are_matrices_equal(shapes[2].arr, [[1, 1, 1], [1, 0, 0], [1, 0, 0]]))
        self.assertTrue(are_matrices_equal(shapes[3].arr, [[1, 1, 1], [0, 0, 1], [0, 0, 1]]))
        # s.print()

    def test_rotate_left(self):
        s = Shape([[1], [1], [1, 1, 1]])
        s1 = s.rotate_left()
        s.print()
        s1.print()

    def test_rotations(self):
        s = Shape([[1], [1], [1, 1, 1]])
        shapes = s.rotations()
        self.assertEqual(len(shapes), 4)

        self.assertTrue(are_matrices_equal(shapes[0].arr, [[1, 0, 0], [1, 0, 0], [1, 1, 1]]))
        # shapes[1].print()
        self.assertTrue(are_matrices_equal(shapes[1].arr, [[1, 1, 1], [1, 0, 0], [1, 0, 0]]))

        self.assertTrue(are_matrices_equal(shapes[2].arr, [[1, 1, 1], [0, 0, 1], [0, 0, 1]]))

        self.assertTrue(are_matrices_equal(shapes[3].arr, [[0, 0, 1], [0, 0, 1], [1, 1, 1]]))

    def test_merge_add_below(self):
        s1 = Shape([[1], [1], [1, 1, 1]])
        s2 = Shape([[1], [1], [1, 1, 1]])
        # print(s.add_below(s1))
        shapes = Shape.merge_add_below(s1, s2)
        self.assertEqual(0, len(shapes))
        s1 = Shape([[1, 1, 1], [1], [1]])
        s2 = Shape([[1], [0, 1], [0, 1, 1]])
        shapes = Shape.merge_add_below(s1, s2)
        self.assertEqual(0, len(shapes))

        s1 = Shape([[1, 1, 1], [1], [1]])
        s2 = Shape([[0, 1], [0, 1], [0, 1, 1]])
        shapes = Shape.merge_add_below(s1, s2)
        self.assertEqual(2, len(shapes))
        s1.print()
        s2.print()
        # print("Merged results")
        # for s in shapes:
        #     s.print()

        s1 = Shape([[1, 1, 1], [1], [1]])
        s2 = Shape([[0, 1, 1, 1], [0, 1], [0, 1, 1, 1]])
        shapes = Shape.merge_add_below(s1, s2)
        self.assertEqual(2, len(shapes))
        s1.print()
        s2.print()
        # print("Merged results")
        # for s in shapes:
        #     s.print()

    def test_merge_add_below_bugfix(self):
        s1 = Shape(
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1],
            ]
        )
        s1.print()
        s1 = s1.empty_fill(2, True)
        s2 = Shape(
            [
                [0, 0, 1],
                [0, 0, 1],
                [1, 1, 1],
            ]
        )
        s2.print()
        shapes = Shape.merge_add_below(s2, s1)
        # self.assertEqual(2, len(shapes))
        for index, shape in enumerate(shapes):
            print("-" * 10, index)
            shape.print()
            shape.rotate_left().print()

    def test_add_below(self):
        s1 = Shape([[1]])
        s2 = Shape([[1]])
        result = s1.add_below(s2)
        self.assertTrue(1, len(result))
        self.assertTrue(are_matrices_equal([[1], [1]], result[0].clone_arr()))

        s1 = Shape([[1]])
        s2 = Shape([[1, 1]])
        result = s1.add_below(s2)
        self.assertTrue(2, len(result))
        self.assertTrue(
            are_matrices_equal(
                [
                    [1, 0],
                    [1, 1],
                ],
                result[0].clone_arr(),
            )
        )
        self.assertTrue(
            are_matrices_equal(
                [
                    [0, 1],
                    [1, 1],
                ],
                result[1].clone_arr(),
            )
        )

        s2 = Shape([[0, 0, 1], [0, 0, 1], [1, 1, 1]])
        s3 = Shape([[0, 0, 1], [0, 0, 1], [1, 1, 1]])
        for index, shape in enumerate(s2.add_below(s3)):
            print("----" * 10, index)
            shape.print()

    def test_add_above(self):
        s = Shape([[1], [1], [1, 1, 1]])
        s1 = Shape([[1], [1], [1, 1, 1]])
        for shape in s.add_above(s1):
            shape.print()

    def test_add_left(self):
        s1 = Shape([[1]])
        s2 = Shape([[1]])
        result = s1.add_left(s2)
        self.assertTrue(1, len(result))
        result[0].print()

        s1 = Shape([[1]])
        s2 = Shape(
            [
                [1],
                #
                [1],
            ],
        )
        result = s1.add_left(s2)
        self.assertTrue(2, len(result))
        result[0].print()
        result[1].print()

        s = Shape(
            [
                [1],
                [1],
                [1, 1, 1],
            ]
        )
        s.print()
        s1 = Shape(
            [
                [1],
                [1],
                [1, 1, 1],
            ]
        )
        s1.print()
        for index, shape in enumerate(s.add_left(s1)):
            print("-" * 10, index)
            shape.print()

    def test_shape_instances(self):
        print(f"Total number of shape instances are {Shape.instance_count}")

    # def test_upper(self):
    #     self.assertEqual("foo".upper(), "FOO")
    #
    # def test_isupper(self):
    #     self.assertTrue("FOO".isupper())
    #     self.assertFalse("Foo".isupper())
    #
    # def test_split(self):
    #     s = "hello world"
    #     self.assertEqual(s.split(), ["hello", "world"])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_identical_matrices(self):
        a = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]

        b = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]

    def test_dump_to_file(self):
        s = Shape([[1]])
        file_path = s.dump_to_file()
        s1 = Shape.load_from_file(file_path)
        print(type(s1))
        print(Shape.active_instance_ids)
        s1.print()


if __name__ == "__main__":
    unittest.main()
