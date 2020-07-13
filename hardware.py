from scadder.model import Model
from scadder.componenttypes import *

from hexagon import Hexagon

class NutHole(Model):
    diameter = 6.2
    depth = 2.2

    def hexagon(self):
        return Hexagon(
            name="hexagon",
            diameter=self.diameter,
        ).component()

    def component(self):
        return LinearExtrude(
            name=self.name,
            height=self.depth,
            children=[
                self.hexagon(),
            ]
        )


class ScrewHole(Model):
    length = 20.7
    shaft_diameter = 3.2
    head_diameter = 5.6
    head_depth = 2.8

    def shaft_hole(self, length=None):
        return Cylinder(
            name="shaft_hole",
            diameter=self.shaft_diameter,
            height=length if length else self.length,
        )

    def head_hole(self):
        return Cylinder(
            name="head_hole",
            diameter=self.head_diameter,
            height=self.head_depth,
        )

    def component(self):
        return Union(
            name=self.name,
            children=[
                self.shaft_hole(),
                self.head_hole(),
            ],
        )


class TestHardware(Model):
    cube_length = (NutHole.depth + ScrewHole.head_depth) * 2
    cube_width = NutHole.diameter + ScrewHole.head_diameter
    cube_height = cube_width

    def test_cube(self):
        return Cube(
            name="test_cube",
            size=[self.cube_length, self.cube_width, self.cube_height]
        )

    def nut_hole_rotated(self):
        return Rotate(
            name="nut_hole_rotated",
            angle=90,
            vector=[0, 1, 0],
            children=[
                NutHole(name="nut_hole").component(),
            ]
        )

    def screw_hole_rotated(self):
        return Rotate(
            name="screw_hole_rotated",
            angle=90,
            vector=[0, -1, 0],
            children=[
                ScrewHole(name="screw_hole").component(),
            ]
        )

    def screw_hole_aligned_nut_hole(self):
        return Translate(
            name="screw_hole_aligned_nut_hole",
            vector=[self.cube_length, 0, 0],
            children=[
                self.screw_hole_rotated(),
            ]
        )

    def screw_and_nut_hole(self):
        return Union(
            name="screw_and_nut_hole",
            children=[
                self.screw_hole_aligned_nut_hole(),
                self.nut_hole_rotated(),
            ]
        )

    def screw_and_nut_hole_aligned_test_cube(self):
        return Translate(
            name="screw_and_nut_hole_aligned_test_cube",
            vector=[0, self.cube_width/2, self.cube_height/2],
            children=[
                self.screw_and_nut_hole(),
            ]
        )

    def component(self):
        return Difference(
            name=self.name,
            children=[
                self.test_cube(),
                self.screw_and_nut_hole_aligned_test_cube(),
            ]
        )

if __name__ == "__main__":
    #NutHole(name="test_nut_hole").render("test_hardware")

    #ScrewHole(name="test_screw_hole").render("test_hardware")

    TestHardware(name="test_hardware").render("test_hardware")
