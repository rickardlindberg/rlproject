class Coordinate:

    def move(self, dx=0, dy=0):
        return self._replace(x=self.x+dx, y=self.y+dy)

class SuperTuple(tuple):

    def add(self, item):
        return SuperTuple(self+(item,))

    def map(self, fn):
        return SuperTuple([fn(x) for x in self])

    def print(self):
        for item in self:
            print(item)

class Selections(SuperTuple):

    def __repr__(self):
        return f"Selections({', '.join(repr(x) for x in self)})"
