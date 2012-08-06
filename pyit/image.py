# -*- conding: utf-8 -*-
import math
import Image as _Image  # PIL


class ImageObject(object):

    # PIL Image wrapper
    # It uses a delegating wrapper becase according to  Fredrik Lundh
    # the PIL Image class "isn't designed to be subclassed by application code.
    # If you want custom behaviour, use a delegating wrapper."
    _image_wrapper = None

    def __init__(self, image_inst):
        """
        Constructor.
        :param image_inst: PIL Image class instance.
        """
        self._image_wrapper = image_inst

    def __getattr__(self, attribute):
        if attribute in self.__dict__:
            return getattr(self, attribute)
        return getattr(self._image_wrapper, attribute)

    @classmethod
    def open(cls, image_path):
        """
        Class Method.
        Creates and returns an ImageObject instance based on the image path.
        :param image_path: path to the image file.
        """
        return cls(_Image.open(image_path))

    def get_pil_image_object(self):
        """
        Returns the PIL Image instance that is being used at this instace.
        """
        return self._image_wrapper

    def resize_and_crop(self, width, height):
        """
        Resizes and crops (if it's necessary) the image source
        from the center.
        :param width: Requested width.
        :param height: Requested height.
        """
        actual_width, actual_height = map(float, self.size)
        width, height = width, height
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
