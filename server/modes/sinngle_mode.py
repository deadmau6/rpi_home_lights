from .lights_controller import LightsController

class SingleMode(LightsController):

    _validator = Validator({
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
            }
        })

    def process(self, red=0, green=0, blue=0):
        self.pixels.fill((red, green, blue))
        self.pixels.show()