"""
pygame Vector Rect

author: Piop2
"""


class VectorRect:
    def __init__(self, x: float, y: float, width: float, height:float, angle: float = 0) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle


