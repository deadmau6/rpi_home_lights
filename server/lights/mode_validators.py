from cerberus import Validator

class ModeValidators:
    SINGLE = Validator({
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
    RAINBOW = Validator({
            'wait': {
                'type': 'float',
                'coerce': float,
                'min': 0.001,
                'max': 1.0,
            }
        })
