import os
import unittest
import Image  # PIL
from tests import settings
from pyit.image import ImageObject

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


class TestImageObject(unittest.TestCase):

    def _get_test_image_paths(self):
        return ["%s/%s" % (settings.FIXTURE_FOLDER_PATH, test_file)
            for test_file in os.listdir(settings.FIXTURE_FOLDER_PATH)]

    def _get_default_image_object(self):
        return ImageObject(Image.open(
            settings.DEFAULT_IMAGE_PATH
        ))

    def test_getattr(self):
        # gettting a PIL Image instance attribute
        image_object = self._get_default_image_object()
        try:
            image_object.getpixel((1, 1))
        except AttributeError:
            self.fail('Attribute error: getpixel')

    def test_open(self):
        self.assertIsInstance(ImageObject.open(
            settings.DEFAULT_IMAGE_PATH), ImageObject)

    def test_get_pil_image_obj(self):
        image_object = self._get_default_image_object()
        pil_image_object = image_object.get_pil_image_object()
        self.assertIsNotNone(pil_image_object)

    def test_resize_and_crop(self):
        for file_path in self._get_test_image_paths():
            image_object = ImageObject(Image.open(file_path))
            for width, height in TEST_SIZES:
                image_object.resize_and_crop(width, height)
                new_width, new_height = image_object.size
                self.assertEqual(width, new_width)
                self.assertEqual(height, new_height)

    def test_grayscale(self):
        image_object = self._get_default_image_object()
        image_object.grayscale()
        for pixel in image_object.getdata():
            self.assertTrue(pixel <= 255)

    def test_black_and_white(self):
        image_object = self._get_default_image_object()
        image_object.black_and_white()
        for pixel in image_object.getdata():
            self.assertTrue(pixel == 0 or pixel == 255)


if __name__ == '__main__':
    unittest.main()
