from scadder import LinearExtrude, Hexagon, Union, Cylinder, Cube, Translate, XYZ, Difference


class NutHole(LinearExtrude):
    diameter = 6.2
    depth = 2.2

    def __init__(self, name="nut_hole"):
        super(NutHole, self).__init__(name=name, children=None, height=self.depth)

        self.add_child(self.hexagon())

    def hexagon(self):
        return Hexagon(
            radius=self.diameter/2,
        )


class ScrewHole(Union):
    length = 20.7
    shaft_diameter = 3.2
    head_diameter = 5.6
    head_depth = 2.8

    def __init__(self, name="screw_hole"):
        super(ScrewHole, self).__init__(name=name, children=None)

        self.add_children([
            self.shaft_hole(),
            self.head_hole(),
        ])

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


class TestHardwareCube(Difference):
    cube_length = NutHole.diameter + ScrewHole.head_diameter
    cube_width = cube_length
    cube_height = ScrewHole.length

    def __init__(self, name=None):
        super(TestHardwareCube, self).__init__(name=name, children=None)

        self.add_children([
            self.test_cube_centered(),
            self.all_holes(),
        ])

    def test_cube(self):
        return Cube(
            length=self.cube_length,
            width=self.cube_width,
            height=self.cube_height,
        )

    def test_cube_centered(self):
        return Translate(
            name="centered_cube",
            vector=XYZ(
                -self.cube_length/2,
                -self.cube_width/2,
                0,
            ),
            children=[self.test_cube()]
        )

    def nut_hole_top_of_cube(self):
        return Translate(
            name="placed_nut_hole",
            vector=XYZ(0, 0, self.cube_height-NutHole.depth),
            children=[NutHole()]
        )

    def all_holes(self):
        return Union(
            name="all_holes",
            children=[
                ScrewHole(),
                self.nut_hole_top_of_cube(),
            ]
        )


if __name__ == "__main__":
    TestHardwareCube(name="test_hardware_cube").render(output_path="test_hardware")
