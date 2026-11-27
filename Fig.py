EMPTY_COLOR = (75, 75, 75)
BORDER_RADIUS = 3


class Fig:
    """One board cell: an empty slot, a ghost outline or a block."""

    def __init__(self, color, border, border_rad=BORDER_RADIUS, placed=False, is_fig=False) -> None:
        self.color = color
        self.border = border
        self.border_rad = border_rad
        self.placed = placed
        self.is_fig = is_fig

    @classmethod
    def empty(cls):
        return cls(EMPTY_COLOR, 1)

    @classmethod
    def block(cls, color):
        return cls(color, 0, is_fig=True)
