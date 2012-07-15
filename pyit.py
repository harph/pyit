import math
import Image

def resize_and_crop(image, width, height):
    image_filename = image.filename
    actual_width, actual_height = image.size
    width, height = float(width), float(height)
    new_width, new_height = 0, 0
    crop_x, crop_y = 0, 0
    width_ratio = actual_width / width
    height_ratio = actual_height / height
    if width_ratio < height_ratio:
        new_width = width
        new_height = math.ceil(actual_height * new_width / actual_width)
        crop_y =  int(math.fabs((new_height / 2) - (height / 2)))
    else:
        new_height = height
        new_width = math.ceil(actual_width * new_height / actual_height)
        crop_x = int(math.fabs((new_width / 2) - (width / 2)))
    new_width = int(new_width)
    new_height = int(new_height)
    resized_image = image.resize((new_width, new_height))
    width, height = int(width), int(height)
    cropped_image = resized_image.crop((crop_x, crop_y, crop_x + width,  crop_y + height))
    return cropped_image

def grayscale(image):
    return image.convert('L')

def black_and_white(image):
    return image.convert('1')
