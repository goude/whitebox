from typing import Tuple

from solid import OpenSCADObject, scad_render_to_file
from solid.objects import mirror, rotate, translate
from solid.utils import back, down, forward, hole, left, part, right, up

P3 = Tuple[float, float, float]
Vec3 = P3

SEGMENTS = 48


class SolidBuilder:
    def __init__(self, o: OpenSCADObject = None) -> None:
        self._oso = translate([0, 0, 0])
        self._oso.add(o)

    def add(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso.add(sb.render())
        return self

    def right(self, d: float) -> "SolidBuilder":
        self._oso = right(d)(self._oso)
        return self

    def left(self, d: float) -> "SolidBuilder":
        self._oso = left(d)(self._oso)
        return self

    def forward(self, d: float) -> "SolidBuilder":
        self._oso = forward(d)(self._oso)
        return self

    def back(self, d: float) -> "SolidBuilder":
        self._oso = back(d)(self._oso)
        return self

    def up(self, d: float) -> "SolidBuilder":
        self._oso = up(d)(self._oso)
        return self

    def down(self, d: float) -> "SolidBuilder":
        self._oso = down(d)(self._oso)
        return self

    def hole(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso = self._oso - hole()(sb._oso)
        return self

    def part(self) -> "SolidBuilder":
        self._oso = part()(self._oso)
        return self

    def translate(self, v: Vec3) -> "SolidBuilder":
        self._oso = translate(v)(self._oso)
        return self

    def mirror(self, v) -> "SolidBuilder":
        self._oso = mirror(v)(self._oso)
        return self

    def rotate(self, a: float, v) -> "SolidBuilder":
        self._oso = rotate(a, v)(self._oso)
        return self

    def render(self) -> OpenSCADObject:
        return self._oso

    def clone(self) -> "SolidBuilder":
        return SolidBuilder(self._oso.copy())

    def __add__(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso += sb._oso
        return self

    def __sub__(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso -= sb._oso
        return self

    def render_to_file(self, filepath):
        file_out = scad_render_to_file(
            self._oso, filepath=filepath, file_header=f"$fn = {SEGMENTS};"
        )
        print(f"{__file__}: SCAD file written to: \n{file_out}")


def node(o: OpenSCADObject) -> SolidBuilder:
    return SolidBuilder(o)


def empty() -> SolidBuilder:
    return node(translate([0, 0, 0]))
