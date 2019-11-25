from typing import Tuple

from solid import OpenSCADObject, scad_render_to_file
from solid.objects import hull, minkowski, mirror, rotate, translate
from solid.utils import back, down, forward, hole, left, part, right, up

P3 = Tuple[float, float, float]
Vec3 = P3

SEGMENTS = 48


class SolidBuilder:
    def __init__(self, o: OpenSCADObject = None) -> None:
        if o is None:
            self._oso = translate([0, 0, 0])
        else:
            self._oso = o

        self.set_center()
        self.set_origin()

    def set_center(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._center_x = x
        self._center_y = y
        self._center_z = z

    def set_origin(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self._origin_x = x
        self._origin_y = y
        self._origin_z = z

    def align_center(self) -> "SolidBuilder":
        self.left(self._center_x)
        self.back(self._center_y)
        self.down(self._center_z)
        return self

    def align_origin(self) -> "SolidBuilder":
        self.left(self._origin_x)
        self.back(self._origin_y)
        self.down(self._origin_z)
        return self

    def align_center_above(self) -> "SolidBuilder":
        self.left(self._center_x)
        self.back(self._center_y)
        self.down(self._origin_z)
        return self

    def add(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso.add(sb.render())
        return self

    def right(self, d: float) -> "SolidBuilder":
        self._center_x += d
        self._origin_x += d
        self._oso = right(d)(self._oso)
        return self

    def left(self, d: float) -> "SolidBuilder":
        self._center_x -= d
        self._origin_x -= d
        self._oso = left(d)(self._oso)
        return self

    def forward(self, d: float) -> "SolidBuilder":
        self._center_y += d
        self._origin_y += d
        self._oso = forward(d)(self._oso)
        return self

    def back(self, d: float) -> "SolidBuilder":
        self._center_y -= d
        self._origin_y -= d
        self._oso = back(d)(self._oso)
        return self

    def up(self, d: float) -> "SolidBuilder":
        self._center_z += d
        self._origin_z += d
        self._oso = up(d)(self._oso)
        return self

    def down(self, d: float) -> "SolidBuilder":
        self._center_z -= d
        self._origin_z -= d
        self._oso = down(d)(self._oso)
        return self

    def translate(self, v: Vec3) -> "SolidBuilder":
        self._center_x += v[0]
        self._center_y += v[1]
        self._center_z += v[2]
        self._origin_x += v[0]
        self._origin_y += v[1]
        self._origin_z += v[2]

        self._oso = translate(v)(self._oso)
        return self

    def hole(self, sb: "SolidBuilder") -> "SolidBuilder":
        self._oso = self._oso - hole()(sb._oso)
        return self

    def part(self) -> "SolidBuilder":
        self._oso = part()(self._oso)
        return self

    def minkowski(self) -> "SolidBuilder":
        self._oso = minkowski()(self._oso)
        return self

    def hull(self) -> "SolidBuilder":
        self._oso = hull()(self._oso)
        return self

    def mirror(self, v) -> "SolidBuilder":
        self._oso = mirror(v)(self._oso)
        return self

    def mirror_clone(self, v, clone=True) -> "SolidBuilder":
        if clone:
            self += self.clone().mirror(v)
            return self
        else:
            return self.mirror(v=[1, 0, 0])

    def reflect_x(self, clone: bool = True) -> "SolidBuilder":
        return self.mirror_clone(v=[1, 0, 0], clone=clone)

    def reflect_y(self, clone: bool = True) -> "SolidBuilder":
        return self.mirror_clone(v=[0, 1, 0], clone=clone)

    def reflect_z(self, clone: bool = True) -> "SolidBuilder":
        return self.mirror_clone(v=[0, 0, 1], clone=clone)

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
    # return node(translate([0, 0, 0]))
    return node(None)
