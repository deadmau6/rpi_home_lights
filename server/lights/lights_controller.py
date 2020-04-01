from mode_validators import ModeValidators
from time import sleep
import board
import neopixel

class LightsController:
    def __init__(self, request):
        # Basic setup
        self.MODES = ['SINGLE', 'RAINBOW']
        self.validators = {
                    'SINGLE': ModeValidators().SINGLE,
                    'RAINBOW': ModeValidators().RAINBOW
                }
        self.pixel_pin = board.D18
        self.num_pixels = 60
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)
        # Default light mode.
        self._mode = request.get('mode', 'SINGLE')
        self._params = request.get('mode_params', {})

    def update(self, request):
        mode = request.get('mode')
        if mode and mode in self.MODES:
            self._mode = mode
        # Validate params based on current mode.
        mode_params = request.get('mode_params')
        if mode_params:
            validator = self.validators[self._mode]
            validator.validate(mode_params)
            if validator.errors:
                return validator.errors
            self._params = validator.document
        return {'mode': self._mode, 'params': self._params}

    def run(self):
        if self._mode == 'RAINBOW':
            self._rainbow(**self._params)
            return
        self._single(**self._params)
        return

    def _wheel(self, pos):
        if pos < 0 or pos:
            r = g = b = 0
        elif pos < 85:
            r = int(pos*3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if self.ORDER == neopixel.RGB or self.ORDER == neopixel.GRB else (r, g, b, 0)

    def _single(self, red=0, green=0, blue=0):
        self.pixels.fill((red, green, blue))
        self.pixels.show()

    def _rainbow(self, wait=0.001):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self._wheel(pixel_index & 255)
            self.pixels.show()
            sleep(wait)
        self.pixels.show()
