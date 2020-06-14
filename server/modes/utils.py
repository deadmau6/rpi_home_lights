
class Utils:

    @staticmethod
    def string_to_bool(s):
        return s == 'True' or s =='true'

    @staticmethod
    def rgb_prime(h, c, x):
        if 0 <= h < 60:
            return c, x, 0
        if 60 <= h < 120:
            return x, c, 0
        if 120 <= h < 180:
            return 0, c, x
        if 180 <= h < 240:
            return 0, x, c
        if 240 <= h < 300:
            return x, 0, c
        return c, 0, x

    @staticmethod
    def hsv_to_rgb(h, s, v):
        # when 0 <= h < 360, 0 <= s <= 1, 0 <= v <= 1 
        c = v * s
        x = c * (1 - abs(h/60 % 2 - 1))
        m = v - c
        r, g, b = Utils.rgb_prime(h, c, x)
        return [int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)]