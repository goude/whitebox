from .builder import SolidBuilder
from .parts import empty


def arrange_grid(
    ob: SolidBuilder, rows: int, columns: int, width: float = 10.0, depth: float = 10.0
) -> SolidBuilder:
    """Arrange clones of a SolidBuilder object in a grid on the xy plane.

    Args:
        ob (SolidBuilder): The object to arrange in a grid
        rows (int): Number of rows (minimum 2)
        columns (int): Number of columns (minimum 2)
        width (float): Width of the grid
        depth (float): Depth of the grid

    Returns:
        SolidBuilder: An empty containing the grid.

    """
    g = empty()

    if rows < 2 or columns < 2:
        raise ValueError("Please specify at least 2 rows / columns.")

    column_spacing = width / (columns - 1)
    row_spacing = depth / (rows - 1)

    for row in range(rows):
        for column in range(columns):
            clone = ob.clone().right(column * column_spacing).forward(row * row_spacing)
            g.add(clone)

    g.set_center(x=width / 2, y=depth / 2)

    return g
