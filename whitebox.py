import math
from typing import Dict, List

from solid.objects import circle, cube
from solid.utils import linear_extrude

import measurements as m
from builder import SolidBuilder, empty, node

BoardMeasurements = Dict[str, List[List[float]]]


def board_pegs() -> SolidBuilder:
    arduino_measurements: BoardMeasurements = dict(
        holes=[[0, 0], [0, 48.2], [50.8, 36.0], [50.8, 5.1]]
    )
    rpi_measurements: BoardMeasurements = dict(
        holes=[[0, 0], [0, 49.0], [58.0, 49.0], [58.0, 0.0]]
    )
    os = [arduino_measurements, rpi_measurements]

    g = empty()

    for (i, o) in enumerate(os):
        for (x, y) in o["holes"]:
            c = node(cube()).right(x + i * 5).forward(y)
            g.add(c)

    g = g.up(5)
    return g


def box(width: float, depth: float, height: float) -> SolidBuilder:
    return node(cube([width, depth, height]))


def cylinder(radius, length, segments=48):
    n = node(linear_extrude(height=length)(circle(radius, segments=segments)))
    return n


def nut(length, diameter):
    return cylinder(radius=diameter / 2, length=length, segments=48)


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


def pillar(width, depth, height, cutout) -> SolidBuilder:
    g = empty()
    g.add(box(width, depth, height))

    cutouts = (
        box(cutout, cutout, height)
        + box(cutout, cutout, height).forward(depth - cutout)
        + box(cutout, cutout, height).right(depth - cutout)
        + box(cutout, cutout, height).forward(depth - cutout).right(depth - cutout)
        + nut(length=20, diameter=3.1)
        .up(height - 20)
        .forward(depth / 2)
        .right(depth / 2)
    )
    g -= cutouts
    g.part()
    return g


def bottom(rows=5, columns=8, height=30) -> SolidBuilder:
    g = empty()

    fcs = m.fibcube_side

    width = columns * fcs
    depth = rows * fcs
    base_plate = square_pipe_part(width, depth, m.wall_thickness, fcs / 2)

    marg = m.wall_thickness
    marg_half = m.wall_thickness / 2

    inner_indentation = (
        box(width - fcs + marg, depth - fcs + marg, 20)
        .right(fcs / 2 - marg_half)
        .forward(fcs / 2 - marg_half)
        .up(marg_half)
    )

    g.add(base_plate)

    outer_indentation = (
        square_pipe_part(width + marg, depth + marg, marg, marg)
        .right(-marg_half)
        .forward(-marg_half)
        .up(marg_half)
    )

    g -= inner_indentation
    g -= outer_indentation
    g.part()

    h = empty()
    p = pillar(fcs / 2, fcs / 2, height, marg_half)
    h.add(p + p.clone().right(width - fcs / 2))
    g += h
    g += h.clone().forward(depth - fcs / 2)

    inner_brim = (
        square_pipe_part(width - marg, depth - marg, marg, marg)
        .right(marg_half)
        .forward(marg_half)
        .up(marg)
    )
    g += inner_brim
    return g


if __name__ == "__main__":
    # item = board_pegs()
    item = bottom()
    item.render_to_file(filepath="output/whitebox.scad")
