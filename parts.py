from solid.objects import circle, cube
from solid.utils import linear_extrude

from builder import SolidBuilder, empty, node


def box(
    width: float, depth: float, height: float, center: bool = False
) -> SolidBuilder:
    return node(cube([width, depth, height], center=center))


def boxoid(
    width: float, depth: float, height: float, corner_radius: float = None
) -> SolidBuilder:

    if corner_radius is None:
        return node(cube([width, depth, height]))

    quarter_width = width / 2 - corner_radius
    quarter_depth = depth / 2 - corner_radius

    g = empty().minkowski()
    g.add(cylinder(diameter=corner_radius * 2, length=height))
    g.add(box(width=quarter_width, depth=quarter_depth, height=height))

    g.back(quarter_depth)
    g.left(quarter_width)
    g.reflect_x()
    g.reflect_y()
    return g


def cylinder(diameter: float, length: float, segments: int = 48):
    n = node(linear_extrude(height=length)(circle(diameter / 2.0, segments=segments)))
    return n


def hexnut(length, diameter):
    return cylinder(diameter=diameter, length=length, segments=6)


def round_pipe_part(
    outer_diameter: float, inner_diameter: float, length: float, segments: int = 48
) -> SolidBuilder:
    g = empty()

    pipe_hole = cylinder(diameter=inner_diameter, length=length, segments=segments)
    g.add(
        cylinder(diameter=outer_diameter, length=length, segments=segments).hole(
            pipe_hole
        )
    )
    return g.part()


def square_pipe_part(
    width: float, depth: float, height: float, wall_thickness: float
) -> SolidBuilder:
    g = empty()

    pipe_hole = (
        node(cube([width - wall_thickness * 2, depth - wall_thickness * 2, height]))
        .right(wall_thickness)
        .forward(wall_thickness)
    )
    g.add(box(width, depth, height).hole(pipe_hole))
    return g.part()
