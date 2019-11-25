from solid.objects import circle, cube
from solid.objects import sphere as so_sphere
from solid.utils import linear_extrude

from .builder import SolidBuilder, empty, node


def box(width: float, depth: float, height: float) -> SolidBuilder:
    """A cube."""
    c = node(cube([width, depth, height]))
    c.set_center(x=width / 2, y=depth / 2, z=height / 2)
    return c


def sphere(radius: float, segments: int = 48) -> SolidBuilder:
    s = node(so_sphere(r=radius, segments=segments))
    s.set_origin(x=-radius, y=-radius, z=-radius)
    return s


def cylinder(diameter: float, height: float, segments: int = 48):
    n = node(linear_extrude(height=height)(circle(diameter / 2.0, segments=segments)))
    n.set_origin(x=-diameter / 2, y=-diameter / 2)
    n.set_center(z=height / 2)
    return n


def hexnut(height, diameter):
    h = cylinder(diameter=diameter, height=height, segments=6)
    return h


def round_pipe(
    outer_diameter: float, inner_diameter: float, height: float, segments: int = 48
) -> SolidBuilder:
    g = empty()

    pipe_hole = cylinder(diameter=inner_diameter, height=height, segments=segments)
    g.add(
        cylinder(diameter=outer_diameter, height=height, segments=segments).hole(
            pipe_hole
        )
    )
    g.set_origin(x=-outer_diameter / 2, y=-outer_diameter / 2)
    g.set_center(z=height / 2)
    return g.part()


def square_pipe(
    width: float, depth: float, height: float, wall_thickness: float
) -> SolidBuilder:
    g = empty()

    pipe_hole = (
        node(cube([width - wall_thickness * 2, depth - wall_thickness * 2, height]))
        .right(wall_thickness)
        .forward(wall_thickness)
    )
    g.add(box(width, depth, height).hole(pipe_hole))
    g.set_center(x=width / 2, y=depth / 2, z=height / 2)
    return g.part()


def boxoid(
    width: float, depth: float, height: float, corner_radius: float
) -> SolidBuilder:
    """ A box with rounded corners. """
    if corner_radius == 0:
        return box(width=width, depth=depth, height=height)

    if corner_radius < 0:
        raise ValueError("Corner radius cannot be negative.")

    if corner_radius * 2 >= min(width, depth):
        raise ValueError("Corner radius exceeds half of width or depth.")

    # First build a quarter of the cuboid, then reflect it in x and y
    # Note: Minkowskis have to be constructed by add()-ing children.
    g = empty().minkowski()

    # Cylinder corners
    quarter_width = width / 2 - corner_radius
    quarter_depth = depth / 2 - corner_radius
    quarter_height = height / 2

    g.add(cylinder(diameter=corner_radius * 2, height=quarter_height))
    g.add(box(width=quarter_width, depth=quarter_depth, height=quarter_height))

    g.reflect_x()
    g.reflect_y()

    g.set_origin(x=-width / 2, y=-depth / 2)
    g.set_center(z=height / 2)

    return g
