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
    return cylinder(radius=diameter / 2, length=length, segments=6)


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


def pillar(
    width, depth, height, cutout, pillar_index, is_right, is_far
) -> SolidBuilder:
    g = empty()
    g.add(box(width, depth, height))

    cutout_shapes = [
        box(cutout, cutout, height),
        box(cutout, cutout, height).forward(depth - cutout),
        box(cutout, cutout, height).forward(depth - cutout).right(width - cutout),
        box(cutout, cutout, height).right(width - cutout),
    ]

    # nut holes
    m3_nut_thickness = 2.40
    m3_width_across_corners = 6.35
    m3_width_across_flats = 5.50
    m3_diameter = 3.1

    cutouts = (
        cylinder(length=20, radius=m3_diameter / 2)
        .up(height - 20)
        .forward(depth / 2)
        .right(depth / 2)
    )

    for i, c in enumerate(cutout_shapes):
        if i != pillar_index:
            cutouts += c

    g -= cutouts

    n = nut(length=m3_nut_thickness, diameter=m3_width_across_corners)
    n += cylinder(length=20, radius=m3_diameter / 2).down(10)

    n2 = n.clone().rotate(90, [0, 1, 0])
    n3 = n2.clone().rotate(90, [0, 0, 1])

    b = box(m3_width_across_flats, m3_width_across_flats, m3_nut_thickness)

    b.right(width - m3_width_across_flats / 2).forward(
        depth / 2 - m3_width_across_flats / 2
    ).up(25)
    n.right(width / 2).forward(depth / 2).up(25)
    g -= n + b

    delta = 0.0001

    n2.forward(depth / 2).up(10)

    if not is_right:
        n2.right(width - m3_nut_thickness + delta)

    n3.forward(depth - m3_nut_thickness + delta).up(20).right(width / 2)

    if is_far:
        n3.back(depth - m3_nut_thickness + delta * 5)

    g -= n2 + n3
    g.part()
    return g


def bottom(rows=5, columns=8, height=30) -> SolidBuilder:
    g = empty()

    fcs = m.fibcube_side

    width = columns * fcs
    depth = rows * fcs

    inner_size = 8

    base_plate = square_pipe_part(width, depth, m.wall_thickness, inner_size)

    marg = 2.0
    marg_half = marg / 2

    inner_indentation = (
        box(width - inner_size * 2 + marg, depth - inner_size * 2 + marg, 5)
        .right(inner_size - marg_half)
        .forward(inner_size - marg_half)
        .up(m.wall_thickness / 2)
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
    pillar_side = 8.0
    for i, (x, y) in enumerate(
        [(False, False), (False, True), (True, True), (True, False)]
    ):
        p = pillar(
            pillar_side,
            pillar_side,
            height,
            marg_half,
            pillar_index=i,
            is_right=x,
            is_far=y,
        )

        if x:
            p.right(width - pillar_side)
        if y:
            p.forward(depth - pillar_side)

        h.add(p)
    g += h

    inner_brim = (
        square_pipe_part(width - marg, depth - marg, 5.0, 3.0)
        .right(marg_half)
        .forward(marg_half)
    )
    g += inner_brim
    return g


if __name__ == "__main__":
    # item = board_pegs()
    item = bottom()
    item.render_to_file(filepath="output/whitebox.scad")
