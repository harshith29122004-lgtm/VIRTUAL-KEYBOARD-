import unittest

from main import KEY_ROWS, build_key_rectangles, point_in_rect


class KeyboardGeometryTests(unittest.TestCase):
    def test_expected_keys_are_present(self):
        rectangles = build_key_rectangles(1280, 720)
        labels = [key for key, _ in rectangles]

        self.assertEqual(len(labels), sum(len(row) for row in KEY_ROWS))
        self.assertIn("SPACE", labels)
        self.assertIn("BACK", labels)
        self.assertEqual(len(labels), len(set(labels)))

    def test_rectangles_stay_inside_frame_for_common_sizes(self):
        for width, height in [(640, 480), (1280, 720), (1920, 1080)]:
            with self.subTest(width=width, height=height):
                rectangles = build_key_rectangles(width, height)
                for key, (x1, y1, x2, y2) in rectangles:
                    self.assertGreaterEqual(x1, 0, key)
                    self.assertGreaterEqual(y1, 0, key)
                    self.assertGreater(x2, x1, key)
                    self.assertGreater(y2, y1, key)
                    self.assertLessEqual(x2, width - 35, key)
                    self.assertLessEqual(y2, height, key)

    def test_point_inside_and_outside_rectangle(self):
        rectangle = (10, 20, 50, 60)

        self.assertTrue(point_in_rect((10, 20), rectangle))
        self.assertTrue(point_in_rect((30, 40), rectangle))
        self.assertTrue(point_in_rect((50, 60), rectangle))
        self.assertFalse(point_in_rect((9, 40), rectangle))
        self.assertFalse(point_in_rect((51, 40), rectangle))
        self.assertFalse(point_in_rect((30, 61), rectangle))


if __name__ == "__main__":
    unittest.main()
