import sys
import os
import unittest
from pyit import utils


class TestUtils(unittest.TestCase):

    def test_get_color_tuple(self):
        rgb = (255, 255, 255)
        rgba = (255, 255, 255, 0.5)
        hex_code = '#FFFFFF'
        # rgb format
        self.assertEqual(utils.get_color_tuple(rgb), rgb)
        # rgba format
        self.assertEqual(utils.get_color_tuple(rgba), rgba)
        # hexadecimal format
        self.assertEqual(utils.get_color_tuple(hex_code), rgb)

        # tuple length exception
        self.assertRaises(ValueError, utils.get_color_tuple, rgb[:2])
        self.assertRaises(ValueError, utils.get_color_tuple, rgb[:2] * 3)

        # tuple color value range exception
        self.assertRaises(ValueError, utils.get_color_tuple, (2.5, 255, 255))

        # tuple alpha value range exception
        self.assertRaises(ValueError,
            utils.get_color_tuple, (255, 255, 255, 10))

        # hexadecimal code length exception
        self.assertRaises(ValueError, utils.get_color_tuple, hex_code[:2])
        self.assertRaises(ValueError, utils.get_color_tuple, hex_code * 2)

        # invalid hexadecimal color format
        self.assertRaises(ValueError, utils.get_color_tuple, '#$%^&*<')


if __name__ == '__main__':
    unittest.main()
