# -*- coding: utf-8 -*-
import Image as _Image
import utils


class SVGObject(object):

    # PIL Image or pyit.image.ImageObject instace
    _image_source = None
    # Dictionary used to keep the tiles path/color structure
    _SVG_path_dict = None

    def __init__(self, image_inst):
        """
        Contructor
        :param image_inst: PIL Image or pyit.image.ImageObject instance.
        """
        self._image_source = image_inst

    @classmethod
    def open_image(cls, image_path):
        """
        Creates and returns a SVGObject instance based on
        an image file.
        :param image_path: path to the image file.
        """
        return SVGObject(_Image.open(image_path))

    def _generate_SVG_source(self, x1=0, y1=0, x2=None, y2=None):
        # Generates SVG source by using tile paths.
        if not isinstance(self._SVG_path_dict, dict):
            self._SVG_path_dict = {}
        size = self._image_source.size
        if not x2:
            x2 = size[0]
        if not y2:
            y2 = size[1]
        color = None
        approved_tile = True
        width = x2 - x1
        height = y2 - y1
        for x in range(x1, x2):
            for y in range(y1, y2):
                pixel = self._image_source.getpixel((x, y))
                if not color:
                    color = pixel
                if color != pixel:
                    approved_tile = False
                    if width > height:
                        self._generate_SVG_source(x1, y1, x1 + width / 2, y2)
                        self._generate_SVG_source(x1 + width / 2, y1, x2, y2)
                    else:
                        self._generate_SVG_source(x1, y1, x2, y1 + height / 2)
                        self._generate_SVG_source(x1, y1 + height / 2, x2, y2)
                    break
            if not approved_tile:
                break
        if approved_tile:
            if not color in self._SVG_path_dict:
                self._SVG_path_dict[color] = ''
            self._SVG_path_dict[color] += ' M%(x1)d %(y1)d H%(x2)d '\
            'V%(y2)d H%(x1)d Z' % {
                'x1': x1,
                'x2': x2,
                'y1': y1,
                'y2': y2
            }

    def get_SVG_source(self):
        """
        Returns the svg source that represents the current image.
        """
        source = '<?xml version="1.0" standalone="no"?>'\
        '<svg width="%(width)d" height="%(height)d" '\
        'version="1.1" xmlns="http://www.w3.org/2000/svg">'\
        '%(path_sources)s'\
        '</svg>'
        path_sources = ''
        width, height = self._image_source.size
        self._generate_SVG_source()
        for color, path in self._SVG_path_dict.iteritems():
            path = path.strip()
            path_sources += '<path d="%(path)s" fill="%(color)s"/>' % {
                'color': utils.get_web_color(color),
                'path': path,
            }
        return source % {
            'width': width,
            'height': height,
            'path_sources': path_sources,
        }

    def save(self, file_path):
        """
        Creates and writes a file with the result from the function
        `get_SVG_source`.
        :param file_path: path to the file.
        """
        if not file_path.endswith('.svg'):
            file_path += '.svg'
        svg_file = open(file_path, 'w')
        svg_file.write(self.get_SVG_source())
        svg_file.close()
