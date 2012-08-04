# -*- coding: utf-8 -*-


def get_color_tuple(color):
    """
    Processes a color format and returns a `rgb` or `rgba` tuple.
    :param color: Color in the following formats:
        - rgb: rgb tuple, i.e.: (255, 255, 255)
        - rgba: rgba tuple, i.e.: (255, 255, 255, 0.5)
        - hex color: haxdeximal code format, i.e.: #00FFCC or #0FC
    """
    if isinstance(color, tuple):
        color_len = len(color)
        if color_len == 3 or color_len == 4:
            for color_value in color[:3]:
                if (not isinstance(color_value, int) or
                    color_value < 0 or color_value > 255):
                    raise ValueError('The red, green or blue value '
                        'must be an integer between 0 and 255.')
            alpha = None if color_len == 3 else color[3] * 1.0
            if alpha and isinstance(alpha, float) and alpha < 0 or alpha > 1:
                raise ValueError('The alpha value must be an integer '
                    'between 0 and 1.')
            return color
        else:
            raise ValueError(
                'Invalid len for color tuple. Length must be between 3 o 4.')
    elif isinstance(color, str):
        color = color.replace('#', '')
        color_len = len(color)
        red, green, blue = None, None, None
        if color_len == 6:
            red, green, blue = color[:2], color[2:4], color[4:]
        elif color_len == 3:
            red, green, blue = color
        else:
            raise ValueError('Invalid hexadecimal color format.')
        try:
            return (int(red, 16), int(green, 16), int(blue, 16))
        except ValueError:
            raise ValueError('"%s" is not a valid hexadecimal color format.')


def get_web_color(color):
    """
    Processes a color format and returns a `rgb` or `rgba` tuple.
    :param color: Color in the following formats:
        - rgb: rgb tuple, i.e.: (255, 255, 255)
        - rgba: rgba tuple, i.e.: (255, 255, 255, 0.5)
        - hex color: haxdeximal code format, i.e.: #00ffcc or #0fc
    """
    color_tuple = get_color_tuple(color)
    if len(color_tuple) == 3:
        return '#%02x%02x%02x' % color_tuple
    return 'rgba%s' % str(color_tuple)
