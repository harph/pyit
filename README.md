PyIT - Python Image Tool
========================

:Version: 0.1
:Status: Development.
:Author: [Harrington Joseph](http://hjoseph.com)

This is a simple library that helps you to manipulate images (crop, resize, convert - black and white / grayscale / svg). The basic idea behind this project it to provide a easy way to execute common operations over images that are required very often.

# Requirements

+ Python 2.7 (It possibly works in lower versions - Not tested)
+ PIL (Python Image Library).

# How to use it.

It's very simple. Currently the library just has the following main functions:

+ *black_and_white*
+ *grayscale*
+ *resize_and_crop*
+ *svg_source*

So, how to use it? 

	import pyit
	import Image # this is part of the PIL

	image = Image.open('foo.jpg')

	# Black and white
	# Getting a black and white image from the original one
	new_image = pyit.black_and_white(image)
	new_image.save('foo_black_and_white.jpg')

	# Grayscale
	# Getting a grayscale image from the original one
	new_image = pyit.grayscale(image)
	new_image.save('foo_grayscale.jpg')

	# Crop and resize
	# Getting a 800px x 600px image from the original one
	new_image = pyit.resize_and_crop(image, 800, 600)
	new_image.save('foo_800x600.jpg')

	# Converting to SVG
	# Getting SVC source from and image.
	svg_source = pyit.svg_source(image)
	svg_file = open('foo.svg', 'w')
	svg_file.write(svg_source)
	svg_file.close()

# TODOs

+ Write documentation for each function.
+ Write a setup script.
+ Find a way to test/validate the SVG source.
+ Improve the *svg_source* algorithm to get a smaller SVG source.

# Support this project

Please feel free to fork the project comment about the existing functionality and suggest new features.