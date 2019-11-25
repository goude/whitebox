from whitebox.parts import box, boxoid, empty, hexnut, round_pipe, sphere, square_pipe
from whitebox.utils import arrange_grid


def rpi_pegs():
    # arduino_measurements = dict(holes=[[0, 0], [0, 48.2], [50.8, 36.0], [50.8, 5.1]])
    # rpi_measurements = dict(holes=[[0, 0], [0, 49.0], [58.0, 49.0], [58.0, 0.0]])
    return arrange_grid(
        round_pipe(outer_diameter=3.0, inner_diameter=1.0, height=5.0),
        rows=3,
        columns=3,
        depth=49.0,
        width=58.0,
    )


def build():
    # g = rpi_pegs().align_center()
    # g += square_pipe(width=10, depth=20, height=30, wall_thickness=3).align_center()
    # g += boxoid(width=10, depth=10, height=10, corner_radius=2).align_origin()
    # g = round_pipe(outer_diameter=3.0, inner_diameter=1.0, length=5.0).align_origin()
    # g = hexnut(height=5, diameter=3).align_origin()
    # g = sphere(radius=2).align_origin()
    g = box(width=5, height=5, depth=5).translate((1, 1, 1)).align_center_above()
    return g


if __name__ == "__main__":
    item = build()
    item.render_to_file(filepath="output/whitebox.scad")
