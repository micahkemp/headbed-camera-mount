from scadder.model import Model
from scadder.componenttypes import *


class BedMount(Model):
    spacer_diameter = 6
    spacer_diameter_tolerance = 0.1
    spacer_height = 6
    spacer_offset = 12
    guide_width = 12.3
    guide_width_tolerance = 0.1

    @property
    def spacer_cube_length(self):
        return self.spacer_offset * 2

    @property
    def spacer_cube_width(self):
        return self.spacer_offset * 2

    @property
    def spacer_cube_height(self):
        return self.spacer_height

    def spacer_cube(self):
        return Cube(
            name="spacer_cube",
            size=[self.spacer_cube_length, self.spacer_cube_width, self.spacer_height],
        )

    @property
    def spacer_hole_diameter(self):
        return self.spacer_diameter + self.spacer_diameter_tolerance

    def spacer_hole(self):
        return Cylinder(
            name="spacer_hole",
            diameter=self.spacer_hole_diameter,
            height=self.spacer_cube_height,
        )

    def spacer_hole_placed(self):
        return Translate(
            name="spacer_hole_placed",
            vector=[self.spacer_cube_length/2, self.spacer_cube_width/2, 0],
            children=[
                self.spacer_hole(),
            ]
        )

    def spacer_cube_with_spacer_hole(self):
        return Difference(
            name="spacer_cube_with_spacer_hole",
            children=[
                self.spacer_cube(),
                self.spacer_hole_placed(),
            ]
        )

    @property
    def guide_cube_length(self):
        return self.spacer_offset * 2

    @property
    def guide_cube_width(self):
        return self.spacer_offset * 2

    @property
    def guide_cube_height(self):
        return self.spacer_height

    def guide_cube(self):
        return Cube(
            name="guide_cube",
            size=[self.guide_cube_length, self.guide_cube_width, self.guide_cube_height]
        )

    @property
    def guide_cutout_length(self):
        return self.guide_width + self.guide_width_tolerance

    @property
    def guide_cutout_width(self):
        return self.guide_cube_width

    @property
    def guide_cutout_height(self):
        return self.spacer_height

    @property
    def guide_cutout(self):
        return Cube(
            name="guide_cutout",
            size=[self.guide_width, self.guide_cube_width, self.guide_cutout_height]
        )

    def guide_cutout_placed(self):
        return Translate(
            name="guide_cutout_placed",
            vector=[
                self.guide_cube_length/2 - self.guide_cutout_length/2,
                0,
                0,
            ],
            children=[
                self.guide_cutout,
            ]
        )

    def guide_cube_with_guide_cutout(self):
        return Difference(
            name="guide_cube_with_guide_cutout",
            children=[
                self.guide_cube(),
                self.guide_cutout_placed(),
            ]
        )

    def guide_cube_with_guide_cutout_placed(self):
        return Translate(
            name="guide_cube_with_guide_cutout_placed",
            vector=[0, 0, -self.guide_cube_height],
            children=[
                self.guide_cube_with_guide_cutout(),
            ]
        )

    def component(self):
        return Union(
            name=self.name,
            children=[
                self.spacer_cube_with_spacer_hole(),
                self.guide_cube_with_guide_cutout_placed(),
            ]
        )


if __name__ == "__main__":
    BedMount("test_bed_mount").render("test_bed_mount")
