from whitebox.builder import SolidBuilder, empty
from whitebox.parts import box, boxoid, cylinder, hexnut, round_pipe_part

# Measurements
hole_extra = 0.1
pillar_delta_correction = 0.0001
box_wall_thickness = 1.0

m3_nut_thickness = 2.40
m3_nut_width_across_corners = 6.35 + 0.1  # increased slightly for looser fit
m3_nut_width_across_flats = 5.50

m3_nut_thickness_vertical_print = m3_nut_thickness + 1.0

m3_shaft_diameter = 3.0  # measured shaft: 2.83
m3_shaft_diameter_with_extra = m3_shaft_diameter + hole_extra

m3_head_hole_diameter = 6.00  # measured head: 5.5, given max: 6.35
m3_head_hole_height = 3.0  # measured head: 2.85
m3_head_hole_tube_diameter = m3_head_hole_diameter + box_wall_thickness


def pillar(
    width: float, depth: float, height: float, mid_hole=False, bottom_hole=False
) -> SolidBuilder:
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
    top_nut += cylinder(length=10, diameter=m3_shaft_diameter_with_extra).down(5)
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

    bottom_nut += cylinder(
        length=m3_head_hole_height, diameter=m3_head_hole_tube_diameter + hole_extra
    ).down(
        6
    )  # magic adjustment...

    bottom_nut.rotate(90, [0, 1, 0])
    mid_nut = bottom_nut.clone().rotate(90, [0, 0, 1])

    mid_nut.forward(depth - m3_nut_thickness + pillar_delta_correction)
    mid_nut.up((height + box_wall_thickness) / 2)
    mid_nut.right(width / 2)

    bottom_nut.forward(depth / 2).up(10)
    bottom_nut.right(width - m3_nut_thickness + pillar_delta_correction)

    # Outer brim of pillar
    g += box(2.0, 2.0, height).back(1).left(1)

    if mid_hole:
        g -= mid_nut

    if bottom_hole:
        g -= bottom_nut

    # Move pillar
    g.forward(box_wall_thickness)
    g.right(box_wall_thickness)

    return g


def lid_part(height, width, depth) -> SolidBuilder:

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

    # Lid
    lid_group += lid_plate + plug_part
    lid_group.hole(hole_part)  # here, difference does not work

    lid_height = height + 20
    lid_group.up(lid_height)

    return lid_group


def whitebox_part(rows=8, columns=8, height=20) -> SolidBuilder:
    g = empty()

    base_unit = 10.0  # 1 cm
    width = columns * base_unit
    depth = rows * base_unit
    inner_size = 8

    # Base plate with hole and indentation
    # base_plate = box(
    # width=width / 2, depth=inner_size, height=box_wall_thickness
    # ) + box(width=inner_size, depth=depth / 2, height=box_wall_thickness)

    # Base plate
    base_plate = box(width=width / 2, depth=depth / 2, height=box_wall_thickness)
    g.add(base_plate)

    # Inside screw holders
    screw_holder = round_pipe_part(outer_diameter=5, inner_diameter=2.5, length=10)
    screw_holder.right(20).forward(6)
    g.add(screw_holder)

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

    # Pillar
    g += pillar(width=inner_size, depth=inner_size, height=height)

    # Lid
    # g += lid_part(width=width, depth=depth, height=height)

    # Translate and mirror
    g.left(width / 2)
    g.back(depth / 2)
    g.reflect_x()
    g.reflect_y()

    return g


def refinements():

    # Lid cutout for screen
    lid_hole_offset = 0.1

    inky_screen = box(
        width=48.5 + lid_hole_offset,
        depth=23.8 + lid_hole_offset,
        height=5.0,
        center=True,
    )
    inky_screen.up(0)

    current_side_distance = (59.3 - 48.5) / 2
    wanted_side_distance = 2.2
    side_offset = current_side_distance - wanted_side_distance

    inky_screen_board = box(
        width=59.3 + lid_hole_offset,
        depth=29.3 + lid_hole_offset,
        height=5.0,
        center=True,
    )
    inky_screen_board.up(2.5 + 0.5)  # half height uncenters + half thickness
    inky_screen_board.left(side_offset)

    inky_wire_indentation = box(
        width=4.0 + lid_hole_offset,
        depth=18.0 + lid_hole_offset,
        height=5.0,
        center=True,
    )
    inky_wire_indentation.up(2.5 + 0.5)
    inky_wire_indentation.left(side_offset + 59.3 / 2 + 4.0 / 2)

    rpi_board = boxoid(
        width=65 + lid_hole_offset,
        depth=30 + lid_hole_offset,
        height=3,
        corner_radius=3.0,
    )
    rpi_board.up(0.7)
    rpi_board.left(side_offset)
    # 18 4
    lid_cutout = inky_screen_board + inky_screen + inky_wire_indentation  # + rpi_board
    # lid_cutout.up(lid_height - 5.5)

    lid_cutout.forward(15)
    return lid_cutout


def build_box():
    w = whitebox_part() - refinements()
    # return refinements()
    return w


if __name__ == "__main__":
    item = build_box()
    item.render_to_file(filepath="output/whitebox.scad")
