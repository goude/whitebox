from solid import scad_render_to_file
from solid.objects import circle, cube, cylinder, linear_extrude, part, translate
from solid.utils import forward, hole, left, right, screw_dimensions, up

import measurements as m
from builder import empty, node

SEGMENTS = 48


def board_pegs():
    arduino_measurements = dict(holes=[[0, 0], [0, 48.2], [50.8, 36.0], [50.8, 5.1]])
    rpi_measurements = dict(holes=[[0, 0], [0, 49.0], [58.0, 49.0], [58.0, 0.0]])
    os = [arduino_measurements, rpi_measurements]

    g = empty()

    for i, o in enumerate(os):
        for x, y in o["holes"]:
            c = node(cube()).right(x + i * 5).forward(y)
            g.add(c)

    g = g.set_translation([0, 0, 30])
    return g.render()


def board_pegs_old():
    arduino_measurements = dict(holes=[[0, 0], [0, 48.2], [50.8, 36.0], [50.8, 5.1]])

    rpi_measurements = dict(holes=[[0, 0], [0, 49.0], [58.0, 49.0], [58.0, 0.0]])
    os = [arduino_measurements, rpi_measurements]

    gs = []
    for o in os:
        for (x, y) in o["holes"]:
            # s = OpenSCADObject()
            gs.append(right(x)(forward(y)(cube())))

    g2 = translate([0, 0, 0])
    for g in gs:
        g2.add(g)

    g2.add_param("v", [5, 0, 0])

    return g2


def fibcube():
    outside = cube([m.fibcube_side, m.fibcube_side, m.fibcube_height], center=False)

    top = translate(
        [
            m.fibcube_wall + m.fibcube_extra / 2,
            m.fibcube_wall + m.fibcube_extra / 2,
            m.fibcube_height,
        ]
    )(
        cube(
            [
                m.fibcube_plopp - m.fibcube_extra,
                m.fibcube_plopp - m.fibcube_extra,
                m.fibcube_top_margin,
            ],
            center=False,
        )
    )

    inside = translate([m.fibcube_wall, m.fibcube_wall, -m.fibcube_wall])(
        cube([m.fibcube_plopp, m.fibcube_plopp, m.fibcube_height], center=False)
    )

    fc = outside + top
    fc = fc + hole()(inside)
    return fc


def fibcubes():
    g = translate([0, 0, 0])
    for x in range(2):
        g += right(x * m.fibcube_side)(fibcube())

    h = translate([0, 0, 0])
    for x in range(2):
        for y in range(2):
            h += forward(y * m.fibcube_side)(right(x * m.fibcube_side)(fibcube()))
    h = right(28)(h)

    i = translate([0, 0, 0])
    for x in range(2):
        i += right(x * (m.fibcube_side + 3))(fibcube())
    i = forward(13)(i)

    return g + h + i


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
    # item = fibcubes()
    item = board_pegs()
    file_out = scad_render_to_file(
        item, filepath="output/whitebox.scad", file_header=f"$fn = {SEGMENTS};"
    )
    print(f"{__file__}: SCAD file written to: \n{file_out}")
