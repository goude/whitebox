from typing import Tuple

from solid import OpenSCADObject, scad_render_to_file
from solid.objects import translate
from solid.utils import forward, right, up

P3 = Tuple[float, float, float]
Vec3 = P3

SEGMENTS = 48


class SolidBuilder:
    def __init__(self, o: OpenSCADObject = None) -> None:
        self._oso = translate([0, 0, 0])
        self._oso.add(o)

    def set_translation(self, v: Vec3) -> "SolidBuilder":
        self._oso.add_param("v", v)
        return self

    def add(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso.add(sb.render())
        return self

    def right(self, d: float) -> "SolidBuilder":
        self._oso = right(d)(self._oso)
        return self

    def forward(self, d: float) -> "SolidBuilder":
        self._oso = forward(d)(self._oso)
        return self

    def up(self, d: float) -> "SolidBuilder":
        self._oso = up(d)(self._oso)
        return self

    def render(self) -> OpenSCADObject:
        return self._oso

    def clone(self) -> "SolidBuilder":
        return SolidBuilder(self._oso.copy())

    def render_to_file(self, filepath):
        file_out = scad_render_to_file(
            self._oso, filepath=filepath, file_header=f"$fn = {SEGMENTS};"
        )
        print(f"{__file__}: SCAD file written to: \n{file_out}")


def node(o: OpenSCADObject) -> SolidBuilder:
    return SolidBuilder(o)


def empty() -> SolidBuilder:
    return node(translate([0, 0, 0]))
