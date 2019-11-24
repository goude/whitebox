from whitebox.builder import SolidBuilder, empty
from whitebox.parts import box, boxoid, cylinder, hexnut, round_pipe_part


def build_box():
    return box(width=10, depth=10, height=10)


if __name__ == "__main__":
    item = build_box()
    item.render_to_file(filepath="output/whitebox.scad")
