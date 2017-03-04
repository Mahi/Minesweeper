"""Utility functions and classes used by the game."""

import typing


__all__ = (
    'KeyDefaultDict',
    'Point',
    'points_around_point',
)


class KeyDefaultDict(typing.DefaultDict):
    """Defaultdict which passes the key to :attr:`default_factory`."""

    def __missing__(self, key: typing.Hashable) -> typing.Any:
        if self.default_factory is None:
            raise KeyError(key)
        value = self[key] = self.default_factory(key)
        return value


Point = typing.NamedTuple('Point', [('x', int), ('y', int)])


def points_around_point(point: Point) -> typing.Iterator[Point]:
    """Iterate through the points surrounding a point."""
    px, py = point  # Supports normal tuples along Point
    for x in range(px - 1, px + 2):
        for y in range(py - 1, py + 2):
            if x == px and y == py:
                continue
            yield Point(x, y)
