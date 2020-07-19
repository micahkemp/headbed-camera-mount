from scadder.model import Model
from scadder.componenttypes import *

class InterlockingPiece(Model):
    def __init__(self, name, length, width):
        self.length = length
        self.width = width

        super(InterlockingPiece, self).__init__(name=name)

    def interlocking_cylinder(self):
        return Translate(
            name="interlocking_cylinder",
            vector=[self.length/2, 0, self.length/2],
            children=[
                Rotate(
                    name="interlocking_cylinder_before_translate",
                    angle=90,
                    vector=[-1, 0, 0],
                    children=[
                        Cylinder(
                            name="interlocking_cylinder_before_rotate",
                            diameter=self.length,
                            height=self.width,
                        ),
                    ],
                )
            ]
        )

    def interlocking_cube(self):
        return Cube(
            name="interlocking_cube",
            size=[self.length, self.width, self.length/2],
        )

    def component(self):
        return Union(
            name=self.name,
            children=[
                self.interlocking_cylinder(),
                self.interlocking_cube(),
            ]
        )


if __name__ == "__main__":
    interlocking_piece = InterlockingPiece(
        name="test_interlocking_piece",
        length=10,
        thickness=20,
    )

    interlocking_piece.render("test_interlocking_piece")
