from abc import abstractmethod

class LightsController:
    def __init__(self):
        # Basic setup
        self.pixel_pin = board.D18
        self.num_pixels = 60
        self.ORDER = neopixel.GRB
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=0.2, auto_write=False, pixel_order=self.ORDER)

    @abstractmethod
    def process(self):
        pass

    def validate(self, params):
        self._validator.validate(params)
        if self._validator.errors:
            # TODO: Warning or maybe thrown error?
            return None
        return self._validator.document