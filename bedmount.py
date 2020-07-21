from scadder import Union, Cube, Cylinder, Difference, Translate, XYZ


class BedMount(Union):
    spacer_diameter = 6
    spacer_diameter_tolerance = 0.1
    spacer_height = 5.5
    spacer_offset = 12
    guide_width = 12.3
    guide_width_tolerance = 0.1

    def __init__(self, name=None):
        super(BedMount, self).__init__(name=name, children=None)

        self.add_children([
            self.spacer_component(),
        ])

    @property
    def spacer_cube_length(self):
        return self.spacer_offset * 2

    @property
    def spacer_cube_width(self):
        return self.spacer_offset * 2

    @property
    def spacer_cube_height(self):
        return self.spacer_height

    @property
    def spacer_hole_diameter(self):
        return self.spacer_diameter + self.spacer_diameter_tolerance

    def spacer_cube(self):
        return Cube(
            name="spacer_cube",
            length=self.spacer_cube_length,
            width=self.spacer_cube_width,
            height=self.spacer_height,
        )

    def spacer_hole(self):
        return Translate(
            name="spacer_hole",
            vector=XYZ(self.spacer_cube_length/2, self.spacer_cube_width/2, 0),
            children=[
                Cylinder(
                    diameter=self.spacer_hole_diameter,
                    height=self.spacer_cube_height,
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


if __name__ == "__main__":
    BedMount(name="test_bed_mount").render("test_bed_mount")
