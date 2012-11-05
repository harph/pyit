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
        self.assertRaises(ValueError,
            self._get_default_image_object().resize_and_crop,
            -100, 300)
        self.assertRaises(ValueError,
            self._get_default_image_object().resize_and_crop,
            100, -300)
        self.assertRaises(ValueError,
            self._get_default_image_object().resize_and_crop,
            '100', 300)
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

    def test_replace_color(self):
        default_image = self._get_default_image_object()
        old_color = (255, 255, 255)
        new_color = (255, 0, 0)
        # Without tolerance
        image_object_with_no_tol = self._get_default_image_object()
        image_object_with_no_tol.replace_color(old_color, new_color)
        # With tolerance
        image_object_with_tol = self._get_default_image_object()
        image_object_with_tol.replace_color(old_color, new_color, 1)
        w, h = default_image.size
        for y in range(0, h):
            for x in range(0, w):
                no_tol_pixel = image_object_with_no_tol.getpixel((x, y))
                tol_pixel = image_object_with_tol.getpixel((x, y))
                default_pixel = default_image.getpixel((x, y))
                # Validating the the old color is not on the image anymore.
                self.assertNotEqual(no_tol_pixel, old_color)
                self.assertNotEqual(tol_pixel, old_color)
                # Validating old color replacement by the new one
                if default_pixel == old_color:
                    self.assertEqual(no_tol_pixel, new_color)
                # Because the tolerance of the second replacement is 1, all the
                # colors should be 'new_color'. This validate the previous
                # condition on the 'image_object_with_tol' and it also verifies
                # the tolerance assuming that all the colors should be the
                # same.
                self.assertEqual(tol_pixel, new_color)


if __name__ == '__main__':
    unittest.main()
