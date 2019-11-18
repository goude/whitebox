from solid.objects import cube

# import measurements as m
from builder import empty, node


def board_pegs():
    arduino_measurements = dict(holes=[[0, 0], [0, 48.2], [50.8, 36.0], [50.8, 5.1]])
    rpi_measurements = dict(holes=[[0, 0], [0, 49.0], [58.0, 49.0], [58.0, 0.0]])
    os = [arduino_measurements, rpi_measurements]

    g = empty()

    for i, o in enumerate(os):
        for x, y in o["holes"]:
            c = node(cube()).right(x + i * 5).forward(y)
            g.add(c)

    g = g.up(5)
    return g


if __name__ == "__main__":
    item = board_pegs()
    item.render_to_file(filepath="output/whitebox.scad")
