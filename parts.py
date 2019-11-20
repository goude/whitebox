from solid.objects import circle, cube
from solid.utils import linear_extrude

from builder import SolidBuilder, empty, node


def box(width: float, depth: float, height: float) -> SolidBuilder:
    return node(cube([width, depth, height]))


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
