from scadder.model import Model
from scadder.componenttypes import *
from interlockingpiece import InterlockingPiece
from hardware import ScrewHole, NutHole

class OuterHingePiece(Model):
    def __init__(self, name, length, thickness, interlock_width):
        self.length = length
        self.width = ScrewHole.length
        self.thickness = thickness
        self.interlock_width = interlock_width

        super(OuterHingePiece, self).__init__(name=name)

    @property
    def interlock_length(self):
        return self.thickness * 2

    @property
    def plate_length(self):
        return self.length - self.interlock_length

    @property
    def screw_offset_x(self):
        return self.plate_length + self.interlock_length/2

    @property
    def screw_offset_y(self):
        return 0

    @property
    def screw_offset_z(self):
        return self.thickness

    def plate_cube(self):
        return Cube(
            name="plate_cube",
            size=[self.plate_length, self.width, self.thickness],
        )

    def interlocking_piece(self):
        return InterlockingPiece(
            name="interlocking_piece",
            length=self.interlock_length,
            width=self.interlock_width,
        ).component()

    def front_interlocking_piece(self):
        return Translate(
            name="front_interlocking_piece",
            vector=[self.plate_length, 0, 0],
            children=[
                self.interlocking_piece(),
            ]
        )

    def rear_interlocking_piece(self):
        return Translate(
            name="rear_interlocking_piece",
            vector=[self.plate_length, self.width-self.interlock_width, 0],
            children=[
                self.interlocking_piece(),
            ]
        )

    def screw_hole(self):
        return ScrewHole(name="screw_hole").component()

    def nut_hole(self):
        return NutHole(name="nut_hole").component()

    def nut_hole_aligned_width_screw_hole(self):
        return Translate(
            name="nut_hole_aligned_width_screw_hole",
            vector=[0, 0, self.width],
            children=[
                self.nut_hole(),
            ]
        )

    def screw_and_nut_hole(self):
        return Union(
            name="screw_and_nut_hole",
            children=[
                self.screw_hole(),
                self.nut_hole_aligned_width_screw_hole(),
            ]
        )

    def screw_and_nut_hole_rotated(self):
        return Rotate(
            name="screw_and_nut_hole_rotated",
            angle=90,
            vector=[-1, 0, 0],
            children=[
                self.screw_and_nut_hole(),
            ]
        )

    def screw_and_nut_hole_aligned_interlocking_pieces(self):
        return Translate(
            name="screw_and_nut_hole_aligned_interlocking_pieces",
            vector=[self.screw_offset_x, self.screw_offset_y, self.screw_offset_z],
            children=[
                self.screw_and_nut_hole_rotated(),
            ]
        )

    def plate_cube_and_interlocking_pieces(self):
        return Union(
            name="plate_cube_and_interlocking_pieces",
            children=[
                self.plate_cube(),
                self.front_interlocking_piece(),
                self.rear_interlocking_piece(),
            ]
        )

    def component(self):
        return Difference(
            name=self.name,
            children=[
                self.plate_cube_and_interlocking_pieces(),
                self.screw_and_nut_hole_aligned_interlocking_pieces(),
            ]
        )


if __name__ == "__main__":
    outer_hinge_piece = OuterHingePiece(
        name="test_outer_hinge_piece",
        length=ScrewHole.length*1.2,
        thickness=NutHole.diameter,
        interlock_width=ScrewHole.head_depth*2,
    )

    outer_hinge_piece.render("test_outer_hinge_piece")