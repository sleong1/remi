#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in o, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
import remi.gui as gui
from remi.game import Color, Rect
from remi.game.canvas import Canvas
from remi.game.raster import load_image, draw, draw_from_source
from remi import start, App

import PIL.Image
import io
import time

class PILImageViewverWidget(gui.Image):
    def __init__(self, pil_image=None, **kwargs):
        super(PILImageViewverWidget, self).__init__("/res/logo.png", **kwargs)
        self._buf = None
        self.attributes['name'] = 'img_' + self.attributes['id']

    def load(self, file_path_name):
        pil_image = PIL.Image.open(file_path_name)
        self._buf = io.BytesIO()
        pil_image.save(self._buf, format='png')
        self.refresh()

    def refresh(self):
        i = int(time.time() * 1e6)
        self.attributes['src'] = "/%s/get_image_data?update_index=%d" % (id(self), i)

    def get_image_data(self, update_index):
        if self._buf is None:
            return None
        self._buf.seek(0)
        headers = {'Content-type': 'image/png'}
        return [self._buf.read(), headers]

    @property
    def id(self):
        return self.attributes['id']


class MyApp(App):
    canvas = None
    def __init__(self, *args):
        super(MyApp, self).__init__(*args)

    def main(self, name='world'):
        #margin 0px auto allows to center the app to the screen
        self.container = gui.Widget(width=600, height=600)
        
        button = gui.Button('Go!')
        button.set_on_click_listener(self.draw)
        
        self.img_container = PILImageViewverWidget(width=556, height=600)
        self.img_container.load('/home/magiclab/web_gui_ws/src/remi/examples/res/mine.png')
        self.img_container.style['display'] = 'none' #hide preloaded image
        
        self.canvas = Canvas(self, resolution=(600, 600))#, margin='0px auto')

        self.container.append(button)
        self.container.append(self.img_container)
        self.container.append(self.canvas)

        # returning the root widget
        return self.container

    def draw(self, widget):
        # image = load_image('res/cat_2.png')
        draw_from_source(self.canvas, self.img_container, (0, 0),
            556, 600)
        
if __name__ == "__main__":
    print 'Starting with pid: %s' % os.getpid()
    # starts the webserver
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(MyApp, debug=True)
