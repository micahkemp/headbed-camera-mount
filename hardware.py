from scadder.model import Model
from scadder.componenttypes import *

from hexagon import Hexagon

class NutHole(Model):
    diameter = 6.4
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


if __name__ == "__main__":
    NutHole(name="test_nut_hole").render("test_hardware")
