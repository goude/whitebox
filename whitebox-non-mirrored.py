from typing import Dict, List

import measurements as m
from builder import SolidBuilder, empty, node
from parts import box, cylinder, hexnut, round_pipe_part, square_pipe_part

# from solid.objects import cube


BoardMeasurements = Dict[str, List[List[float]]]

# Measurements
hole_extra = 0.1
vertical_print_extra = 0.2
pillar_delta_correction = 0.0001
box_wall_thickness = 1.0

m3_nut_thickness = 2.40
m3_nut_width_across_corners = 6.35
m3_nut_width_across_flats = 5.50

m3_nut_thickness_vertical_print = m3_nut_thickness + vertical_print_extra

m3_shaft_diameter = 3.0
m3_shaft_diameter_with_extra = m3_shaft_diameter + hole_extra
m3_head_diameter = 6.35
m3_head_hole_diameter = 5.0
m3_head_hole_tube_diameter = 5.0 + box_wall_thickness
m3_head_hole_height = 3.0


def pillar(width, depth, height, is_right, is_far) -> SolidBuilder:
    is_left = not is_right

    g = empty()
    g.add(box(width, depth, height))

    # Hole for countersunk lid screw
    lid_hole = (
        cylinder(
            length=m3_head_hole_height, diameter=m3_head_hole_tube_diameter + hole_extra
        )
        .up(height - m3_head_hole_height)
        .forward(depth / 2)
        .right(depth / 2)
    )
    g -= lid_hole

    # Outer brim of pillar
    outer_pillar_brim = box(2.0, 2.0, height)

    if is_right:
        outer_pillar_brim.right(width - 1.0)
    else:
        outer_pillar_brim.left(1.0)

    if is_far:
        outer_pillar_brim.forward(depth - 1.0)
    else:
        outer_pillar_brim.back(1.0)

    g += outer_pillar_brim

    # Top nut hole insert
    top_nut = hexnut(
        length=m3_nut_thickness_vertical_print, diameter=m3_nut_width_across_corners
    )
    top_nut += cylinder(length=20, diameter=m3_shaft_diameter_with_extra).down(10)
    top_nutbox = box(
        m3_nut_width_across_flats,
        m3_nut_width_across_flats,
        m3_nut_thickness_vertical_print,
    )
    top_nutbox.forward(depth / 2 - m3_nut_width_across_flats / 2)
    top_nutbox.up(height - m3_head_hole_height - m3_nut_thickness_vertical_print)
    top_nut.right(width / 2).forward(depth / 2).up(
        height - m3_head_hole_height - m3_nut_thickness_vertical_print
    )

    if is_left:
        top_nutbox.right(width - m3_nut_width_across_flats / 2)

    g -= top_nut + top_nutbox

    # Bottom and mid nut holes
    bottom_nut = hexnut(length=m3_nut_thickness, diameter=m3_nut_width_across_corners)
    bottom_nut += cylinder(length=20, diameter=m3_shaft_diameter_with_extra).down(10)
    bottom_nut.rotate(90, [0, 1, 0])
    mid_nut = bottom_nut.clone().rotate(90, [0, 0, 1])
    mid_nut.forward(depth - m3_nut_thickness + pillar_delta_correction).up(
        height - 15
    ).right(width / 2)

    bottom_nut.forward(depth / 2).up(10)

    if not is_right:
        bottom_nut.right(width - m3_nut_thickness + pillar_delta_correction)

    if is_far:
        mid_nut.back(depth - m3_nut_thickness + pillar_delta_correction * 5)

    g -= bottom_nut + mid_nut

    # Finalize part
    g.part()
    return g


def whitebox_part(rows=5, columns=8, height=30) -> SolidBuilder:
    far_right = [(False, False), (True, False), (True, True), (False, True)]

    g = empty()

    fcs = m.fibcube_side

    width = columns * fcs
    depth = rows * fcs

    # Base plate with hole and indentation
    inner_size = 8
    inner_margin = 2.0
    inner_margin_half = inner_margin / 2

    inner_indentation = (
        box(
            width - inner_size * 2 + inner_margin,
            depth - inner_size * 2 + inner_margin,
            5,
        )
        .right(inner_size - inner_margin_half)
        .forward(inner_size - inner_margin_half)
        .up(box_wall_thickness / 2)
    )

    base_plate = square_pipe_part(width, depth, box_wall_thickness, inner_size)
    g.add(base_plate)
    g -= inner_indentation
    g.part()

    # Pillars
    h = empty()
    pillar_side = 8.0
    for is_far, is_right in far_right:
        p = pillar(pillar_side, pillar_side, height, is_right=is_right, is_far=is_far)

        if is_right:
            p.right(width - pillar_side - 1.0)
        else:
            p.right(1.0)
        if is_far:
            p.forward(depth - pillar_side - 1.0)
        else:
            p.forward(1.0)

        h.add(p)
    g += h

    # Stabilizing brim
    brim_inset = 2.0
    inner_brim = (
        square_pipe_part(
            width=width - brim_inset,
            depth=depth - brim_inset,
            height=5.0,
            wall_thickness=3.0,
        )
        .right(brim_inset / 2)
        .forward(brim_inset / 2)
    )
    g += inner_brim

    # Top in the bottom - ho ho ho
    top_group = empty()
    top_plate = box(width=width, depth=depth, height=box_wall_thickness)

    plug_group = empty()
    hole_group = empty()
    for far, right in far_right:
        shaft_cyl = cylinder(diameter=m3_head_hole_diameter, length=m3_head_hole_height)
        inner_cyl = cylinder(
            diameter=m3_shaft_diameter_with_extra, length=m3_head_hole_height
        )
        inner_cyl.down(box_wall_thickness)
        hole_part = shaft_cyl + inner_cyl
        hole_part.right(5).forward(5).down(m3_head_hole_height - box_wall_thickness)

        outer_cyl = cylinder(
            diameter=m3_head_hole_tube_diameter, length=m3_head_hole_height
        )
        lower_disk = cylinder(
            diameter=m3_head_hole_tube_diameter, length=box_wall_thickness
        ).down(box_wall_thickness)

        plug_part = outer_cyl + lower_disk
        plug_part.right(5).forward(5).down(m3_head_hole_height - box_wall_thickness)
        if far:
            plug_part.forward(depth - 10)
            hole_part.forward(depth - 10)
        if right:
            plug_part.right(width - 10)
            hole_part.right(width - 10)

        plug_group += plug_part
        hole_group += hole_part

    top_group += top_plate + plug_group
    top_group -= hole_group

    top_up = 40
    top_group.up(top_up)

    g.add(top_group)
    return g


if __name__ == "__main__":
    item = whitebox_part()
    item.render_to_file(filepath="output/whitebox.scad")

"""
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
"""
