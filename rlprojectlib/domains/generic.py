class Coordinate:

    def move(self, dy):
        return self._replace(y=self.y+dy)

class SuperTuple(tuple):

    def map(self, fn):
        return SuperTuple([fn(x) for x in self])

    def print(self):
        for item in self:
            print(item)

class Selections(SuperTuple):

    def __repr__(self):
        return f"Selections({', '.join(repr(x) for x in self)})"
