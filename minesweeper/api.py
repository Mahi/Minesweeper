import typing


Point = typing.NamedTuple('Point', [('x', int), ('y', int)])

VALUE_MINE = -1  # Used to indicate that a cell is a mine


class Cell:
    """An individual cell to place into a minefield.

    Each cell has a :attr:`value` attribute which indicates how many
    mines are surrounding the cell in question. A value of
    ```VALUE_MINE`` (default: ``-1``) can be used to indicate
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
