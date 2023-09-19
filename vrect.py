from __future__ import annotations
from typing import Optional, Callable, Sequence
from math import sin, cos, atan2, radians, dist, degrees

import pygame.draw
from pygame import Rect, FRect, Vector2, Surface


ColorValue = Sequence[float] | str
RectValue = Sequence[float]


def _cos(degree: float) -> float:
    return cos(radians(degree))


def _sin(degree: float) -> float:
    return sin(radians(degree))


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
        self._angle = new % 360

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, new: float) -> None:
        self._angle = new % 360

    @property
    def points(self) -> tuple[Vector2, Vector2, Vector2, Vector2]:
        h_diagonal = dist((0, 0), (self.width / 2, self.height / 2))
        slope_angle = degrees(atan2(self.height / 2, self.width / 2))
        return (
            Vector2(
                self.x + h_diagonal * _cos(180 + slope_angle + self.angle),
                self.y + h_diagonal * _sin(180 + slope_angle + self.angle),
            ),
            Vector2(
                self.x + h_diagonal * _cos(180 - slope_angle + self.angle),
                self.y + h_diagonal * _sin(180 - slope_angle + self.angle),
            ),
            Vector2(
                self.x + h_diagonal * _cos(slope_angle + self.angle),
                self.y + h_diagonal * _sin(slope_angle + self.angle),
            ),
            Vector2(
                self.x + h_diagonal * _cos(360 - slope_angle + self.angle),
                self.y + h_diagonal * _sin(360 - slope_angle + self.angle),
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
        return f"<{self.__class__.__name__} x={self.x} y={self.y} width={self.width} height={self.height} angle={self.angle}>"

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

    def _get_rect_by_points(self, *points: Vector2) -> Rect:
        return Rect(
            (x := min(point.x for point in points)),
            (y := min(point.y for point in points)),
            max(point.x for point in points) - x,
            max(point.y for point in points) - y,
        )

    def _get_linears(
        self,
    ) -> tuple[
        Callable[[float], float],
        Callable[[float], float],
        Callable[[float], float],
        Callable[[float], float],
    ]:
        points = sorted(self.points, key=lambda p: p.y)
        linears = (
            lambda x: (points[0].y - points[1].y)
            / (points[0].x - points[1].x)
            * (x - points[0].x)
            + points[0].y,
            lambda x: (points[0].y - points[2].y)
            / (points[0].x - points[2].x)
            * (x - points[0].x)
            + points[0].y,
            lambda x: (points[3].y - points[1].y)
            / (points[3].x - points[1].x)
            * (x - points[3].x)
            + points[3].y,
            lambda x: (points[3].y - points[2].y)
            / (points[3].x - points[2].x)
            * (x - points[3].x)
            + points[3].y,
        )
        return linears

    def collidepoint(self, x: float, y: float) -> bool:
        if self.a % 90 == 0:
            return self._get_rect_by_points(*self.points).collidepoint(x, y)

        line1, line2, line3, line4 = self._get_linears()
        return line1(x) <= y and line2(x) <= y and line3(x) >= y and line4(x) >= y

    def _collide_rect(self, rect: Rect | FRect) -> bool:
        for x, y in (
            rect.topleft,
            rect.topright,
            rect.bottomleft,
            rect.bottomright,
        ):
            if self.collidepoint(x, y):
                return True
        return False
    
    def _collide_vrect(self, vrect: VRect) -> bool:
        for x, y in vrect.points:
            if self.collidepoint(x, y):
                return True
        return False

    def colliderect(self, rect: VRect | Rect | FRect | RectValue) -> bool:
        if isinstance(rect, Rect | FRect):
            return self._collide_rect(rect)
        elif isinstance(rect, Sequence) and len(rect) == 4:
            return self._collide_rect(Rect(*rect))
        elif isinstance(rect, VRect):
            return self._collide_vrect(rect)
        elif isinstance(rect, Sequence) and len(rect) == 5:
            return self._collide_vrect(VRect(*rect))
        else:
            raise TypeError("Invalid rect, 4 or 5 fields must be numeric")

    def draw(
        self,
        surface: Surface,
        color: ColorValue,
        width: int = 0,
        debug: bool = False,
        debug_color: ColorValue = "blue",
    ) -> None:
        pygame.draw.polygon(surface, color, self.points, width)

        if debug:
            points = sorted(self.points, key=lambda p: p.y)
            pygame.draw.polygon(
                surface, debug_color, (points[0], points[1], points[3], points[2]), 1
            )
            pygame.draw.aaline(surface, debug_color, points[0], points[3], 1)
            pygame.draw.aaline(surface, debug_color, points[1], points[2], 1)
            pygame.draw.aaline(
                surface,
                debug_color,
                self.x_y,
                (self.x + self.h * _cos(self.a), self.y + self.h * _sin(self.a)),
                1,
            )
