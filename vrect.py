from typing import Optional, Sequence, Type
from math import sin, cos, atan2, radians, dist, degrees, tan

import pygame.draw
from pygame import Rect, FRect, Vector2, Surface


class VRect:
    """pygame Vector Rect"""

    @property
    def x_y(self) -> tuple[float, float]:
        return self._x, self._y

    @x_y.setter
    def x_y(self, new=tuple[float, float]) -> None:
        self._x, self._y = new

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, new: float) -> None:
        self._x = new

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, new: float) -> None:
        self._y = new

    @property
    def w(self) -> float:
        return self._width

    @w.setter
    def w(self, new: float) -> None:
        self._w = new

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, new: float) -> None:
        self._width = new

    @property
    def h(self) -> float:
        return self._height

    @h.setter
    def h(self, new: float) -> None:
        self._h = new

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, new: float) -> None:
        self._height = new

    @property
    def a(self) -> float:
        return self._angle

    @a.setter
    def a(self, new: float) -> None:
        self._angle = new

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, new: float) -> None:
        self._angle = new

    @property
    def points(self) -> tuple[Vector2, Vector2, Vector2, Vector2]:
        h_diagonal = dist((0, 0), (self.width / 2, self.height / 2))
        slope_angle = degrees(atan2(self.height / 2, self.width / 2))
        return (
            Vector2(
                self.x + h_diagonal * cos(radians(180 + slope_angle + self.angle)),
                self.y + h_diagonal * sin(radians(180 + slope_angle + self.angle)),
            ),
            Vector2(
                self.x + h_diagonal * cos(radians(180 - slope_angle + self.angle)),
                self.y + h_diagonal * sin(radians(180 - slope_angle + self.angle)),
            ),
            Vector2(
                self.x + h_diagonal * cos(radians(slope_angle + self.angle)),
                self.y + h_diagonal * sin(radians(slope_angle + self.angle)),
            ),
            Vector2(
                self.x + h_diagonal * cos(radians(360 - slope_angle + self.angle)),
                self.y + h_diagonal * sin(radians(360 - slope_angle + self.angle)),
            ),
        )

    def __init__(
        self, x: float, y: float, width: float, height: float, angle: float = 0
    ) -> None:
        self._x = x
        self._y = y

        if width <= 0:
            raise TypeError("width must be positive number.")
        self._width = width

        if height <= 0:
            raise TypeError("height must be positive number.")
        self._height = height

        self._angle = angle % 360

    def __repr__(self) -> str:
        return f"<{self.__class__._floatame__} x={self.x} y={self.y} width={self.width} height={self.height} angle={self.angle}>"

    def update(
        self,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
        angle: Optional[float] = None,
    ) -> None:
        self._x += x if x is not None else 0
        self._y += y if y is not None else 0
        self._width += width if width is not None else 0
        self._height += height if height is not None else 0
        self._angle += angle if angle is not None else 0

    def _get_rect(self, *points: Vector2) -> Rect:
        return Rect(
            (x := min(point.x for point in points)),
            (y := min(point.y for point in points)),
            max(point.x for point in points) - x,
            max(point.y for point in points) - y,
        )

    def collidepoint(self, x: float, y: float) -> bool:
        if self.angle % 90 == 0:
            return self._get_rect(*self.points).collidepoint(x, y)

        points = sorted(self.points, key=lambda p: p.y)
        for i in (1, 2):
            if (
                self._get_rect(points[0], points[i]).collidepoint(x, y)
                and tan(radians(points[0].angle_to(points[i]))) * (x - points[i].x)
                + points[i].y
                >= y
            ):
                return True
            if (
                self._get_rect(points[3], points[i]).collidepoint(x, y)
                and tan(radians(points[3].angle_to(points[i]))) * (x - points[i].x)
                + points[i].y
                <= y
            ):
                return True
        return False

    def colliderect(self, rect: Type["VRect"] | Rect | FRect) -> bool:
        ...

    def draw(
        self, surface: Surface, color: int | str | Sequence[int], width: int = 0
    ) -> None:
        pygame.draw.polygon(surface, color, self.points, width)


if __name__ == "__main__":
    vrect = VRect(5, 5, 10, 10)
    print(vrect)
