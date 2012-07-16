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
    cropped_image = resized_image.crop(
        (crop_x, crop_y, crop_x + width,  crop_y + height)
    )
    return cropped_image

def grayscale(image):
    return image.convert('L')

def black_and_white(image):
    return image.convert('1')


def _tiles_to_svg(image, x1, y1, x2, y2):
    color = None
    svg_code = ''
    approved = True
    width = x2 - x1
    height = y2 - y1
    for x in range(x1, x2):
        for y in range(y1, y2):
            pixel = image.getpixel((x, y))
            if not color:
                color = pixel
            if color != pixel:
                approved = False
                if width > height:
                    svg_code = _tiles_to_svg(image, x1, y1, x1 + width / 2, y2)
                    svg_code += _tiles_to_svg(image, x1 + width / 2, y1, x2, y2)
                    pass
                else:
                    svg_code = _tiles_to_svg(image, x1, y1, x2, y1 + height / 2)
                    svg_code += _tiles_to_svg(image, x1, y1 + height / 2, x2, y2)
                break
        if not approved:
            break
    if approved:
        color_format = 'rgba' if len(color) == 4 else 'rgb'
        svg_code += '<rect x="%(x1)d" y="%(y1)d" '
        svg_code +='width="%(width)d" height="%(height)d" style="fill:%(color_format)s%(color)s;"/>'
        svg_code %= {
            'x1': x1, 
            'y1': y1,
            'width': x2 - x1,
            'height': y2 - y1, 
            'color': str(color),
            'color_format': color_format
        }
    return svg_code

def svg_source(image):
    data = image.getdata()
    width, height = image.size
    tiles_source = _tiles_to_svg(image, 0, 0, width, height)
    source = '''<?xml version="1.0" standalone="no"?>\
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \
    "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\
    <svg width="%(width)d" height="%(height)d"\
         xmlns="http://www.w3.org/2000/svg" version="1.1">\
      <desc>Example line01 - lines expressed in user coordinates</desc>\
      %(tiles_source)s\
    </svg>
    ''' % {'width': width, 'height': height, 'tiles_source': tiles_source} 
    return source