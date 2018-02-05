#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from PIL import Image


class RasterImage(object):
    data = ''
    width = 0
    height = 0


def load_image(image_file):
    image = Image.open(image_file)
    data = image.tobytes()
    data = [ord(b) for b in data]
    result = RasterImage()
    result.width = image.size[0]
    result.height = image.size[1]
    print("Loading image, width is: " + str(result.width) +
          " height is: " + str(result.height))
    result.data = repr(data)
    return result


def draw(image, canvas, position): #Draws pixel by pixel - much slower to draw
    canvas.draw('''var canvas = document.getElementById('%s');
canvas.width = %s;
canvas.height = %s;
var ctx = canvas.getContext('2d');
var image = ctx.createImageData(%s, %s);
image.data.set(new Uint8Clamped Array(%s));
ctx.putImageData(image, %s, %s);''' % (
        canvas.id,
        canvas.style['width'].replace('px', ''),
        canvas.style['height'].replace('px', ''),
        image.width, image.height, image.data,
        position[0], position[1],
        canvas.id,
        image.width, image.height,
        position[0], position[1],  # image.data,
    ))


def draw_from_source(canvas, img_source, position, width, height):
    #Uses preloaded image so it draws faster
    #print(canvas.style)
    canvas.draw('''var canvas = document.getElementById('%s');
canvas.width = %s;
canvas.height = %s;
var ctx = canvas.getContext('2d');
var image = document.getElementById('%s');
ctx.drawImage(image, %s, %s, %s, %s);''' % (
        canvas.id,
        canvas.style['width'].replace('px', ''),
        canvas.style['height'].replace('px', ''),
        #forces default width and height to be replaced with user inputted
        img_source.identifier,
        position[0], position[1],
        width, height
    ))
