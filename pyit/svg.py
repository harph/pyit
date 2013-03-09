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
        :param image_inst: image instance.
        :type image_inst: Image or pyit.image.ImageObject
        """
        self._image_source = image_inst

    @classmethod
    def open_image(cls, image_path):
        """
        Creates and returns a SVGObject instance based on
        an image file.

        :param image_path: path to the image file.
        :type image_path: str.
        :returns: SVGObject -- instance based on the image path.
        """
        return SVGObject(_Image.open(image_path))

    @property
    def SVG_paths(self):
        if not self._SVG_path_dict:
            self._generate_SVG_paths()
        return self._SVG_path_dict

    def _generate_SVG_paths(self, x1=0, y1=0, x2=None, y2=None):
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
                        self._generate_SVG_paths(x1, y1, x1 + width / 2, y2)
                        self._generate_SVG_paths(x1 + width / 2, y1, x2, y2)
                    else:
                        self._generate_SVG_paths(x1, y1, x2, y1 + height / 2)
                        self._generate_SVG_paths(x1, y1 + height / 2, x2, y2)
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
        Returns the SVG source that represents the current image.
        
        :returns: str -- SVG source.
        """
        source = '<?xml version="1.0" standalone="no"?>'\
        '<svg width="%(width)d" height="%(height)d" '\
        'version="1.1" xmlns="http://www.w3.org/2000/svg">'\
        '%(path_sources)s'\
        '</svg>'
        path_sources = ''
        width, height = self._image_source.size
        for color, path in self.SVG_paths.iteritems():
            if not path:
                continue
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
        new_color_path = ''
        similitude = 1 - tolerance
        old_color_tuple = utils.get_color_tuple(old_color)
        new_color_tuple = utils.get_color_tuple(new_color)
        for color in self.SVG_paths.keys():
            similarity = utils.get_color_similarity(
                old_color_tuple, color)
            if similarity >= similitude:
                new_color_path += self.SVG_paths[color]
                del self.SVG_paths[color]

        if new_color_path:
            if new_color_tuple not in self.SVG_paths:
                self.SVG_paths[new_color_tuple] = ''
            self.SVG_paths[new_color_tuple] += new_color_path

    def save(self, file_path):
        """
        Creates and writes a file with the result from the function
        `get_SVG_source`.
        
        :param file_path: path to the file.
        :type file_path: str.
        """
        if not file_path.endswith('.svg'):
            file_path += '.svg'
        svg_file = open(file_path, 'w')
        svg_file.write(self.get_SVG_source())
        svg_file.close()
