from .single_mode import SingleMode
from .rainbow_mode import RainbowMode

class LightModes:
    _MODES = {
        'SINGLE': SingleMode(),
        'RAINBOW': RainbowMode()
    }

    def __init__(self, request):
        self.current_mode = request.get('mode', 'SINGLE')
        self.params = request.get('mode_params', {})

    @property
    def current_mode(self):
        return self._current_mode

    @current_mode.setter
    def current_mode(self, mode):
        if mode.upper() in self._MODES:
            self._current_mode = mode.upper()
        else:
            # TODO: maybe throw error
            self._current_mode = 'SINGLE'

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        if params is None:
            self._params = {}
        else:
            self._params = params

    def update(self, request):
        if request.get('mode'):
            self.current_mode = request.get('mode')
        if request.get('mode_params'):
            self.params = self._MODES[self.current_mode].validate(request.get('mode_params'))

    def run(self):
        self._MODES[self.current_mode].process(**self.params)
