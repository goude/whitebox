from typing import Dict, List

import measurements as m
from builder import SolidBuilder, empty, node
from parts import box, boxoid, cylinder, hexnut, round_pipe_part, square_pipe_part

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


def pillar(width: float, depth: float, height: float) -> SolidBuilder:
    g = empty()
    g.add(box(width, depth, height))

    lid_hole = (
        cylinder(
            length=m3_head_hole_height, diameter=m3_head_hole_tube_diameter + hole_extra
        )
        .up(height - m3_head_hole_height)
        .forward(depth / 2)
        .right(width / 2)
    )
    g -= lid_hole

    # Top nut hole insert
    top_nut_y = height - m3_head_hole_height - m3_nut_thickness_vertical_print - 1.0

    top_nut = hexnut(
        length=m3_nut_thickness_vertical_print, diameter=m3_nut_width_across_corners
    )
    top_nut += cylinder(length=20, diameter=m3_shaft_diameter_with_extra).down(10)
    top_nut.right(width / 2).forward(depth / 2).up(top_nut_y)

    top_nutbox = box(
        m3_nut_width_across_flats,
        m3_nut_width_across_flats,
        m3_nut_thickness_vertical_print,
    )
    top_nutbox.forward(depth / 2 - m3_nut_width_across_flats / 2).right(width / 2)
    top_nutbox.up(top_nut_y)

    g -= top_nut + top_nutbox

    # Bottom and mid nut holes
    bottom_nut = hexnut(length=m3_nut_thickness, diameter=m3_nut_width_across_corners)
    bottom_nut += cylinder(length=20, diameter=m3_shaft_diameter_with_extra).down(10)
    bottom_nut.rotate(90, [0, 1, 0])
    mid_nut = bottom_nut.clone().rotate(90, [0, 0, 1])
    mid_nut.forward(depth - m3_nut_thickness + pillar_delta_correction).up(
        height / 2
    ).right(width / 2)

    bottom_nut.forward(depth / 2).up(10)
    bottom_nut.right(width - m3_nut_thickness + pillar_delta_correction)

    g -= bottom_nut + mid_nut

    # Move pillar
    g.forward(box_wall_thickness)
    g.right(box_wall_thickness)

    # Outer brim of pillar
    g += box(2.0, 2.0, height)

    return g


def whitebox_part(rows=5, columns=8, height=50) -> SolidBuilder:
    g = empty()

    base_unit = 10.0  # 1 cm
    width = columns * base_unit
    depth = rows * base_unit

    # Base plate with hole and indentation
    inner_size = 8
    inner_margin = 2.0

    base_plate = box(
        width=width / 2, depth=inner_size, height=box_wall_thickness
    ) + box(width=inner_size, depth=depth / 2, height=box_wall_thickness)
    g.add(base_plate)

    # Brim
    brim_inset = 1.0
    brim_thickness = 3.0
    brim_height = 5.0

    g += (
        box(width=width / 2, depth=brim_thickness, height=brim_height)
        .forward(brim_inset)
        .right(brim_inset)
    )

    g += (
        box(width=brim_thickness, depth=depth / 2, height=brim_height)
        .right(brim_inset)
        .forward(brim_inset)
    )

    # Lid
    lid_group = empty()
    lid_plate = box(width=width, depth=depth, height=box_wall_thickness)

    # Lid shaft hole
    shaft_cyl = cylinder(
        diameter=m3_head_hole_diameter, length=m3_head_hole_height + box_wall_thickness
    )
    inner_cyl = cylinder(
        diameter=m3_shaft_diameter_with_extra, length=m3_head_hole_height
    )
    inner_cyl.down(box_wall_thickness)

    hole_part = shaft_cyl + inner_cyl
    hole_part.right(5).forward(5).down(m3_head_hole_height - box_wall_thickness)

    # Lid shaft solid parts
    outer_cyl = cylinder(
        diameter=m3_head_hole_tube_diameter, length=m3_head_hole_height
    )
    lower_disk = cylinder(
        diameter=m3_head_hole_tube_diameter, length=box_wall_thickness
    ).down(box_wall_thickness)

    plug_part = outer_cyl + lower_disk
    plug_part.right(5).forward(5).down(m3_head_hole_height - box_wall_thickness)

    lid_group += lid_plate + plug_part
    lid_group.hole(hole_part)  # here, difference does not work

    lid_height = height + 20
    lid_group.up(lid_height)

    g.add(lid_group)

    # Pillar
    g += pillar(width=inner_size, depth=inner_size, height=height)

    # Translate and mirror
    g.left(width / 2)
    g.back(depth / 2)
    g.reflect_x()
    g.reflect_y()

    # Lid cutout for screen
    lid_hole_offset = 0.1

    inky_screen = box(
        width=48.5 + lid_hole_offset,
        depth=23.8 + lid_hole_offset,
        height=5.0,
        center=True,
    )
    inky_screen.up(5)
    rpi_board = boxoid(
        width=65 + lid_hole_offset,
        depth=30 + lid_hole_offset,
        height=3,
        corner_radius=3.0,
    )
    lid_cutout = rpi_board + inky_screen
    lid_cutout.up(lid_height - 5.5)
    g -= lid_cutout

    return g


if __name__ == "__main__":
    item = whitebox_part()
    item.render_to_file(filepath="output/whitebox.scad")
