from scadder import Union, Cube, Cylinder, Difference, Translate, XYZ


class BedMountSpacerComponent(Union):
    def __init__(self, height, hole_offset, hole_diameter, name=None):
        super(BedMountSpacerComponent, self).__init__(name=name, children=None)

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


class BedMountGuideRailsComponent(Difference):
    def __init__(self, guide_width, height, spacer_offset):
        super(BedMountGuideRailsComponent, self).__init__(name=None, children=None)

        self.guide_width = guide_width
        self.height = height
        self.spacer_offset = spacer_offset

        self.add_children([
            self.outer_cube(),
            self.guide_cutout(),
        ])

    @property
    def outer_cube_length(self):
        return self.spacer_offset * 2

    @property
    def outer_cube_width(self):
        return self.spacer_offset * 2

    def outer_cube(self):
        return Cube(
            name="outer_cube",
            length=self.outer_cube_length,
            width=self.outer_cube_width,
            height=self.height,
        )

    def guide_cutout(self):
        return Translate(
            name="guide_cutout",
            vector=XYZ(
                self.outer_cube_length / 2 - self.guide_width / 2,
                0,
                0,
            ),
            children=[
                Cube(
                    length=self.guide_width,
                    width=self.outer_cube_width,
                    height=self.height,
                )
            ]
        )


class BedMount(Union):
    spacer_diameter = 6.2
    spacer_height = 5.5
    spacer_offset = 12
    guide_width = 12.3

    def __init__(self, name=None):
        super(BedMount, self).__init__(name=name, children=None)

        self.add_children([
            BedMountSpacerComponent(
                name="spacer_layer",
                height=self.spacer_height,
                hole_offset=self.spacer_offset,
                hole_diameter=self.spacer_diameter,
            ),
            Translate(
                name="guide_layer",
                vector=XYZ(0, 0, -self.spacer_height),
                children=[
                    BedMountGuideRailsComponent(
                        guide_width=self.guide_width,
                        height=self.spacer_height,
                        spacer_offset=self.spacer_offset,
                    ),
                ]
            ),
        ])


if __name__ == "__main__":
    BedMount(name="test_bed_mount").render("test_bed_mount")
