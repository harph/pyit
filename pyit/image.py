# -*- conding: utf-8 -*-
import math
import Image as _Image  # PIL
from pyit import utils


class ImageObject(object):

    # PIL Image wrapper
    # It uses a delegating wrapper becase according to  Fredrik Lundh
    # the PIL Image class "isn't designed to be subclassed by application code.
    # If you want custom behaviour, use a delegating wrapper."
    _image_wrapper = None

    def __init__(self, image_inst):
        """
        :param image_inst: PIL Image class instance.
        :type image_inst: Image.
        """
        self._image_wrapper = image_inst

    def __getattr__(self, attribute):
        if attribute in self.__dict__:
            return getattr(self, attribute)
        return getattr(self._image_wrapper, attribute)

    @classmethod
    def open(cls, image_path):
        """
        Creates and returns an ImageObject instance based on the image path.

        :param image_path: path to the image file.
        :type image_path: str.
        :returns: ImageObject -- instance based on the image path.
        """
        return cls(_Image.open(image_path))

    def get_pil_image_object(self):
        """
        :returns: Image -- PIL image instance that is being used at this
        instace.
        """
        return self._image_wrapper

    def resize_and_crop(self, width, height):
        """
        Resizes and crops (if it's necessary) the image source
        from the center.

        :param width: Requested width.
        :type width: int.
        :param height: Requested height.
        :type height: int.
        """
        for size in (width, height):
            if not isinstance(size, int) or size <= 0:
                raise ValueError('Width and height must be positive integers')
        actual_width, actual_height = map(float, self.size)
        new_width, new_height = 0, 0
        crop_x, crop_y = 0, 0
        width_ratio = actual_width / width
        height_ratio = actual_height / height
        if width_ratio < height_ratio:
            new_width = width
            new_height = math.ceil(actual_height * new_width / actual_width)
            crop_y = int(math.fabs((new_height / 2) - (height / 2)))
        else:
            new_height = height
            new_width = math.ceil(actual_width * new_height / actual_height)
            crop_x = int(math.fabs((new_width / 2) - (width / 2)))
        new_width = int(new_width)
        new_height = int(new_height)
        self.resize((new_width, new_height))
        cropped_image = self.crop(
            (crop_x, crop_y, crop_x + width,  crop_y + height)
        )
        self._image_wrapper = cropped_image

    def grayscale(self):
        """
        Transforms all the pixels of the image into a color range
        between 0 and 255.
        """
        self._image_wrapper = self.convert('L')

    def black_and_white(self):
        """
        Transforms all the pixels of the image into black or white.
        """
        self._image_wrapper = self.convert('1')

    def replace_color(self, old_color, new_color, tolerance=0):
        """
        Replace all the ocurrences of the `old_color` by the new_one.
        If the optional argument `tolerance` is given it will replace
        colors where the similarity based on rgb dimension distance
        matchs that value.

        :param old_color: Color (rgb, rbga tuple or hex code) to be replaced.
        :type old_color: str or tuple.
        :param new_color: Color (rgb, rbga tuple or hex code) that is going
        to replace the old color.
        :type new_color: str or tuple.
        :param tolerance: Optional value (between 0 and 1) that indicates
        the the similarity between color that you want to replace. This can
        be undertood as a percentage of similarity alowed between the
        `old_color` and the rest in the image.
        :type tolerance: float.
        """
        if tolerance < 0 or tolerance > 1:
            raise ValueError(
                'Invalid tolerance value. This value must be between 0 and 1.')
        similitude = 1 - tolerance
        width, height = self.size
        old_color_tuple = utils.get_color_tuple(old_color)
        new_color_tuple = utils.get_color_tuple(new_color)
        for x in range(0, width):
            for y in range(0, height):
                pixel = self.getpixel((x, y))
                similarity = utils.get_color_similarity(
                    old_color_tuple, pixel)
                if similarity >= similitude:
                    self.putpixel((x, y), new_color_tuple)
