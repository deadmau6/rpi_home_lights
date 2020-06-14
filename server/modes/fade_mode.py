from .lights_controller import LightsController
from .utils import Utils
from cerberus import Validator
from time import sleep

class FadeMode(LightsController):
    _validator = Validator({
            'cycle': {
                'type': 'boolean',
                'coerce': Utils.string_to_bool
            },
            'num_of_colors': {
                'type': 'integer',
                'coerce': int
            },
            'steps': {
                'type': 'integer',
                'coerce': int,
                'min': 0,
                'max': 10,
            },
            'red': {
                'type': 'integer',
                'coerce': int,
                'min': 0,
                'max': 255,
            },
            'green': {
                'type': 'integer',
                'coerce': int,
                'min': 0,
                'max': 255,
            },
            'blue': {
                'type': 'integer',
                'coerce': int,
                'min': 0,
                'max': 255,
            },
        })

    _current_index = 0

    @property
    def colors(self):
        return getattr(self, '_colors', [[255,0,0], [0,255,0], [0,0,255]])

    @setter.colors
    def colors(self, colors):
        if isinstance(colors, list):
            # maybe check r + g + b >= 255
            self._colors = colors
        else:
            # assume colors is a num
            self._colors = [Utils.hsv_to_rgb(i, 1, 1) for i in range(0, 360, int(360/colors))]

    def process(self, cycle=True, num_of_colors=3, steps=3, red=0, green=0, blue=0):
        if not cycle:
            # maybe check r + g + b >= 255
            self.colors = [[red, green, blue]]
        elif len(self.colors) != num_of_colors:
            self.colors = num_of_colors

        step_size = [int(x / steps) for x in self.colors[self._current_index]]
        current_color = [0, 0, 0]
        # fade in
        for i in range(0, steps):
            current_color = [(current_color[i] + step_size[i]) % 255 for i in range(3)]
            self.pixels.fill(current_color)
            self.pixels.show()
            sleep(1 / steps)
        # fade out
        for i in range(0, steps):
            current_color = [abs(current_color[i] - step_size[i]) % 255 for i in range(3)]
            self.pixels.fill(current_color)
            self.pixels.show()
            sleep(1 / steps)

        self._current_index = self._current_index + 1 % len(self.colors)
