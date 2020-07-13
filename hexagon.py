from scadder.model import Model
from scadder.componenttypes import *

from math import sin, cos, radians

class Hexagon(Model):
    def __init__(self, name, diameter):
        self.diameter = diameter

        super(Hexagon, self).__init__(name=name)

    @property
    def top_right_x(self):
        return cos(radians(60)) * self.diameter/2

    @property
    def top_right_y(self):
        return sin(radians(60)) * self.diameter/2

    def component(self):
        return Polygon(
            name=self.name,
            points=[
                [self.diameter/2, 0],
                [self.top_right_x, self.top_right_y],
                [-self.top_right_x, self.top_right_y],
                [-self.diameter/2, 0],
                [-self.top_right_x, -self.top_right_y],
                [self.top_right_x, -self.top_right_y],
            ]
        )


if __name__ == "__main__":
    Hexagon(
        name="test_hexagon",
        diameter=6,
    ).render("test_hexagon")


