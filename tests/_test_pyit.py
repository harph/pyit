import os
import Image
import unittest
import random
import pyit

TEST_FOLDER = 'fixtures'
TEST_SIZES = (
    (100, 100),  # small square
    (100, 200),  # small horizontal rectangle
    (200, 100),  # small vertical rectangle
    (500, 500),  # medium square
    (500, 800),  # medium horizontal rectangle
    (800, 500),  # medium vertical rectangle
    (2000, 2000),  # huge square
    (2000, 4000),  # huge horizontal rectangle
    (4000, 2000),  # huge vertical rectangle
)


class TestPyIT(unittest.TestCase):

    def setUp(self):
        self.file_names = [
            f_name for f_name in os.listdir(TEST_FOLDER)
            if f_name != '.DS_Store' and not os.path.isdir(
                os.path.join(TEST_FOLDER, f_name))
        ]

    def test_resize_and_crop(self):
        for file_name in self.file_names:
            file_path = os.path.join(TEST_FOLDER, file_name)
            image = Image.open(file_path)
            for width, height in TEST_SIZES:
                new_image = pyit.resize_and_crop(image, width, height)
                new_width, new_height = new_image.size
                self.assertEqual(width, new_width)
                self.assertEqual(height, new_height)

    def _get_random_image(self):
        file_name = random.choice(self.file_names)
        file_path = os.path.join(TEST_FOLDER, file_name)
        image = Image.open(file_path)
        return image

    def test_black_and_white(self):
        image = self._get_random_image()
        new_image = pyit.black_and_white(image)
        for pixel in new_image.getdata():
            self.assertTrue(pixel == 0 or pixel == 255)

    def test_grayscale(self):
        file_name = random.choice(self.file_names)
        file_path = os.path.join(TEST_FOLDER, file_name)
        image = Image.open(file_path)
        new_image = pyit.grayscale(image)
        for pixel in new_image.getdata():
            self.assertTrue(pixel <= 255)

    def test_svg(self):
        #TODO: Improve this test. Find a way to validate the svg source
        image = self._get_random_image()
        svg_source = pyit.svg_source(image)
        svg_file = open('foo.svg', 'w')
        svg_file.write(svg_source)
        svg_file.close()

if __name__ == '__main__':
    unittest.main()
