"""Business logic classes and functions for a minesweeper game."""

import random
import typing

from utilities import Point, points_around_point


__all__ = (
    'VALUE_MINE',
    'Cell',
    'Minefield',
)


VALUE_MINE = -1  # Used to indicate that a cell is a mine


class Cell:
    """An individual cell to place into a minefield.

    Each cell has a :attr:`value` attribute which indicates how many
    mines are surrounding the cell in question. A value of
    ``VALUE_MINE`` (default: ``-1``) can be used to indicate
    that the cell itself is a mine.

    Cells have two other attributes too:
    :attr:`flagged` tells if the cell has been flagged by the user
    :attr:`visible` tells if the cell has been revealed already
    """

    def __init__(self, value: int, *, flagged: bool=False, visible: bool=False) -> None:
        self._value = value
        self.flagged = flagged
        self.visible = visible

    @property
    def value(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return 'Cell({self.value}, flagged={self.flagged}, visible={self.visible})'.format(self=self)

    def __str__(self) -> str:
        if self.flagged:
            return 'f'
        if not self.visible:
            return ' '
        if self.value == VALUE_MINE:
            return 'X'
        return str(self.value)


class Minefield:
    """A minefield of cells.

    Mostly a thin wrapper around a two-dimensional list of cells with
    a few extra methods for manipulating the cells.
    """

    def __init__(self, size: Point, n_mines: int) -> None:
        self._cells = [[Cell(0) for _ in range(size.x)] for _ in range(size.y)]
        self._n_mines = n_mines

    @property
    def n_mines(self) -> int:
        return self._n_mines

    @property
    def width(self) -> int:
        return len(self._cells[0])

    @property
    def height(self) -> int:
        return len(self._cells)

    def __repr__(self) -> str:
        return 'Minefield({width}x{height}, n_mines={n_mines}'.format(
            width=len(self._cells[0]),
            height=len(self._cells),
            n_mines=self.n_mines,
        )

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(str(cell) for cell in row)
            for row in self._cells)

    def __getitem__(self, point: Point) -> Cell:
        x, y = point  # Supports normal tuples along Point
        if x < 0 or y < 0:
            raise IndexError('Minefield doesn\'t support negative coordinates.')
        return self._cells[y][x]

    def __setitem__(self, point: Point, cell: Cell) -> None:
        x, y = point  # Supports normal tuples along Point
        self._cells[y][x] = cell

    def __iter__(self) -> typing.Iterator[Cell]:
        for row in self._cells:
            yield from row

    def iter_points(self) -> typing.Iterator[Point]:
        """Iterate through the cells' ``(x, y)`` points."""
        for y, row in enumerate(self._cells):
            for x in range(len(row)):
                yield Point(x, y)

    def cells_around_point(self, point: Point) -> typing.Iterator[Cell]:
        """Iterate through the cells surrounding a point."""
        for p in points_around_point(point):
            try:
                yield self[p]
            except IndexError:
                pass

    def count_mines_around_point(self, point: Point) -> int:
        """Get the number of mine cells around a point."""
        return sum(cell.value == VALUE_MINE for cell in self.cells_around_point(point))

    def count_flags_around_point(self, point: Point) -> int:
        """Get the number of flagged cells around a point."""
        return sum(cell.flagged for cell in self.cells_around_point(point))

    def reset(self) -> None:
        """Reset the minefield's cells to new ``Cell(0)`` instances."""
        for point in self.iter_points():
            self[point] = Cell(0)

    def init_mines(self, *, restricted_points: typing.Set[Point]=set(), reset: bool=True) -> None:
        """Initialize the minefield with :attr:`n_mines` mines.

        Points passed to ``restricted_points`` argument will be
        guaranteed not to have a mine placed in them.
        """
        if reset:
            self.reset()

        allowed_points = list(set(self.iter_points()) - restricted_points)
        random.shuffle(allowed_points)
        mine_points = allowed_points[:self.n_mines]
        other_points = set(allowed_points[self.n_mines:]) | restricted_points

        for point in mine_points:
            self[point] = Cell(VALUE_MINE)
        for point in other_points:
            self[point] = Cell(self.count_mines_around_point(point))

    def reveal_cell_at(self, point: Point, *, recursive: bool=True) -> None:
        """Attempt to reveal a cell at given ``(x, y)`` coordinates.

        If ``recursive`` is set to ``True``, this will recursively
        reveal all the surrounding cells  if the cell's value was
        equal to ``0``.

        Flagged cells cannot be revealed.
        """
        cell = self[point]
        if cell.flagged or cell.visible:
            return
        cell.visible = True
        if cell.value == 0 and recursive:
            for p in points_around_point(point):
                try:
                    self.reveal_cell_at(p)
                except IndexError:
                    pass
