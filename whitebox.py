from solid import scad_render_to_file

# from solid.objects import circle, cube, cylinder, difference, polygon, translate, union
# from solid.utils import bearing, nut, right, screw_dimensions
from solid.objects import circle, cube, linear_extrude
from solid.utils import screw_dimensions

SEGMENTS = 48


def solid_nut(screw_type="m3"):
    dims = screw_dimensions[screw_type.lower()]
    outer_rad = dims["nut_outer_diam"]
    ret = linear_extrude(height=dims["nut_thickness"])(circle(outer_rad, segments=6))
    return ret


def enclosure():
    ret = cube(size=[100, 10, 10])
    return ret


if __name__ == "__main__":
    file_out = scad_render_to_file(
        enclosure(), filepath="output/whitebox.scad", file_header=f"$fn = {SEGMENTS};"
    )
    print(f"{__file__}: SCAD file written to: \n{file_out}")
