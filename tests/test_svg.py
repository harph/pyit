import os
import unittest
import Image  # PIL
from tests import settings
from pyit.svg import SVGObject


class TestSVGObject(unittest.TestCase):

    def _get_default_svg_object(self):
        return SVGObject(Image.open(
            settings.DEFAULT_IMAGE_PATH
        ))

    def test_open_image(self):
        self.assertIsInstance(
            SVGObject.open_image(settings.DEFAULT_IMAGE_PATH),
            SVGObject)

    def test_get_SVG_source(self):
        svg_object = self._get_default_svg_object()
        svg_source = svg_object.get_SVG_source()
        self.assertIsNotNone(svg_source)
        # This needs a better test.
        # Find a way to validate the SVG source.


    def test_replace_color(self):
        svg_object = self._get_default_svg_object()
        old_color = (255, 255, 255)
        new_color = (255, 0, 0)
        svg_object.replace_color(old_color, new_color, tolerance=0.2)
        colors = svg_object.SVG_paths.keys()
        self.assertTrue(old_color not in colors)
        self.assertTrue(new_color in colors)

    def test_save(self):
        svg_test_path = 'unittest_svg.svg'
        svg_object = self._get_default_svg_object()
        svg_object.save(svg_test_path)
        self.assertTrue(os.path.isfile(svg_test_path))
        svg_file = open(svg_test_path, 'r')
        self.assertTrue(svg_file.read())
        svg_file.close()
        # This needs a better test.
        # Find a way to validate content of the
        # SVG file.
        os.remove(svg_test_path)


if __name__ == '__main__':
    unittest.main()
