from scadder import Union, Cube, Cylinder, Difference, Translate, XYZ


class BedMountSpacerComponent(Union):
    def __init__(self, height, hole_offset, hole_diameter):
        super(BedMountSpacerComponent, self).__init__(name=None, children=None)

        self.height = height
        self.hole_offset = hole_offset
        self.hole_diameter = hole_diameter

        self.add_children([
            self.spacer_component(),
        ])

    @property
    def length(self):
        return self.hole_offset * 2

    @property
    def width(self):
        return self.hole_offset * 2

    def spacer_cube(self):
        return Cube(
            name="spacer_cube",
            length=self.length,
            width=self.width,
            height=self.height,
        )

    def spacer_hole(self):
        return Translate(
            name="spacer_hole",
            vector=XYZ(self.length/2, self.width/2, 0),
            children=[
                Cylinder(
                    diameter=self.hole_diameter,
                    height=self.height,
                )
            ]
        )

    def spacer_component(self):
        return Difference(
            name="spacer_component",
            children=[
                self.spacer_cube(),
                self.spacer_hole(),
            ]
        )

class BedMount(Union):
    spacer_diameter = 6.2
    spacer_height = 5.5
    spacer_offset = 12

    def __init__(self, name=None):
        super(BedMount, self).__init__(name=name, children=None)

        self.add_children([
            BedMountSpacerComponent(
                height=self.spacer_height,
                hole_offset=self.spacer_offset,
                hole_diameter=self.spacer_diameter,
            ),
        ])


if __name__ == "__main__":
    BedMount(name="test_bed_mount").render("test_bed_mount")
