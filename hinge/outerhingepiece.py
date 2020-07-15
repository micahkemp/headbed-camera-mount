from scadder.model import Model
from scadder.componenttypes import *
from interlockingpiece import InterlockingPiece

class OuterHingePiece(Model):
    def __init__(self, name, length, width, thickness, interlock_width):
        self.length = length
        self.width = width
        self.thickness = thickness
        self.interlock_width = interlock_width

        super(OuterHingePiece, self).__init__(name=name)

    @property
    def interlock_length(self):
        return self.thickness * 2

    @property
    def plate_length(self):
        return self.length - self.interlock_length

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

    def component(self):
        return Union(
            name=self.name,
            children=[
                self.plate_cube(),
                self.front_interlocking_piece(),
                self.rear_interlocking_piece(),
            ]
        )


if __name__ == "__main__":
    outer_hinge_piece = OuterHingePiece(
        name="test_outer_hinge_piece",
        length=50,
        width=50,
        thickness=5,
        interlock_width=10,
    )

    outer_hinge_piece.render("test_outer_hinge_piece")