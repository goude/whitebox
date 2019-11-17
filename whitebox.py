# from solid.objects import circle, cube, cylinder, difference, polygon, translate, union
# from solid.utils import bearing, nut, right, screw_dimensions
from solid import OpenSCADObject, scad_render_to_file
from solid.objects import circle, cube, cylinder, linear_extrude, part, translate
from solid.utils import fillet_2d, forward, hole, left, right, screw_dimensions, up

SEGMENTS = 48


class Measurements:
    wall_thickness = 3.0
    # note: rpi 4
    rpi_board_width = 85.0
    rpi_board_depth = 65.0
    rpi_board_height = 3.0  # not really
    rpi_cylinder = 6.0
    rpi_hole = 2.7
    rpi_hole_x_dist = 58.0
    rpi_hole_y_dist = 49.0
    enclosure_height = 10.0
    margin = 10.0
    enclosure_width = 110.0  # rpi_board_width + margin
    enclosure_depth = 80.0  # rpi_board_depth + margin

    diameter_margin = 0.1

    fibcube_side = 10.0
    fibcube_wall = 2.30
    fibcube_top_margin = 1.00
    fibcube_plopp = fibcube_side - (fibcube_wall * 2)


m = Measurements()


def fibcube(extra=0.0):
    outside = cube(m.fibcube_side, center=False)

    top = translate(
        [m.fibcube_wall + extra / 2, m.fibcube_wall + extra / 2, m.fibcube_side]
    )(
        cube(
            [m.fibcube_plopp - extra, m.fibcube_plopp - extra, m.fibcube_top_margin],
            center=False,
        )
    )

    inside = translate([m.fibcube_wall, m.fibcube_wall, -m.fibcube_wall])(
        cube([m.fibcube_plopp, m.fibcube_plopp, m.fibcube_side], center=False)
    )

    fc = outside + top
    fc = fc + hole()(inside)
    return fc


def fibcubes():
    f = fibcube(extra=0)
    for i in range(4):
        f += right(i * 20)(fibcube(extra=i * 0.1))
    return f


def board_cylinder():
    group = cube()  # FIXME: look into empties/children
    for x in [-m.rpi_hole_x_dist / 2, m.rpi_hole_x_dist / 2]:
        for y in [-m.rpi_hole_y_dist / 2, m.rpi_hole_y_dist / 2]:
            c = cylinder(r=m.rpi_cylinder / 2, h=5)

            c2 = up(m.rpi_board_height)(
                cylinder(r=m.rpi_hole / 2 - m.diameter_margin, h=m.rpi_board_height)
            )
            c = c + c2

            group += forward(y)(left(x)(c))

    return group


def solid_nut(screw_type="m3"):
    dims = screw_dimensions[screw_type.lower()]
    outer_rad = dims["nut_outer_diam"]
    ret = linear_extrude(height=dims["nut_thickness"])(circle(outer_rad, segments=6))
    return ret


def enclosure():
    enc_outer = cube(
        size=[m.enclosure_width, m.enclosure_depth, m.enclosure_height], center=True
    )

    enc_hole = up(m.wall_thickness)(
        cube(
            size=[
                m.enclosure_width - m.wall_thickness,
                m.enclosure_depth - m.wall_thickness,
                m.enclosure_height,
            ],
            center=True,
        )
    )

    enclosure = enc_outer + hole()(enc_hole)
    enclosure = part()(enclosure)
    enclosure = up(m.enclosure_height / 2)(enclosure)

    return enclosure


if __name__ == "__main__":
    # item = enclosure() + up(m.wall_thickness)(board_cylinder())
    # item = enclosure()
    item = fibcubes()
    file_out = scad_render_to_file(
        item, filepath="output/whitebox.scad", file_header=f"$fn = {SEGMENTS};",
    )
    print(f"{__file__}: SCAD file written to: \n{file_out}")
