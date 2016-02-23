class EffectTypes(object):
    """docstring for EffectTypes"""

    def __init__(self):
        pass

    def imageenhance(self):
        return ['contrast', 'brightness', 'sharpness', 'color']

    def imageops(self):
        return ['flip', 'mirror', 'grayscale']

    def image(self):
        return ['rotate']

    def imagefilter(self):
        return ['smooth', 'emboss', 'contour', 'sharpen', 'blur', 'findedges']
